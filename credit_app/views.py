from django.shortcuts import render
from .models import Customer, Loan, Emi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer, LoanSerializer

# Create your views here.
@api_view(['POST'])
def create_loan(request):
    if request.method == 'POST':
        data = request.data

        customer_id = data.get('customer_id')
        loan_amount = data.get('loan_amount')
        interest_rate = data.get('interest_rate')
        tenure = data.get('tenure')

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform eligibility check and loan processing logic here

        loan_approved = True  # Update with your logic
        monthly_installment = 1500.00  # Update with your logic

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            tenure=tenure,
            loan_approved=loan_approved,
            monthly_installment=monthly_installment
        )

        return Response({
            'loan_id': loan.id,
            'customer_id': customer.id,
            'loan_approved': loan.loan_approved,
            'message': 'Loan processed successfully' if loan.loan_approved else 'Loan not approved',
            'monthly_installment': loan.monthly_installment
        })
@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return Response({'message': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LoanSerializer(loan)
    return Response(serializer.data)

@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer=customer)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

def credit_app_view(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'credit_app/credit_app.html', context)

def customer_view(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    loans = Loan.objects.filter(customer=customer)
    emis = Emi.objects.filter(loan__in=loans)
    context = {'customer': customer, 'loans': loans, 'emis': emis}
    return render(request, 'credit_app/customer.html', context)


def emi_view(request, emi_id):
    emi = Emi.objects.get(pk=emi_id)
    context = {'emi': emi}
    return render(request, 'credit_app/emi.html', context)

@api_view(['POST'])
def register_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)