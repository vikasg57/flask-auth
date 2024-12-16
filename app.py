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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response = SupabaseHandler().do_login(email, password)

        if response.get('session') and response.get('session').get('access_token'):
            access_token = response.get('session') and response.get('session').get('access_token')
            session['access_token'] = access_token
            return redirect(url_for('dashboard'))
    return render_template('login.html', title='Home', name='User')


@app.route("/logout")
def logout():
    # Remove 'access_token' from the session
    session.pop("access_token", None)
    # Redirect to login page
    return redirect(url_for("login"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response = SupabaseHandler().do_signup(email, password)

        print(response)

        if response.status_code == 200:
            data = response.json()
            session['access_token'] = data['access_token']  # Store the token in session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
