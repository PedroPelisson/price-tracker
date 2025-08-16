from celery import shared_task
from .models import Product
from .scraper import get_price
import time

@shared_task
def update_product_prices():
    print("Iniciando a tarefa de atualização de preços...")
    products = Product.objects.all()
    updated_count = 0

    for product in products:
        print(f"Verificando preço para: {product.name} ({product.id})")
        new_price = get_price(product.product_url)

        time.sleep(2) 
        
        if new_price is not None and new_price != product.current_price:
            product.current_price = new_price
            product.save()
            updated_count += 1
            print(f"Preço atualizado para {product.name}: R$ {new_price}")
    
    print(f"Tarefa concluída. {updated_count} produto(s) atualizado(s).")
    return f"{updated_count} produto(s) atualizado(s)."