#Ali Houmani

#scrape product information from www.visions.ca
#Please have beautifulsoup installed prior to running this

import sys
import time

try:
    import urllib2 as urllib
except:

    from urllib import request as urllib

from bs4 import BeautifulSoup as BS




LIMIT_PER_CATEGORY = 2  
                       
DOMAIN_NAME = 'http://www.visions.ca'



def open_url(url):
    # time.sleep prevents the server from thinking that our
    # url request is some kind of DDOS
    time.sleep(1)
    return urllib.urlopen(url).read() 
    

def get_categories_name_from_front_page(front_page_url):
    categories_dict = {}
    html = open_url(front_page_url)
    soup = BS(html)
    ul = soup.find("ul", {'id':'mastermenu-dropdown'})
    li = ul.find_all('li')
    for each in li:
        hrefs = each.find_all('a')
        for href in hrefs:
            try:
                category_id = href['href'].split('categoryId=')
                category_id = category_id[1].split('&menu')[0]
                categories_dict[category_id] = {}
                categories_dict[category_id]['name'] = href.text
                categories_dict[category_id]['href'] = href['href'].split('&menu')[0]             
            except IndexError:
                pass
    return categories_dict


def parse_single_category(url):
    '''
    this function parses items from single category
    such as 
    http://www.visions.ca/Catalogue/Category/ProductResults.aspx?categoryId=46&menu=48
    '''
    all_hrefs = []
    html = open_url(url)
    soup = BS(html)
    divs = soup.find_all('div', {'class':'productresult-itembox'})
    for div in divs:
        hrefs = div.find('a')
        all_hrefs.append( (hrefs['href']) )
    return all_hrefs


def parse_single_item(url):
    '''
    This function parses the webpage for a single item, such as
    http://www.visions.ca/Catalogue/Category/Details.aspx?categoryId=46&productId=22372&sku=MGMPOP84
    and returns a dict
    {'title': 'title of item', 'price': '$19.99' }
    '''
    product_dict = {}
    html = open_url(url)
    soup = BS(html)
    product_detail = soup.find('div', {'id': 'productdetail-container'})
    # the title
    title = product_detail.find('h1').span.text
    
    # the price
    price_div = product_detail.find('div', {'class': 'productdetail-pricing'})
    price = price_div.span.text
    
    product_dict['title'] = title
    product_dict['price'] = price
    return product_dict
    

def save_to_database(title, price, url, availability = True):
    print('The item "{title} " costs "{price}", and is available at "{url}".'.format(
        title=title, price=price, url=url    
    ))
    pass
   
    

def main():
    all_categoris = get_categories_name_from_front_page(DOMAIN_NAME)
    for key in all_categoris:
        print("The current category is: {}".format(
            all_categoris[key]['name'].encode('utf-8')
        ))
        print('.........................................')
        
        url_to_open = DOMAIN_NAME + all_categoris[key]['href']
        single_urls = parse_single_category(url_to_open)[:LIMIT_PER_CATEGORY]
        
        for url in single_urls:
            # http://www.visions.ca/catalogue/category/Details.aspx?categoryId=143&productId=23689&sku=RXV577
            full_url = DOMAIN_NAME + '/catalogue/category/' + url
            try:            
                item_detail = parse_single_item(full_url)
                title = item_detail['title']
                price = item_detail['price']
                url = full_url 
                save_to_database(title, price, url)
            except Exception:
                pass
                      
            
        print('\n' * 4)

        
       
main()
print("Thank you for using Ali's scraper.")
sys.exit()


