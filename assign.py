import requests
from bs4 import BeautifulSoup
import csv
import time
def scrape_amazon_products(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
         print(f"Error in request: {e}")
    # Handle the error or exit the script

    response = requests.get(url, headers=headers)
    time.sleep(2)
    print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    for product in soup.select('.s-result-item'):
        title_elem = product.select_one('.a-text-normal')
        price_elem = product.select_one('.a-offscreen')
        rating_elem = product.select_one('.a-icon-star span[data-asin="B07VGRJDFY"]')  # Adjust the selector
        reviews_elem = product.select_one('.a-size-small .a-link-normal')
        availability_elem = product.select_one('.a-text-bold span.a-declarative span')

        title = title_elem.get_text(strip=True) if title_elem else 'NA'
        price = price_elem.get_text(strip=True) if price_elem else 'NA'
        
        # Extracting rating with more flexibility
        rating = 'NA'
        if rating_elem:
            rating = rating_elem.get_text(strip=True)
        else:
            rating_elem = product.select_one('.a-icon-star-small')
            if rating_elem:
                rating = rating_elem.find_next('span').get_text(strip=True)

        reviews = reviews_elem.get_text(strip=True) if reviews_elem else 'NA'
        availability_text = availability_elem.get_text(strip=True) if availability_elem else 'NA'
        is_out_of_stock = 'Yes' if 'Currently unavailable' in availability_text else 'No'

        product_data = {
            'Product Title': title,
            'Product Price': price,
            'Overall Rating': rating,
            'Total Reviews': reviews,
            'Out of Stock': is_out_of_stock  # Updated column heading
        }

        products.append(product_data)

    return products

def write_to_csv(products, filename='amazon_products.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product Title', 'Product Price', 'Overall Rating', 'Total Reviews', 'Out of Stock']  # Updated column heading
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for product in products:
                writer.writerow(product)

def main(url):
    products = scrape_amazon_products(url)
    write_to_csv(products)
    print(f"Scraped {len(products)} products. Data written to 'amazon_products.csv'.")
    
if __name__ == '__main__':
    url = 'https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar'
    main(url)
