from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
import math

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def register_customer(request):
    try:
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        age = request.data.get('age')
        monthly_income = float(request.data.get('monthly_income'))
        phone_number = request.data.get('phone_number')

        approved_limit = round((36 * monthly_income) / 100000) * 100000

        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            monthly_income=monthly_income,
            approved_limit=approved_limit,
            phone_number=phone_number,
            current_debt=0
        )

        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    

# @csrf_exempt
# def check_eligibility(request):
 
#     if request.method == 'POST':
#         try:
#             import json
#             data = json.loads(request.body)
#             customer_id = data.get('customer_id')

#             if not customer_id:
#                 return JsonResponse({'error': 'customer_id is required'}, status=400)

#             # Try to find the customer
#             customer = Customer.objects.filter(customer_id=customer_id).first()
#             if not customer:
#                 return JsonResponse({'error': 'Customer not found'}, status=404)

#             # Basic eligibility logic (you can adjust later)
#             if customer.age < 21:
#                 return JsonResponse({'eligible': False, 'reason': 'Customer is below 21 years old'})

#             if customer.monthly_income < 15000:
#                 return JsonResponse({'eligible': False, 'reason': 'Income too low'})

#             if customer.credit_score < 650:
#                 return JsonResponse({'eligible': False, 'reason': 'Credit score too low'})

#             # If all checks passed
#             return JsonResponse({'eligible': True, 'message': 'Customer is eligible for a loan'})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def check_eligibility(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        import json
        from datetime import datetime

        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        loan_amount = float(data.get('loan_amount', 0))
        interest_rate = float(data.get('interest_rate', 0))
        tenure = int(data.get('tenure', 0))

        if not customer_id:
            return JsonResponse({'error': 'customer_id is required'}, status=400)

        customer = Customer.objects.filter(customer_id=customer_id).first()
        if not customer:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        past_loans = Loan.objects.filter(customer=customer)

        credit_score = 0

    
        on_time_loans = past_loans.filter(paid_on_time=True).count()
        credit_score += min(on_time_loans * 10, 30)

        
        total_loans = past_loans.count()
        credit_score += min(total_loans * 5, 20)

       
        current_year = datetime.now().year
        loans_this_year = past_loans.filter(created_at__year=current_year).count()
        credit_score += min(loans_this_year * 5, 10)

      
        approved_volume = sum([loan.loan_amount for loan in past_loans])
        credit_score += min(approved_volume / 100000 * 10, 20)  # scaled

        if customer.current_debt + loan_amount > customer.approved_limit:
            credit_score = 0

        approve = False
        corrected_interest_rate = interest_rate

        if credit_score > 50:
            approve = True
            corrected_interest_rate = max(interest_rate, 12)
        elif 30 < credit_score <= 50:
            approve = True
            if interest_rate < 12:
                corrected_interest_rate = 12
        elif 10 < credit_score <= 30:
            approve = True
            if interest_rate < 16:
                corrected_interest_rate = 16
        else:
            approve = False

        monthly_rate = corrected_interest_rate / 100 / 12
        if monthly_rate == 0:
            emi = loan_amount / tenure
        else:
            emi = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -tenure)

        
        if (customer.current_debt + emi) > 0.5 * customer.monthly_income:
            approve = False

      
        response = {
            "customer_id": customer.customer_id,
            "approval": approve,
            "interest_rate": interest_rate,
            "corrected_interest_rate": round(corrected_interest_rate, 2),
            "tenure": tenure,
            "monthly_installment": round(emi, 2)
        }

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
