from email import header
from turtle import title
from numpy import var
import requests
from bs4 import BeautifulSoup
url = "https://www.1mg.com"
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
link = "https://www.1mg.com/search/all?name=Medicine"

rep = requests.get(link,headers=head)
soup = BeautifulSoup(rep.text,'lxml')


def getData(url):
    prdType = list()
    price = list()
    rep = requests.get(url,headers=head)
    soup = BeautifulSoup(rep.text,'lxml')
    image = soup.find('div',attrs={'class':'col-xs-10 ProductImage__preview-container___2oTeX'}).find('img')['src']
    print(image)
    title = soup.h1.getText()
    print(title)
    manufacture = soup.find('div',attrs={'class':'ProductTitle__manufacturer___sTfon'}).find('a').getText()
    print(manufacture)
    variants = soup.find_all('div',attrs={'class':'OtcVariantsItem__variant-text___1Grsz'}) 
    amt = soup.find_all('div',attrs={'class':'OtcVariantsItem__variant-price___3RfP5'})

    for x , y in variants,amt:
        prdType.append(x.text)
        price.append(y.text)

    # for x in amt:
    #     price.append(x.text)

    print(prdType,price )

for x in soup.find_all('div',attrs={'class':'style__product-box___3oEU6'}):
    getData(url + x.find('a' ,href=True)['href'])    
    break

