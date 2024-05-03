from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
from sklearn import tree

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1274444608",
            database="kiyan"
)
mycursor = mydb.cursor()
sql = "INSERT INTO cars (price, mileage, color, transmission,year,name) VALUES (%s, %s, %s, %s, %s, %s)"



for page in range(1,333):
    link2='https://www.truecar.com/used-cars-for-sale/listings/?page='+str(page)+'sort[]=best_deal_desc_script'
    r2=requests.get(link2)

    result = re.findall(r'mt-3 flex grow col-md-6 col-xl-4.+?absolute top-0 left-0 bottom-0 right-0 w-full.+?href=\"(.+?)\"', r2.text)

    for i in result:
        link3='https://www.truecar.com/'+i+'/'
        r3 = requests.get(link3)
        result3 = re.findall(r'Price.+?(\d+?,\d+?) .+?Mileage: (\d+?,\d+?) - Color: (.+?)- Transmission: (.+?) .+?content=\"(\d{4}) (.+?)\"', r3.text)

        val=(result3[0][0],result3[0][1],result3[0][2],result3[0][3],result3[0][4],result3[0][5])
        mycursor.execute(sql, val)
        mydb.commit()

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM cars")

myresult = mycursor.fetchall()

x=[]
y=[]
for i in myresult:
  x.append(i[2:6])
  y.append(i[0])

clf=tree.DecisionTreeClassifier()
clf=clf.fit(x,y)

name_new=input("what is your car name want to sell or buy?   ")
year_new=input("what is ots prouduct year?   ")
millage_new=input("what is its morked millage?  ")
color_new=input("what is its color?  ")
transmission_new=input("what is its transmission?  ")
new=[millage_new,color_new,transmission_new,year_new,name_new]

print(clf.predict(new))