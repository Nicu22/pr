import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://999.md"
MAX_PAGES = 5

def get_links_from_page(url):
    """
    Extracts product links from a given URL.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for link in soup.find_all("a", href=True, class_="js-item-ad"):
        if '/ro/' in link["href"] and link["href"] not in links:
            links.append(link["href"])

    return links

def scrape_product_details(links):
    """
    Scrapes product details from a list of product links.
    """
    product_details_list = []

    for i, link in enumerate(links[:100]):
       
        print(link, i)

    return product_details_list

def main():
    start_url = f"{BASE_URL}/ro/list/phone-and-communication/mobile-phones"
    all_links = []

    # Recursively collect links from multiple pages, up to MAX_PAGES
    for page_num in range(1, MAX_PAGES + 1):
        page_url = f"{start_url}?page={page_num}"
        page_links = get_links_from_page(page_url)

        if not page_links:
            break  # No more links found on this page

        all_links.extend(page_links)

    print("Total links:", len(all_links), ". Check links.txt")

    # Save all links to a file
    with open("links.txt", "w") as f:
        f.write("\n".join(all_links))

    print("Extracting details from top 100 links. Check all_information.txt")
    
    # Scrape product details from the first 100 links
    product_details_list = scrape_product_details(all_links)

    

if __name__ == "__main__":
    main()
