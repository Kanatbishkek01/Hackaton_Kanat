import csv
import requests
from bs4 import BeautifulSoup as bs


def get_html(url):
    response = requests.get(url)
    return response.text



def get_total_pages(html):
    soup = bs(html, 'lxml')
    pages_ul = soup.find('div', class_="pager-wrap").find('ul')
    last_page = pages_ul.find_all('li')[-1]
    total_pages = last_page.find('a').get('href').split('=')[-1]
    return int(total_pages)

def write_to_csv(data):
    with open('kivano_handys.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'],
                        data['price'],
                        data['photo']))

def get_page_data(html):
    soup = bs(html, 'lxml')
    product_list = soup.find('div', class_="product-index product-index oh").find('div', class_= "list-view")
    products = product_list.find_all('div', class_="item product_listbox oh")

    for product in products:
        # photo, title, prise
        try:
            photo = product.find('div', class_="listbox_img pull-left").find('a').find('img').get('src')
            print(photo)
        except: 
            photo = ''
        try:
            title = product.find('div', class_="listbox_title oh").find('a').text
            print(title)
        except:
            title = ''
        try:
            price = product.find('div', class_ = "motive_box pull-right").find('div').text
            print(price)
        except:
            price= ''

        data = {'title': title, 'price': price, 'photo': photo}
        write_to_csv(data)

def main():
    handys_url = 'https://www.kivano.kg/mobilnye-telefony'
    pages = '?page='
    
    total_pages = get_total_pages(get_html(handys_url))
    
    for page in range(1, total_pages+1): #25
        url_with_page = handys_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)
main()