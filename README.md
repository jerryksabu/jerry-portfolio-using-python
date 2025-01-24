
**Portfolio Enquiry Form with OTP Verification**


This project is a Flask web application that allows users to make enquiries about a portfolio. The system verifies the user's identity by sending a One-Time Password (OTP) to the provided email address. Only after successful OTP verification, users can access their portfolio details securely.

**Features**


Users can make enquiries about the portfolio by entering their email address. 

The system sends an OTP to the user’s email for verification.

OTP is verified before displaying portfolio details.

Secure implementation with email-based OTP verification.

**Prerequisites**

To run this project locally, you need the following installed:

Python 3.x or later

pip (Python package manager)

Flask web framework

A working email service to send OTPs (e.g., Gmail, SendGrid, etc.)

Additionally, you will need a Flask application and SMTP configuration to send OTPs to users' emails.


**Setup**

1. Clone the Repository

   Clone this repository to your local machine:

   git clone https://github.com/your-username/portfolio-enquiry-flask.git

   cd portfolio-enquiry-flask

2. Set Up Virtual Environment (optional but recommended)
   
     It is highly recommended to create a virtual environment to isolate your project’s dependencies.

     On Windows:

     python -m venv venv

     .\venv\Scripts\activate

     On macOS/Linux:

     python3 -m venv venv

     source venv/bin/activate

3. Install Dependencies
   
     Once your virtual environment is set up, install the required dependencies:

     pip install -r requirements.txt

T     he requirements.txt file includes the following dependencies:

      Flask: Web framework for the application.

      Flask-Mail: Used to send OTP emails.

      itsdangerous: For securely generating and verifying tokens (used in OTP verification).

      python-dotenv: To load environment variables securely (such as email credentials).

4. Configuration
   
     Create a .env file in the root directory to store your environment variables like email credentials and Flask configuration. Example .env:


# Flask settings

   FLASK_APP=app.py

   FLASK_ENV=development

   SECRET_KEY=your-secret-key


# Flask-Mail settings (email configuration)

    MAIL_SERVER=smtp.gmail.com

    MAIL_PORT=587

    MAIL_USE_TLS=True

    MAIL_USERNAME=your-email@gmail.com

    MAIL_PASSWORD=your-email-password

# Other settings (e.g., database, etc.)

    Make sure to replace your-email@gmail.com and your-email-password with actual credentials (use App Passwords if you're using Gmail with 2FA).

5. Database Setup (Optional)
   
   If your application requires a database to store portfolio inquiries or user data, set up SQLAlchemy as described in the app.py file. Alternatively, you can skip this step if the application doesn't need a database.

7. Run the Application
   
   Once everything is set up, run the Flask development server:

   flask run

   The application should now be running on http://127.0.0.1:5000/.

7. Access the Portfolio Enquiry Form
   
   Open your browser and go to http://127.0.0.1:5000/.

   Enter your email address in the enquiry form.

   The system will send an OTP to your email address.

   Enter the OTP on the verification page to access your portfolio details.

   Example Code Snippets

   Flask Application (app.py)

   Here's a simplified version of the application code (app.py) that handles OTP verification for a portfolio enquiry form:

   from flask import Flask, render_template, request, redirect, url_for, flash, session

   from flask_mail import Mail, Message

   import os

   from random import randint

   from dotenv import load_dotenv

   from itsdangerous import URLSafeTimedSerializer


# Load environment variables
   load_dotenv()

   app = Flask(__name__)
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

   app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')

   app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')

   app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')

   app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')

   app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
  

   mail = Mail(app)

   s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

   otp_code = None  # Global variable to store OTP

  @app.route('/', methods=['GET', 'POST'])

  def index():

     global otp_code
    
     if request.method == 'POST':
    
       user_email = request.form['email']
        
        
        # Generate OTP
        
        otp_code = randint(100000, 999999)
        
        
        # Send OTP via email
        
        msg = Message("Your OTP for Portfolio Inquiry", sender=os.getenv('MAIL_USERNAME'), recipients=[user_email])
        
        msg.body = f"Your OTP code is {otp_code}. It is valid for 10 minutes."
        
        mail.send(msg)
        
        flash("OTP has been sent to your email. Please check your inbox.")
        
        return redirect(url_for('verify'))
    
    return render_template('index.html')

@app.route('/verify', methods=['GET', 'POST'])

def verify():

    global otp_code
    
    if request.method == 'POST':
    
        entered_otp = request.form['otp']
        
        if str(otp_code) == entered_otp:
        
            return render_template('portfolio.html', portfolio_data="Your portfolio details here.")
            
        else:
        
            flash("Invalid OTP. Please try again.")
            
            return redirect(url_for('verify'))
    
    return render_template('verify.html')

if __name__ == '__main__':

    app.run(debug=True)
    
File Structure

Here’s an example file structure for the project:


portfolio-enquiry-flask/

├── app.py                   # Main Flask application

├── .env                     # Environment variables (email credentials, etc.)

├── requirements.txt         # Project dependencies

├── templates/               # HTML templates (OTP form, portfolio display)

│   ├── index.html           # Enquiry form

│   ├── verify.html          # OTP verification form

│   └── portfolio.html       # Portfolio details display

└── static/                  # Static files (CSS, JavaScript, images)


**Security Considerations**


Keep your .env file secure: Never share your .env file. It contains sensitive information like your email credentials. 


Email configuration: Ensure you are using secure email services and avoid exposing credentials directly in your code.


Use HTTPS: When deploying the app, ensure it uses HTTPS for security.
