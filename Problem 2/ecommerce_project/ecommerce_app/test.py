from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Product

class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'password': 'testpassword'}

    def test_user_signup(self):
        response = self.client.post(reverse('signup'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.client.post(reverse('signup'), self.user_data, format='json')
        response = self.client.post(reverse('login'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.product_data = {
            'product_id': '123',
            'product_name': 'Test Product',
            'category': 'Electronics',
            'price': 100.00,
            'quantity_sold': 10,
            'rating': 4.5,
            'review_count': 20
        }
        self.product = Product.objects.create(**self.product_data)

    def test_load_data(self):
        with open('products.csv', 'w') as f:
            f.write('product_id,product_name,category,price,quantity_sold,rating,review_count\n')
            f.write('124,Test Product 2,Electronics,150.00,5,4.0,10\n')
            f.write('125,Test Product 3,Books,150.00,5,4.0,10\n')
        
        with open('products.csv', 'rb') as f:
            response = self.client.post(reverse('load_data'), {'file': f}, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_summary_report(self):
        response = self.client.get(reverse('summary_report'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('report_file', response.data)
