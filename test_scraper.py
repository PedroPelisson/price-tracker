import requests
from bs4 import BeautifulSoup
import re

def get_price(url: str, selector: str):
    """
    Receives a URL and a CSS selector, and returns the price as a float.
    Returns None if the price cannot be found or an error occurs.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        print(f"--- Attempting to access URL: {url} ---")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("--- HTML downloaded successfully! Parsing content... ---")

        soup = BeautifulSoup(response.content, "html.parser")

        print(f"--- Searching for price with selector: '{selector}' ---")
        price_element = soup.select_one(selector)
        
        if price_element:
            price_text = price_element.get_text(strip=True)
            print(f"--- Element found! Price text: '{price_text}' ---")
            
            # Robust price cleaning
            price_only_numbers = re.sub(r'[^\d,.]', '', price_text)
            if ',' in price_only_numbers and '.' in price_only_numbers:
                 price_only_numbers = price_only_numbers.replace('.', '')
            cleaned_price_text = price_only_numbers.replace(',', '.')
            
            print(f"--- Cleaned price text: '{cleaned_price_text}' ---")
            return float(cleaned_price_text)
        else:
            print("--- ERROR: CSS selector did not find any element on the page. ---")
            return None

    except requests.exceptions.RequestException as e:
        print(f"--- CRITICAL ERROR during request: {e} ---")
        return None
    except (ValueError, TypeError) as e:
        print(f"--- CRITICAL ERROR converting price: {e} ---")
        return None

# ==============================================================================
#  TEST AREA: CHANGE THE VARIABLES BELOW TO TEST DIFFERENT SITES
# ==============================================================================
if __name__ == "__main__":
    test_url = "https://www.terabyteshop.com.br/produto/27640/cadeira-de-escritorio-dr-office-business-pro-preta-mesh-3d-altura-ajustavel"  
    css_selector = "#valVista"

    final_price = get_price(test_url, css_selector)

    print("\n================== FINAL RESULT ==================")
    if final_price is not None:
        print(f"Price found successfully: {final_price}")
    else:
        print(f"Could not extract the price.")
    print("====================================================")