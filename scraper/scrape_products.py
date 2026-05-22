import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin

BASE_URL = "https://www.transformerindia.com"

product_pages = [
    "/products-and-services/power-transformers",
    "/products-and-services/furnace-transformers",
]

os.makedirs("../images", exist_ok=True)

all_products = []

for page in product_pages:

    url = BASE_URL + page

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text.strip()

    paragraphs = soup.find_all("p")

    content = " ".join(
        [p.text.strip() for p in paragraphs]
    )

    img = soup.find("img")

    image_url = urljoin(BASE_URL, img["src"])

    image_name = image_url.split("/")[-1]

    image_path = f"../images/{image_name}"

    image_data = requests.get(image_url).content

    with open(image_path, "wb") as f:
        f.write(image_data)

    all_products.append({
        "title": title,
        "content": content,
        "image_path": image_path,
        "source": url
    })

with open("../data/raw/products.json", "w") as f:
    json.dump(all_products, f, indent=4)

print("Scraping Completed")