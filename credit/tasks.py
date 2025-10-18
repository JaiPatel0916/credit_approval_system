from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime


@shared_task
def import_customer_data(file_path):
    df = pd.read_excel(file_path)
    
    
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
     
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': row['phone_number'],
                'monthly_income': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'age': row['age'],  # Updated column
            }
        )
    return "Customer data imported successfully"



@shared_task
def import_loan_data(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['customer_id'])
            Loan.objects.update_or_create(
                loan_id=row['loan_id'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['loan_amount'],
                    'tenure': row['tenure'],
                    'interest_rate': row['interest_rate'],
                    'monthly_installment': row['monthly_payment'],
                    'emis_paid_on_time': row['emis_paid_on_time'],  # make sure this matches Excel
                   'start_date': pd.to_datetime(row['date_of_approval']).date(),
'end_date': pd.to_datetime(row['end_date']).date(),

                }
            )
        except Customer.DoesNotExist:
            print(f"Skipping loan for unknown customer {row['customer_id']}")
    return "Loan data imported successfully"
