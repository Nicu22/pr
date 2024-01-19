import requests
from bs4 import BeautifulSoup
from homework import product_details
import json

def return_handler(_links):
    for i in range(len(_links)):
        _links[i] = "https://999.md" + _links[i]
    return _links

def recursion(_URL, _links, max_pages=100, current_page=1):

    #max page handling
    if(max_pages == current_page - 1):
        return return_handler(_links)
    
    #html handling
    r = requests.get(_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    a = soup.find_all("a", href=True, class_="js-item-ad")
    for link in a:
        '/ro/' in link["href"]
        link["href"] not in _links
        if('/ro/' in link["href"] and link["href"] not in _links):
            _links.append(link["href"])

    #next page handling
    nav = soup.find("nav", class_="paginator cf")
    li = nav.ul.find_all("li")
    page_URL = None
    for i in li:
        if(str(current_page) in i.text):
            page_URL = "https://999.md" + i.find("a")["href"]
            break
    
    #if no next page, finish recursion
    if page_URL == None:
        return return_handler(_links)
    
    return recursion(page_URL, _links, max_pages, current_page=current_page+1)

if __name__ == "__main__":
    URL = "https://999.md/ro/list/computers-and-office-equipment/video"
    links = []
    links = recursion(URL, links)
    amm = len(links)
    product_details_list = list()
    print("Total links:", amm, ". check links.txt")
    print("Extracting details from top 100 links, check all_information.txt")
    with open("links.txt", "w") as f:
        for i in range(len(links)):
            f.write(links[i] + '\n')
        f.close()
    for i in range(100):
        product_details_list.append(product_details(links[i]))
        print(links[i], i)
    with open("all_information.txt", "w") as f:
        f.write(json.dumps(product_details_list, indent=4))
    f.close()