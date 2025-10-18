from django.test import TestCase, Client
from django.urls import reverse
from .models import Customer, Loan
import json
from datetime import date


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
       
        response = self.client.post(self.url, json.dumps(self.customer_data), content_type='application/json')
        self.assertEqual(response.status_code, 201) 
        self.assertEqual(Customer.objects.count(), 1)  
        customer = Customer.objects.first()
        self.assertEqual(customer.first_name, "Jai")
        self.assertEqual(customer.approved_limit, 1800000)  



class LoanViewAPITest(TestCase):

    def setUp(self):
        self.client = Client()

       
        self.customer = Customer.objects.create(
            first_name="Jai",
            last_name="Patel",
            age=25,
            monthly_income=50000,
            approved_limit=1800000,
            current_debt=0,
            phone_number="9876543210",
            credit_score=70
        )

       
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=500000,
            tenure=12,
            interest_rate=14,
            monthly_installment=45000,
            emis_paid_on_time=12,
            start_date=date.today(),
            end_date=date.today()
        )

    def test_check_eligibility(self):
    
        url = reverse('check-eligibility')
        response = self.client.post(url, data={
            "customer_id": self.customer.customer_id,
            "loan_amount": 100000,
            "interest_rate": 12,
            "tenure": 12
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('approval', response.json())

    def test_create_loan(self):
     
        url = reverse('create-loan')
        response = self.client.post(url, data={
            "customer_id": self.customer.customer_id,
            "loan_amount": 100000,
            "interest_rate": 12,
            "tenure": 12
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('loan_approved', response.json())

    def test_view_loan(self):
       
        url = reverse('view-loan', args=[self.loan.loan_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['loan_id'], self.loan.loan_id)

    def test_view_loans_by_customer(self):
     
        url = reverse('view-loans-by-customer', args=[self.customer.customer_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['customer_id'], self.customer.customer_id)

        loans = data['loans']  
        self.assertIsInstance(loans, list)
        self.assertEqual(loans[0]['loan_id'], self.loan.loan_id)
