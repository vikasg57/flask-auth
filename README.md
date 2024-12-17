# Flask Application for User Authentication

This README provides detailed instructions for setting up and running your Flask application for user authentication integrated with Supabase and Medusa.

## Prerequisites

Ensure you have the following installed on your system:

- **Python** (version 3.8 or higher): [Download and install Python](https://www.python.org/)
- **Pip** (Python package manager): Included with Python installations
- **Virtualenv** (optional but recommended): Install using `pip install virtualenv`

## Steps to Get Started

### Access the Deployed Application

If your application is deployed, you can access it at the following link:

[Deployed Flask App](https://flask-auth-x8l1.onrender.com/)

**Note**: Free instance will spin down with inactivity, which can delay requests by 50 seconds or more when accessing the app for the first time.


### 1. Clone the Repository

```bash
git clone https://github.com/vikasg57/flask-auth.git
cd flask-auth-app
```

### 2. Set Up a Virtual Environment (Optional)

It is recommended to use a virtual environment to manage dependencies:

```bash
virtualenv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and configure the following environment variables:

```env
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_API_KEY=your-supabase-api-key
```

Replace the placeholders (`your-supabase-url`, `your-supabase-api-key`, etc.) with your actual configuration values.


### 5. Run the Flask Application

Start the development server:

```bash
flask run
```

The application should now be running at `http://127.0.0.1:5000/`.

## Features

### 1. User Authentication
- **Signup**: Registers users in Supabase and Medusa.
- **Login**: Authenticates users and creates sessions using JWT.

### 2. Protected Routes
Routes are protected by validating JWT tokens stored in the session.

### 3. Medusa Integration
Newly registered users are automatically created as customers in Medusa.

## Example Usage

### Signup via Curl

```bash
curl -X POST 'http://127.0.0.1:5000/signup' \
-H 'Content-Type: application/json' \
--data-raw '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "yourpassword"
}'
```

### Login via Curl

```bash
curl -X POST 'http://127.0.0.1:5000/login' \
-H 'Content-Type: application/json' \
--data-raw '{
    "email": "johndoe@example.com",
    "password": "yourpassword"
}'
```

### Protected Route Example

```bash
curl -X GET 'http://127.0.0.1:5000/protected' \
-H 'Authorization: Bearer your-jwt-token'
```

## Troubleshooting

### Common Issues

1. **401 Unauthorized**:
   - Ensure the `Authorization` header contains a valid JWT token.
   - Verify the Supabase and Medusa API keys are correctly set in the `.env` file.

2. **Environment Variable Errors**:
   - Confirm the `.env` file is created and loaded properly.

3. **Dependency Errors**:
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed.

### Logs and Debugging

Run the application in debug mode:

```bash
flask run --debug
```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Medusa Documentation](https://docs.medusajs.com/)

---

Happy coding with Flask! 🚀

