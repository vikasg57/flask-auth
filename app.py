from flask import Flask, render_template, session, redirect, url_for, request

from api_handler import ApiHandler
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            response = SupabaseHandler().do_login(email, password)

            if response.get('session') and response.get('session').get('access_token'):
                access_token = response['session']['access_token']
                session['access_token'] = access_token
                return redirect(url_for('dashboard'))
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

        try:
            response = SupabaseHandler().do_signup(email, password)

            print(response)

            if response.get('session') and response.get('session').get('access_token'):
                session['access_token'] = response['session']['access_token']  # Store the token in session
                success_message = "Signup successful! Redirecting to the dashboard..."
                return redirect(url_for('dashboard'))
            else:
                error_message = "Something went wrong. Please try again later."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    return render_template('signup.html', error=error_message, success=success_message)


@app.route("/logout")
def logout():
    # Remove 'access_token' from the session
    session.pop("access_token", None)
    # Redirect to login page
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
