from bs4 import BeautifulSoup
import pandas as pd

with open('./htmlset/2016round6.html','r',encoding='utf-8') as html_file :
    content=html_file.read()
    

    soup=BeautifulSoup(content,'lxml')
  

 

# Find all table bodies
table_bodies = soup.find_all('tbody')


data = []

# Iterate over each table body
for table_body in table_bodies:
    rows = table_body.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)




#setting a dataframe

df=pd.DataFrame(data)
column_names=['College','Branch','Quota','Caste','Gender','Opening Rank','Closing Rank']
df.columns=column_names
df.to_csv('2016round6.csv',index=False)