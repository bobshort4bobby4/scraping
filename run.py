import requests # pip install requests
from bs4 import BeautifulSoup as bs # pip install beautifulsoup4
import json

# Load the webpage content
r = requests.get("https://www.toplinebolands.ie/garden/c-1069.html")
s = requests.get("https://www.toplinebolands.ie/powertool/c-1285.html")
t = requests.get("https://www.toplinebolands.ie/diy-amp-trade/c-1877.html")

# Convert to a beautiful soup object
soup = bs(r.content, "html.parser")
gazpacho = bs(s.content, "html.parser")
consomme = bs(t.content,"html.parser")

# create an empty list

product_inv_details = []

# garden_items = soup.find("ul", attrs={"id": "products-results"})
garden_items = soup.select("ul#products-results li")
powertool_items = gazpacho.select("ul#products-results li")
diy_items = consomme.select("ul#products-results li")


for index, item in enumerate(garden_items[0:50]):
    title = {
        "prod_id":1000+index,
        "category":"Garden",
        "title":item.find("div", attrs= {"class":"title products__title"}).get_text().strip(),
        "Price":int(item.find("span", attrs={"class":"price__digit"}).get_text()),
        "image_url":item.find("img", attrs= {"class":"lozad"})["data-src"]}
    product_inv_details.append(title)

for index, item in enumerate(powertool_items[0:50]):
    title = {
        "prod_id":2000+index,
        "category":"PowerTools",
        "title":item.find("div", attrs= {"class":"title products__title"}).get_text().strip(),
        "Price":float(item.find("span", attrs={"class":"price__digit"}).get_text().replace(",", "")),
        "image_url":item.find("img", attrs= {"class":"lozad"})["data-src"]}
    product_inv_details.append(title)

for index, item in enumerate(diy_items[0:50]):
    price = float(item.find("span", attrs={"class":"price__digit"}).get_text().replace(",", "")) + float(item.find("span", attrs={"class":"price__decimal"}).get_text())
    title = {
        "prod_id":3000+index,
        "category":"Diy",
        "title":item.find("div", attrs= {"class":"title products__title"}).get_text().strip(),
        "Price":price,
        "image_url":item.find("img", attrs= {"class":"lozad"})["data-src"]}
    product_inv_details.append(title)


# save as json

with open("hardware_data.json", "w") as outfile:
    json.dump( product_inv_details, outfile)

# save image urls to file

for link in product_inv_details:
    image_url = link["image_url"]
    index = link["prod_id"]
    r = requests.get(image_url).content
   
  

    with open(f"images/product_{index}.png", 'wb') as outfile:
            outfile.write(r)


   
# list(map(print, product_inv_details))

