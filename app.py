from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for, request
)

from medusa_handler import MedusaHandler
from supabase_handler import SupabaseHandler

app = Flask(__name__)

app.secret_key = "flask_secret"  # Replace with a secure key


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/dashboard")
def dashboard():
    if "access_token" in session:
        return render_template("dashboard.html")  # Render the dashboard template
    return redirect(url_for("login"))


@app.route("/products")
def products():
    if "medusa_access_token" in session:
        product_response = MedusaHandler().get_products(session['medusa_access_token'])
        if product_response and product_response.get('products'):
            products = product_response.get('products')
            print(products)
            return render_template("products.html", products=products)  # Render the dashboard template
        return render_template("dashboard.html")  # Render the dashboard template
    return redirect(url_for("login"))


def set_session_data(medusa_response, response):
    medusa_access_token = medusa_response['token']
    access_token = response['session']['access_token']
    session['supabase_access_token'] = access_token
    session['medusa_access_token'] = medusa_access_token


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            response = SupabaseHandler().do_login(email, password)

            if response.get('session') and response.get('session').get('access_token'):
                medusa_response = MedusaHandler().do_login(email, password)
                if medusa_response.get('token'):
                    set_session_data(medusa_response, response)
                return redirect(url_for('products'))
            else:
                error_message = "Invalid email or password. Please try again."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    return render_template('login.html', title='Login', name='User', error=error_message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message = None
    success_message = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        try:
            response = SupabaseHandler().do_signup(email, password)
            if response.get('session') and response.get('session').get('access_token'):
                medusa_access_token = None
                try:
                    medusa_jwt_response = MedusaHandler().get_registration_token(email, password)
                    if medusa_jwt_response and medusa_jwt_response.get('token'):
                        medusa_access_token = medusa_jwt_response['token']
                    MedusaHandler().create_customer(medusa_access_token, first_name, last_name, email)
                    medusa_response = MedusaHandler().do_login(email, password)
                    if medusa_response.get('token'):
                        set_session_data(medusa_response, response)
                except Exception as e:
                    print(f"Error creating customer: {str(e)}")
                success_message = "Signup successful! Redirecting to the dashboard..."
                return redirect(url_for('products'))
            else:
                error_message = "Something went wrong. Please try again later."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    return render_template('signup.html', error=error_message, success=success_message)


@app.route("/logout")
def logout():
    # Remove 'access_token' from the session
    session.pop("supabase_access_token", None)
    session.pop("medusa_access_token", None)
    # Redirect to login page
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
