from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, CartItem, Order
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, UserSerializer

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    pagination_class = StandardPagination
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser,)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related('product', 'user').all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser,)

    def get_queryset(self):
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return self.queryset.none()  # Return empty queryset for unauthenticated schema generation
        return self.queryset.filter(user=self.request.user)

    # Short-circuit schema generation for Swagger
    swagger_fake_view = True

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return self.queryset.none()  # Return empty queryset for unauthenticated schema generation
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cart_items = CartItem.objects.filter(user=self.request.user)
        total = sum(item.product.price * item.quantity for item in cart_items)
        serializer.instance.total_amount = total
        serializer.instance.save()

    # Short-circuit schema generation for Swagger
    swagger_fake_view = True

class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],  # Define required fields as a list
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='The username for the new user'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='The email address for the new user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='The password for the new user'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The optional phone number for the new user'),
            },
        ),
        responses={201: 'User created successfully', 400: 'Invalid data'}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)