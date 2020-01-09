from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from cs50 import SQL

my_url = "https://www.specialk.com/en_US/products/cereals.html"

# open connection, read and save html code, close client
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#parse html with BeautifulSoup
page_soup = soup(page_html, "html.parser")

#find all target elements
cereals = page_soup.findAll("div",{"class":"palm-one-half"})

#select database to save scraped data
db = SQL("sqlite:////home/ubuntu/project/scrape/food.db")

for cereal in cereals:

    #scrape data from element
    link = cereal.a["href"]
    product_image_link = cereal.img["src"]
    product_name = cereal.img["alt"]

    #insert data into database
    db.execute("INSERT INTO cereal (product_name, product_image_link, link) VALUES (:pn,:pil,:l)", pn=product_name, pil=product_image_link, l=link)