import requests
from bs4 import BeautifulSoup
import json

def remove_whitespace(text):
    return ' '.join(text.split())

def extract_characteristics(soup):
    characteristics = {}
    for li in soup.find_all("li"):
        span = li.find_all("span")
        characteristic_name = remove_whitespace(span[0].text)
        if span[1].find("a"):
            characteristic_value = remove_whitespace(span[1].a.text)
        else:
            characteristic_value = remove_whitespace(span[1].text)
        characteristics[characteristic_name] = characteristic_value
    return characteristics

def extract_single_characteristics(soup):
    characteristics = []
    for li in soup.find_all("li"):
        span = li.find("span")
        characteristics.append(remove_whitespace(span.text))
    return characteristics

def extract_product_details(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser").find("section", class_="adPage cf")

    product = {
        "ad_link": URL,
        "name": soup.find("h1", itemprop="name").text,
        "image_link": soup.find("a", class_="js-fancybox mfp-zoom mfp-image")["data-src"] if soup.find("a", class_="js-fancybox mfp-zoom mfp-image") else None,
        "description": soup.find("div", class_="adPage__content__description grid_18").text if soup.find("div", class_="adPage__content__description grid_18") else None,
    }

    features = soup.find("div", class_="adPage__content__features")
    spc_chr = features.find("div", class_="adPage__content__features__col grid_9 suffix_1") if features.find("div", class_="adPage__content__features__col grid_9 suffix_1") else None
    if spc_chr and spc_chr.ul:
        product[spc_chr.h2.text] = extract_characteristics(spc_chr)

    spc_chr2 = features.find("div", class_="adPage__content__features__col grid_7 suffix_1") if features.find("div", class_="adPage__content__features__col grid_7 suffix_1") else None
    if spc_chr2 and spc_chr2.ul:
        product[spc_chr2.h2.text] = extract_single_characteristics(spc_chr2)

    category = soup.find("div", class_="adPage__content__features adPage__content__features__category")
    if category.div:
        product[category.div.h2.text] = remove_whitespace(category.div.div.a.text)

    price = soup.find("ul", class_="adPage__content__price-feature__prices").find("li").find_all("span")
    price_text = " ".join(span.text for span in price)
    product["price"] = remove_whitespace(price_text)

    region = soup.find("dl", class_="adPage__content__region grid_18").find_all("dd")
    region_text = " ".join(dd.meta["content"] for dd in region)
    product["region"] = remove_whitespace(region_text)

    contact = soup.find("dl", class_="js-phone-number adPage__content__phone is-hidden grid_18").dd
    product["contact"] = contact.text if not contact.ul else contact.ul.li.a["href"]

    return product

if __name__ == "__main__":
    URL = "https://999.md/ro/83850548"  # Replace with the actual product URL
    product_details_data = extract_product_details(URL)
    print(json.dumps(product_details_data, indent=4))
