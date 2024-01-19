from django.apps import AppConfig


class CreditAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'credit_app'
from flask import Flask, request, jsonify
from models import Customer, calculate_approved_limit, calculate_credit_score

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_customer():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    monthly_income = data.get('monthly_income')
    phone_number = data.get('phone_number')

    approved_limit = calculate_approved_limit(monthly_income)

    customer = Customer(first_name=first_name, last_name=last_name, age=age,
                        monthly_income=monthly_income, approved_limit=approved_limit,
                        phone_number=phone_number)

    # Save the customer to the database or perform any necessary actions

    return jsonify({
        'customer_id': customer.customer_id,
        'name': customer.get_full_name(),
        'age': customer.age,
        'monthly_income': customer.monthly_income,
        'approved_limit': customer.approved_limit,
        'phone_number': customer.phone_number
    })

@app.route('/check-eligibility', methods=['POST'])
def check_eligibility():
    data = request.get_json()

    # Fetch credit score from loan_data.xlsx or database
    credit_score = calculate_credit_score(data)


    return jsonify({
        
    })

if __name__ == '__main__':
    app.run(debug=True)
