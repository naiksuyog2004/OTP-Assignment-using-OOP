"""
Module docstring: This module defines the OTPService class for sending OTPs.
"""

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

    def validate_mobile_no(self, mobile_no):
        """
        Validates a mobile number.
        """
        return len(mobile_no) == 10 and mobile_no.isdigit()

    def validate_email(self, email):
        """
        Validates an email address.
        """
        validation_condition = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.search(validation_condition, email))

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

    def send_otp(self, mobile_no, email):
        """
        Sends OTP via the chosen method (SMS and/or email).
        """
        otp = self.generate_otp()

        if self.validate_mobile_no(mobile_no):
            self.send_otp_over_mobile(mobile_no, otp)
        else:
            print("Invalid Mobile number")

        if self.validate_email(email):
            self.send_email(email, otp)
        else:
            print("Invalid Email")


if __name__ == "__main__":
    ACCOUNT_SID = "AC74d3234c1b27da3f53a19340e214c05f"
    AUTH_TOKEN = "098668260492fa52f2f8bce4966a7322"
    TWILIO_NUMBER = '+14705162791'

    OTP_SERVICE = OTPService(ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER)

    MOBILE_NO = input("Enter the Mobile number:")
    EMAIL = input("Enter the Email:")

    OTP_SERVICE.send_otp(MOBILE_NO, EMAIL)
