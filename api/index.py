import requests
from bs4 import BeautifulSoup

def handler(request):

    keywords = ["asus", "hp", "lenovo", "msi"]
    rows = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i in keywords:

        url = f"https://els.id/product-category/laptop/laptop-by-brand/{i}-laptop-by-brand-laptop-default-category/?per_page=1000"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all(class_="product-info")

            for product in products:
                try:
                    name = product.find(class_="product-title").text.strip()
                    price = product.find(class_="woocommerce-Price-amount amount").text.strip()

                    price = price.replace("Rp", "").replace(",", "").replace(".00", "").strip()
                    price = int(price)

                    rows.append({
                        "toko": "ELS",
                        "sku": i,
                        "nama_produk": name,
                        "harga": price
                    })

                except:
                    pass

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "total": len(rows),
            "data": rows
        }
    }