
import bs4
import requests
from bs4 import BeautifulSoup
import pandas as pd

soup = bs4.BeautifulSoup()

dataframe = pd.DataFrame()
dataframe = pd.DataFrame(columns=['Name','Variants','Manufacturer','Prescription','Price','Offer Price','Product Link','Description','Categor or Sub Category','Availablity','Image Link'])



head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

url = "https://www.1mg.com"

siteLink = "https://www.1mg.com/search/all?filter=true&name=Medicine"

def BS4SoupURL(url):
    rep = requests.get(url,headers=head)    
    return BeautifulSoup(rep.text,'lxml')

def BS4_Find(soup,Tag = None,selector = None,classname=None):
    return soup.find(Tag,attrs={selector:classname})

def BSF_Find_all(soup,Tag = None,selector = None,classname=None):
    return soup.find_all(Tag,attrs={selector:classname})   

def getData(url):
    Product = dict()
    Coffer = list()
    CPrice = list()
    cat = str()

    bs4Response = BS4SoupURL(url)
    image = BS4_Find(bs4Response,'div','class','col-xs-10 ProductImage__preview-container___2oTeX').find('img')['src'] 
    title = bs4Response.h1.getText() 
    manufacture = BS4_Find(bs4Response,'div','class','ProductTitle__manufacturer___sTfon').find('a').getText()
    comOffer = BSF_Find_all(bs4Response, 'div','class','ComboPackItem-m__pack-size___1v_fe')
    comPrice = BSF_Find_all(bs4Response,'span','class','ComboPackItem-m__combo-price___DjoMe')
  
    

    try:
        for c,cp in comOffer,comPrice:
            Coffer.append(c.text)
            CPrice.append(cp.text)
    except:
            Coffer.append("No Offer Price") 
            CPrice.append(" ")

    description = BS4_Find(bs4Response,'div','class','ProductDescription__description-content___A_qCZ')  
    Cat_and_SubCat = BS4_Find(bs4Response,'div','itemtype','http://schema.org/BreadcrumbList').find_all('span',itemprop ='name')   
    
     
    for x in Cat_and_SubCat:
         cat = cat +' -> '+ x.text 


    Product['Name'] = title
    Product['Variants'] = ''
    Product['Manufacturer'] = manufacture
    Product['Prescription'] = "Not Required"
    Product['Price'] = ''
    Product['Offer Price'] = Coffer,CPrice
    Product['Product Link'] = ''
    Product['Description'] = description.text
    Product['Categor or Sub Category'] = cat
    Product['Availablity'] = ''
    Product['Image Link'] = image

    return Product


if __name__ == "__main__":

    scrappedData = dict() 
    counter = 0
    bs4Response = BS4SoupURL(siteLink)
    bs4Findall = BSF_Find_all(bs4Response,'div','class','style__product-box___3oEU6')   
    
    for x in bs4Findall:   
        link = url + x.find('a' ,href=True)['href']
        variants =  BSF_Find_all(bs4Response,'div','class','style__pack-size___3jScl')
        amount =  BSF_Find_all(bs4Response,'div','class','style__price-tag___KzOkY')   
        in_stock = BS4_Find(bs4Response,'div','class','style__interaction___3cb12').getText() 

        if in_stock == 'ADD':
            in_stock = 'Yes in Stock'        
        else:
            in_stock = 'Not in Stock' 

        scrappedData = getData(link)
        scrappedData.update({'Price':amount[counter].text})
        scrappedData.update({'Variants':variants[counter].text})
        scrappedData.update({'Product Link':link})
        scrappedData.update({'Availablity':in_stock})

        dataframe = dataframe.append(scrappedData,ignore_index = True)
        counter +=1



print(dataframe)
dataframe.to_csv('output.csv')

