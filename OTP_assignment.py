import smtplib
import random
import re
from twilio.rest import Client

class OTPService:
    """
    Class docstring: OTPService class handles the generation and sending of OTPs.
    """

    def __init__(self, account_sid, auth_token, twilio_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_number = twilio_number

    def generate_otp(self):
        """
        Generates a 6-digit OTP.
        """
        digits = "0123456789"
        return ''.join(random.choice(digits) for _ in range(6))

    def send_email(self, email, otp):
        """
        Sends the OTP via email.
        """
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('naiksuyogsudhir@gmail.com', 'kajzazcwvvnbhgxg')
        message = f'Your 6 digit OTP is {otp}'
        server.sendmail('naiksuyogsudhir@gmail.com', email, message)
        server.quit()

    def send_otp_over_mobile(self, mobile_no, otp):
        """
        Sends the OTP via Twilio SMS.
        """
        client = Client(self.account_sid, self.auth_token)
        message_body = f'Your 6 digit OTP is {otp}'
        message = client.messages.create(
            body=message_body,
            from_=self.twilio_number,
            to=f'+91{mobile_no}',
        )
        print(message.body)

    def send_otp_to_mobile_user(self, mobile_user):
        """
        Sends OTP to a MobileUser instance.
        """
        if mobile_user.validate_mobile_no():
            self.send_otp_over_mobile(mobile_user.mobile_no, self.generate_otp())
        else:
            print("Invalid Mobile number")

    def send_otp_to_email_user(self, email_user):
        """
        Sends OTP to an EmailUser instance.
        """
        if email_user.validate_email():
            self.send_email(email_user.email, self.generate_otp())
        else:
            print("Invalid Email")


class MobileUser:
    def __init__(self, mobile_no):
        self.mobile_no = mobile_no

    def validate_mobile_no(self):
        """
        Validates a mobile number.
        """
        return len(self.mobile_no) == 10 and self.mobile_no.isdigit()


class EmailUser:
    def __init__(self, email):
        self.email = email

    def validate_email(self):
        """
        Validates an email address.
        """
        validation_condition = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.search(validation_condition, self.email))


if __name__ == "__main__":
    ACCOUNT_SID = "AC74d3234c1b27da3f53a19340e214c05f"
    AUTH_TOKEN = "098668260492fa52f2f8bce4966a7322"
    TWILIO_NUMBER = '+14705162791'

    OTP_SERVICE = OTPService(ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER)

    MOBILE_USER = MobileUser(input("Enter the Mobile number:"))
    EMAIL_USER = EmailUser(input("Enter the Email:"))

    OTP_SERVICE.send_otp_to_mobile_user(MOBILE_USER)
    OTP_SERVICE.send_otp_to_email_user(EMAIL_USER)
