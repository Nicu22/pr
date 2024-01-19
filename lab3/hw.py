import requests
from bs4 import BeautifulSoup

def remove_whitespace(str):
    start = 0
    end = len(str) - 1
    for i in range(len(str)):
        if(str[i] != ' '):
            start = i
            break
    for i in range(len(str) - 1, -1, -1):
        if(str[i] != ' '):
            end = i+1
            break
    return str[start:end]

def extract_two_characteristics(soup):
    spc_chr = dict()
    for li in soup.find_all("li"):
        span = li.find_all("span")
        if(span[1].find("a") == None):
            spc_chr[remove_whitespace(span[0].text)] = remove_whitespace(span[1].text)
        else:
            spc_chr[remove_whitespace(span[0].text)] = remove_whitespace(span[1].a.text)
    return spc_chr

def extract_one_characteristic(soup):
    spc_chr = list()
    for li in soup.find_all("li"):
        span = li.find("span")
        spc_chr.append(remove_whitespace(span.text))
    return spc_chr

def product_details(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser").find("section", class_="adPage cf")
    product = {
        "ad_link" : URL,
        "name" : soup.find("h1", itemprop="name").text,
    }
    image_link = soup.find("a", class_="js-fancybox mfp-zoom mfp-image")
    if(image_link != None):
        product["image_link"] = image_link["data-src"]
    else:
        product["image_link"] = None
    
    description = soup.find("div", class_="adPage__content__description grid_18")
    if(description != None):
        product["description"] = description.text
    else:
        product["description"] = None
    features = soup.find("div", class_="adPage__content__features")
    spc_chr = features.find("div", class_="adPage__content__features__col grid_9 suffix_1")
    if(spc_chr != None):
        if(spc_chr.ul != None):
            product[spc_chr.h2.text] = extract_two_characteristics(spc_chr)
    spc_chr2 = features.find("div", class_="adPage__content__features__col grid_7 suffix_1")
    if(spc_chr2 != None):
        if(spc_chr2.ul != None):
            product[spc_chr2.h2.text] = extract_one_characteristic(spc_chr2)
    category = soup.find("div", class_="adPage__content__features adPage__content__features__category")
    if(category.div != None):
        product[category.div.h2.text] = remove_whitespace(category.div.div.a.text)
    price = soup.find("ul", class_="adPage__content__price-feature__prices").find("li").find_all("span")
    price_text = ""
    for span in price:
        price_text += span.text
    product["price"] = remove_whitespace(price_text)
    region = soup.find("dl", class_="adPage__content__region grid_18").find_all("dd")
    region_text = ''
    for dd in region:
        region_text += ' ' + dd.meta["content"]
    product["region"] = remove_whitespace(region_text)
    contact = soup.find("dl", class_="js-phone-number adPage__content__phone is-hidden grid_18").dd
    if(contact.ul == None):
        product["contact"] = contact.text
    else:
        product["contact"] = contact.ul.li.a["href"]
    return product