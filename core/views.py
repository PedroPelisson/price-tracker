from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from .scraper import get_price


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.products.all()

    def perform_create(self, serializer):
        product_url = serializer.validated_data.get('product_url')
        
        current_price = get_price(product_url)
        
        serializer.save(owner=self.request.user, current_price=current_price)