from flask import Flask, render_template, request, redirect, url_for, flash ,session,Response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os, random, time
from itsdangerous import TimedSerializer
from dotenv import load_dotenv
import secrets

app = Flask(__name__)
load_dotenv()
app.secret_key = secrets.token_hex(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
owner_email=os.getenv('EMAIL_ADDRESS')
mail = Mail(app)
db = SQLAlchemy(app)
otp_serializer = TimedSerializer(app.secret_key)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200),nullable=False)
    message= db.Column(db.String(500), nullable=False)



    def __repr__(self):
        return f'<User {self.email}>'

with app.app_context():
    db.create_all()
def should_hide_about():
    return True
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/resume')
def resume():
    return render_template('resume.html')
@app.route('/project')
def project():
    return render_template('project.html')
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method =='POST':
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']

        if not email:
            flash('email cant empty')
            return render_template('contact.html')
        else:
            session['email'] = email
            session['name'] =name
            session['subject']=subject
            session['message']=message
            otp = random.randint(100000, 999999)
            otp_token = otp_serializer.dumps({'otp': otp, 'timestamp': time.time()})
            send_otp_email(email, otp)
            session['otp_token'] = otp_token
            return redirect(url_for('otp'))
    return render_template('contact.html')
def send_otp_email(email,otp):
    try:
        msg = Message(f"Your Verification Code", recipients=[email])
        msg.body = f"Your OTP code is {otp}. This OTP will expire in 10 minutes."
        mail.send(msg)
    except Exception as e:
        flash("An error occurred while sending the OTP email.")
        return redirect(url_for('contact'))

@app.route('/otp',methods=['GET','POST'])
def otp():
    if request.method == 'POST':
        user_otp=request.form['otp']
        try:
            # Check if OTP session exists
            if 'otp_token' not in session:
                flash('OTP session expired. Please try again.', 'danger')
                return redirect(url_for('login'))

            #
            otp_data = otp_serializer.loads(session['otp_token'])
            original_otp = otp_data['otp']
            timestamp = otp_data['timestamp']

            if time.time() - timestamp > 600:  # 10 minutes
                flash('OTP has expired. Please try again.', 'danger')
                return redirect(url_for('login'))

            if int(user_otp) == original_otp:
                email = session.get('email')
                name=session.get('name')
                subject=session.get('subject')
                message=session.get('message')
                if email and name and subject and message:
                    new_user = User(name=name,email=email,subject=subject,message=message)
                    db.session.add(new_user)
                    db.session.commit()
                    session.pop('otp_token', None)
                    flash('Verification successful. You are now registered!', 'success')
                    # Clear the OTP token from session
                    msg = Message('New Enquiry Form Submission',recipients=[owner_email])
                    msg.body = f"Enquiry from: {name}\n\nEmail: {email}\n\nSubject: {subject}\n\nMessage:  {message}"
                    mail.send(msg)
                    return render_template('thankyou.html')
                else:
                    flash('Error: Missing user data. Please try again.', 'danger')
                    return redirect(url_for('contact'))

            else:
                flash('Invalid OTP. please enter valid otp.', 'danger')
                return redirect(url_for('otp'))  # Show error message if OTP is wrong
        except Exception as e:
            flash('OTP verification failed. Please try again later.', 'danger')
            return redirect(url_for('contact'))
    return render_template('otp.html')


@app.route('/download/csv')
def download_csv():
    users = User.query.all()
    def generate():
        yield 'id,name,email\n'  # header row
        for user in users:
            yield f'{user.id},{user.name},{user.email},{user.subject},{user.message}\n'

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=users.csv"})


if __name__ == '__main__':
    app.run(debug=True)