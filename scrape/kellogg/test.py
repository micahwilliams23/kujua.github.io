from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from cs50 import SQL

#select database to save scraped data
db = SQL("sqlite:////home/ubuntu/project/scrape/food.db")

page_link = list(db.execute("SELECT link FROM cereal WHERE id = 1"))

# for page_link in page_links:

# open a connection with page that link redirects to
page_url = "https://www.specialk.com"+page_link[0]["link"]
print(f"*** PAGE_URL: {page_url} ***")
uClient = uReq(page_url)
temp_html = uClient.read()
uClient.close()

# parse HTML with BeautifulSoup
temp_soup = soup(temp_html, "html.parser")

# find link to nutritional information
nutrition_link = temp_soup.findAll("div", {"class":"smartlabel"})[0].option["value"]

# change http:// to https://
secure_link = "https"+nutrition_link[4:]

uClient = uReq(secure_link)
nutrition_html = uClient.read()
uClient.close()

nutrition_soup = soup(nutrition_html, "html.parser")

print(nutrition_soup.findAll("th",{"class":"calories"}))