# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Product, Order
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer

class CustomerListCreateView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListCreateView(APIView):
    try:
        def get(self, request):
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
    except Exception as e:
        print(e)
        
    try:
        def post(self, request):
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

class OrderDetailsUpdateView(APIView):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderByProductListView(APIView):
    def get(self, request):
        product_names = request.query_params.get('products', '').split(',')
        orders = Order.objects.filter(items__product__name__in=product_names).distinct()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderByCustomerListView(APIView):
    def get(self, request):
        customer_name = request.query_params.get('customer', '')
        orders = Order.objects.filter(customer__name=customer_name)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
