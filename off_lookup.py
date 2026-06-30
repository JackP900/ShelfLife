import requests


def off_lookup(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    headers = {"User-Agent": "ShelfLife/1.0 (BeanHacks project)"}
    responce = requests.get(url, headers=headers)
    data = responce.json()

    if data["status"] == 1:
        product = data.get("product", {})
        name = product.get("product_name", "")
        category = product.get("categories", "")
        return {"name": name, "category": category, "found": True}
    else:
        return {"name": "", "category": "", "found": False}




