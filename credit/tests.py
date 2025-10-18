from django.test import TestCase, Client
from django.urls import reverse
from .models import Customer
import json

class CustomerRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')  
        self.customer_data = {
            "first_name": "Jai",
            "last_name": "Patel",
            "age": 25,
            "monthly_income": 50000,
            "phone_number": "1234567890"
        }

    def test_register_customer_success(self):
        """Test that a customer is created successfully"""
        response = self.client.post(self.url, json.dumps(self.customer_data), content_type='application/json')
        self.assertEqual(response.status_code, 201) 
        self.assertEqual(Customer.objects.count(), 1)  
        customer = Customer.objects.first()
        self.assertEqual(customer.first_name, "Jai")
        self.assertEqual(customer.approved_limit, 1800000)  
