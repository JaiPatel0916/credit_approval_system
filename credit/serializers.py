# from rest_framework import serializers
# from .models import Customer, Loan

# # ---------- Customer Serializer ----------
# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'


# # ---------- Loan Serializer ----------
# class LoanSerializer(serializers.ModelSerializer):
#     customer = CustomerSerializer(read_only=True)

#     class Meta:
#         model = Loan
#         fields = '__all__'



from rest_framework import serializers
from .models import Customer, Loan


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



class LoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

   
    approval = serializers.SerializerMethodField()
    corrected_interest_rate = serializers.SerializerMethodField()
    monthly_installment = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = '__all__' 
        read_only_fields = ['approval', 'corrected_interest_rate', 'monthly_installment']

   
    def get_approval(self, obj):
        return getattr(obj, 'approval', None)

    def get_corrected_interest_rate(self, obj):
        return getattr(obj, 'corrected_interest_rate', None)

    def get_monthly_installment(self, obj):
        return getattr(obj, 'monthly_installment', None)
