
import requests
from bs4 import BeautifulSoup
import pandas as pd
dataframe = pd.DataFrame()
dataframe = pd.DataFrame(columns=['Name','Variants','Manufacturer','Prescription','Price','Offer Price','Product Link','Description','Categor or Sub Category','Availablity','Image Link'])

url = "https://www.1mg.com"
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
link = "https://www.1mg.com/search/all?filter=true&name=Medicine"

rep = requests.get(link,headers=head)
soup = BeautifulSoup(rep.text,'lxml')


def getData(url):
    Product = dict()
    Coffer = list()
    CPrice = list()

    rep = requests.get(url,headers=head)
    soup = BeautifulSoup(rep.text,'lxml')
    image = soup.find('div',attrs={'class':'col-xs-10 ProductImage__preview-container___2oTeX'}).find('img')['src']    
    title = soup.h1.getText()    
    manufacture = soup.find('div',attrs={'class':'ProductTitle__manufacturer___sTfon'}).find('a').getText() 
    comOffer = soup.find_all('div',attrs={'class':'ComboPackItem-m__pack-size___1v_fe'})  
    comPrice = soup.find_all('span',attrs={'class':'ComboPackItem-m__combo-price___DjoMe'})
    

    try:
        for c,cp in comOffer,comPrice:
            Coffer.append(c.text)
            CPrice.append(cp.text)
    except:
            Coffer.append("No Offer Price") 
            CPrice.append(" ")
            
    description = soup.find('div',attrs={'class':'ProductDescription__description-content___A_qCZ'})
    Cat_and_SubCat = soup.find('div',attrs={'itemtype':'http://schema.org/BreadcrumbList'}).find_all('span',itemprop ='name')

 
    cat = str() 
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



counter = 0

for x in soup.find_all('div',attrs={'class':'style__product-box___3oEU6'}):
    data = dict
    link = url + x.find('a' ,href=True)['href']    
    variants = soup.find_all('div',attrs={'class':'style__pack-size___3jScl'})[counter]
    amt = soup.find_all('div',attrs={'class':'style__price-tag___KzOkY'})[counter]    
    in_stock = soup.find('div',attrs={'class':'style__interaction___3cb12'}).get_text()

    if in_stock == 'ADD':
        in_stock = 'Yes in Stock'        
    else:
        in_stock = 'Not in Stock'
        
    
    data = getData(link)  
    data.update({'Price':amt.text})
    data.update({'Variants':variants.text})
    data.update({'Product Link':link})
    data.update({'Availablity':in_stock})
    dataframe = dataframe.append(data,ignore_index = True)
    counter +=1

print(dataframe)
dataframe.to_csv('1mg.csv')