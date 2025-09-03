import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Base URL
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

titles, prices, ratings = [], [], []

for page in range(1, 6):  # scrape first 5 pages
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all("article", class_="product_pod")
for book in books:
    title = book.h3.a['title']
    price_text = book.find("p", class_="price_color").text
    price_clean = price_text.replace("Â", "").replace("£", "").strip()
    rating = book.p['class'][1]  # rating text like 'Three'
    
    titles.append(title)
    prices.append(float(price_clean))
    ratings.append(rating)


# Store in DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Rating": ratings
})

# Ensure data folder exists and save there
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
out_path = os.path.join(os.path.dirname(__file__), "..", "data", "books_data.xlsx")
df.to_excel(out_path, index=False)
print(f"Data saved to {os.path.abspath(out_path)}")
