# from django.shortcuts import render

# # Create your views here.
# from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import PageNumberPagination
# from .models import Product
# from .serializers import ProductSerializer

# class StandardPagination(PageNumberPagination):
#     page_size = 10  # Matches settings.py
#     page_size_query_param = 'limit'
#     max_page_size = 100

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.select_related('category').all()  # Optimizes queries (no N+1)
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_fields = ['category']  # Filter by category ID
#     ordering_fields = ['price', 'created_at']  # Sort options
#     pagination_class = StandardPagination
#     lookup_field = 'id'  # For GET/PUT/DELETE /products/{id}/

from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny  # Import AllowAny
from .models import Product
from .serializers import ProductSerializer

class StandardPagination(PageNumberPagination):
    page_size = 10  # Matches settings.py
    page_size_query_param = 'limit'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()  # Optimizes queries (no N+1)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']  # Filter by category ID
    ordering_fields = ['price', 'created_at']  # Sort options
    pagination_class = StandardPagination
    lookup_field = 'id'  # For GET/PUT/DELETE /products/{id}/
    permission_classes = [AllowAny]  # Allow public access to this endpoint