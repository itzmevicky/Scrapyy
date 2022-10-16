
import pandas as p
import pyshorteners

def shortenLink(url):    
    type_tiny = pyshorteners.Shortener()
    if type(url) == type(str()):        
        short_url = type_tiny.tinyurl.short(url)
        return short_url


csv = p.read_csv('Flipkart.csv')
meltvalues = p.melt(csv,id_vars=('Sr No','Product Name'),value_name='Link',var_name='Flipkart Id')
df = p.DataFrame(meltvalues,columns=['Sr No','Product Name','Link'])
df2 = p.DataFrame()


count = 0
l = 1
for x in df.index:
    xlink = str(df['Link'][x]).split('/') 
    for y in range(l,len(df.index)):
        ylink = str(df['Link'][y]).split('/')  
        if 'nan' not in ylink and 'nan' not in xlink :
            if xlink[3] == ylink[3]:
                count =+1
    if count == 1:
        FinalValues = {
            'Sr No':df['Sr No'][x],
            'Product Name':df['Product Name'][x],
            'Link':shortenLink(df['Link'][x])
        }
        df2 = df2.append(FinalValues,ignore_index = True)        
    count = 0     
    l+=1
    
print(df2)

    
        
    
    
    


    
    
    