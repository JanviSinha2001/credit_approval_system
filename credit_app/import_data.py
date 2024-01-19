import pandas as pd
from django.core.management.base import BaseCommand
from credit_app.models import Customer, Loan

class Command(BaseCommand):
    help = 'Imports customer and loan data from Excel files'

    def handle(self, *args, **options):
        self.import_customer_data()
        self.import_loan_data()

    def import_customer_data(self):
        df = pd.read_excel('customer_data.xlsx')
        for _, row in df.iterrows():
            customer, created = Customer.objects.get_or_create(
                customer_id=row['customer_id'],
                defaults={
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'phone_number': row['phone_number'],
                    'monthly_salary': row['monthly_salary'],
                    'approved_limit': row['approved_limit'],
                    'current_debt': row['current_debt'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully imported customer: {customer}'))

    def import_loan_data(self):
        df = pd.read_excel('loan_data.xlsx')
        for _, row in df.iterrows():
            customer = Customer.objects.get(customer_id=row['customer_id'])
            loan, created = Loan.objects.get_or_create(
                customer=customer,
                loan_id=row['loan_id'],
                defaults={
                    'loan_amount': row['loan_amount'],
                    'tenure': row['tenure'],
                    'interest_rate': row['interest_rate'],
                    'monthly_repayment': row['monthly_repayment'],
                    'emis_paid_on_time': row['emis_paid_on_time'],
                    'start_date': row['start_date'],
                    'end_date': row['end_date'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully imported loan: {loan}'))