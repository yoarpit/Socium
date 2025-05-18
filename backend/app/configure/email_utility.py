import smtplib
from email.message import EmailMessage

EMAIL_SENDER = "anshjaiswal123450@gmail.com"
EMAIL_PASSWORD = "eaum xvyw zpqb ikxl"
def send_otp_email(to_email: str, otp_code: str):
    msg = EmailMessage()
    msg['Subject'] = "Your OTP Verification Code For Socium"
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg.set_content(f"Thanks To Sign UP In Socium✊\n Your OTP verification code is: {otp_code}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
