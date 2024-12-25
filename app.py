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

supabase_client = SupabaseHandler().get_supabase_client()


def get_first_and_last_name(full_name):
    """Get First and Last name."""
    first, *last = full_name.split()
    return first, " ".join(last)


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
            medusa_products = product_response.get('products')
            return render_template("products.html", products=medusa_products)  # Render the dashboard template
        return render_template("dashboard.html")  # Render the dashboard template
    return redirect(url_for("login"))


def set_session_data(medusa_access_token, access_token):
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
                default_password = MedusaHandler().generate_customer_password(email)
                print(default_password)
                medusa_response = MedusaHandler().do_login(email, default_password)
                if medusa_response.get('token'):
                    medusa_access_token = medusa_response['token']
                    access_token = response['session']['access_token']
                    set_session_data(medusa_access_token, access_token)
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
                try:
                    default_password = MedusaHandler().generate_customer_password(email)
                    MedusaHandler().create_customer(first_name, last_name, email, default_password)
                    medusa_response = MedusaHandler().do_login(email, default_password)
                    if medusa_response.get('token'):
                        medusa_access_token = medusa_response['token']
                        access_token = response['session']['access_token']
                        set_session_data(medusa_access_token, access_token)
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


@app.route("/sso/login", methods=['GET'])
def ssologin():
    # Get the Google OAuth URL from Supabase
    provider = 'google'
    redirect_url = f"{request.url_root}sso/callback"
    # Generate the OAuth URL
    print(redirect_url)
    auth_url = supabase_client.auth.sign_in_with_oauth(
        {
            'provider': provider,
            'options':
                {
                    'redirect_to': redirect_url
                }
        }
    )
    redirect_url = auth_url.url + '&prompt=select_account'  # Forces account selection
    return redirect(redirect_url)


@app.route('/sso/callback', methods=['GET', 'POST'])
def callback():
    # Handle the callback from Google/Supabase
    code = request.args.get('code')

    if not code:
        return 'No code provided', 400
    try:
        user_data = supabase_client.auth.exchange_code_for_session({
            'auth_code': code
        })
        full_name = user_data.user.user_metadata.get('full_name') or ''
        access_token = user_data.session.access_token
        email = user_data.user.email
        default_password = MedusaHandler().generate_customer_password(email)
        print(default_password)
        first_name, last_name = get_first_and_last_name(full_name)
        medusa_response = MedusaHandler().do_login(email, default_password)
        if medusa_response.get('type') == 'unauthorized':
            MedusaHandler().create_customer(
                first_name, last_name, email, default_password)
            medusa_response = MedusaHandler().do_login(email, default_password)
        medusa_access_token = medusa_response['token']
        set_session_data(medusa_access_token, access_token)
        return redirect('/products')

    except Exception as e:
        return f'Authentication error: {str(e)}', 400


if __name__ == '__main__':
    app.run(debug=True)
