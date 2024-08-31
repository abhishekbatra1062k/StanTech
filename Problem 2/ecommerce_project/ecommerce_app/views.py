import pandas as pd
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer
from django.db.models import Sum, Max

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"message": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

class LoadDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"message": "No file uploaded!"}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.read_csv(file)
        
        # Handle missing values
        df['price'].fillna(df['price'].median(), inplace=True)
        df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
        df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))
        
        # Ensure numeric values
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        
        for _, row in df.iterrows():
            product, created = Product.objects.get_or_create(
                product_id=row['product_id'],
                defaults={
                    'product_name': row['product_name'],
                    'category': row['category'],
                    'price': row['price'],
                    'quantity_sold': row['quantity_sold'],
                    'rating': row['rating'],
                    'review_count': row['review_count'],
                }
            )
            if not created:
                product.product_name = row['product_name']
                product.category = row['category']
                product.price = row['price']
                product.quantity_sold = row['quantity_sold']
                product.rating = row['rating']
                product.review_count = row['review_count']
                product.save()

        return Response({"message": "Data loaded successfully!"}, status=status.HTTP_201_CREATED)

class SummaryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = Product.objects.values('category').annotate(
            total_revenue=Sum('price') * Sum('quantity_sold'),
            top_product_quantity_sold=Max('quantity_sold'),
            top_product=Max('product_name')
        )
        df = pd.DataFrame(list(summary))
        df.to_csv('summary_report.csv', index=False)
        return Response({"message": "Summary report generated successfully!", "report_file": "summary_report.csv"})
