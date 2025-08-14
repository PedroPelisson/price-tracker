import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

SITE_CONFIGS = {
    'www.kabum.com.br': {
        'selector': '#main-content > div.flex.flex-col.gap-8.tablet\:gap-16.desktop\:gap-32.bg-white > div.container-lg.relative > div.grid.grid-cols-4.tablet\:grid-cols-6.desktop\:grid-cols-12.gap-16.desktop\:gap-32.mt-16 > div.col-span-4.tablet\:col-span-6.desktop\:col-span-3.order-3.desktop\:top-\[88px\].desktop\:z-\[9\].h-fit.space-y-16.desktop\:sticky > div.w-full.p-8.rounded-8.border-solid.border.border-black-400 > h4',
    },
}

def clean_price(price_text):
    if not price_text:
        return None
    try:
        price_only_numbers = re.sub(r'[^\d,.]', '', price_text)
        if ',' in price_only_numbers and '.' in price_only_numbers:
            price_only_numbers = price_only_numbers.replace('.', '')
        standardized_price = price_only_numbers.replace(',', '.')
        return float(standardized_price)
    except (ValueError, TypeError):
        return None

def get_price(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    }
    
    domain = urlparse(url).netloc
    
    if domain not in SITE_CONFIGS:
        print(f"Erro: O site {domain} não é suportado.")
        return None

    config = SITE_CONFIGS[domain]
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        price_element = soup.select_one(config['selector'])
        
        if price_element:
            return clean_price(price_element.get_text())
        else:
            print(f"Seletor '{config['selector']}' não encontrou o preço para {domain}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição para {url}: {e}")
        return None