"""
Module: otp_assignment
Description: This module implements classes for OTP generation and communication.
"""

import smtplib
import random
import re
from twilio.rest import Client

class CommunicationService:
    """
    Abstract base class for communication services.
    """

    @staticmethod
    def generate_otp(length=6):
        """
        Generates a random OTP of the specified length.

        Args:
            length (int): Length of the OTP.

        Returns:
            str: The generated OTP.
        """
        digits = "0123456789"
        return ''.join(random.choice(digits) for _ in range(length))

    def send_otp(self, identifier, otp):
        """
        Abstract method for sending OTP.

        Args:
            identifier (str): Identifier of the user (e.g., email or phone number).
            otp (str): The OTP to be sent.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class OTPService(CommunicationService):
    """
    Service class for OTP generation and communication using Twilio and email.
    """

    def __init__(self, account_sid, auth_token, twilio_number):
        """
        Initializes an instance of OTPService.

        Args:
            account_sid (str): Twilio account SID.
            auth_token (str): Twilio authentication token.
            twilio_number (str): Twilio phone number.
        """
        super().__init__()
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_number = twilio_number

    def send_email(self, email, otp):
        """
        Sends the OTP via email.

        Args:
            email (str): Email address of the user.
            otp (str): The OTP to be sent.
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

        Args:
            mobile_no (str): Mobile number of the user.
            otp (str): The OTP to be sent.
        """
        client = Client(self.account_sid, self.auth_token)
        message_body = f'Your 6 digit OTP is {otp}'
        message = client.messages.create(
            body=message_body,
            from_=self.twilio_number,
            to=f'+91{mobile_no}',
        )
        print(message.body)

    def send_otp(self, identifier, otp):
        """
        Sends OTP using the appropriate method based on the identifier.

        Args:
            identifier (str): Identifier of the user (e.g., email or phone number).
            otp (str): The OTP to be sent.
        """
        if '@' in identifier:
            self.send_email(identifier, otp)
        else:
            self.send_otp_over_mobile(identifier, otp)

    def send_otp_to_mobile_user(self, mobile_user):
        """
        Sends OTP to a MobileUser instance.

        Args:
            mobile_user (MobileUser): Instance of MobileUser.
        """
        if mobile_user.validate():
            self.send_otp(mobile_user.get_identifier(), self.generate_otp())
        else:
            print("Invalid Mobile number")

    def send_otp_to_email_user(self, email_user):
        """
        Sends OTP to an EmailUser instance.

        Args:
            email_user (EmailUser): Instance of EmailUser.
        """
        if email_user.validate():
            self.send_otp(email_user.get_identifier(), self.generate_otp())
        else:
            print("Invalid Email")

class User:
    """
    Base class for representing a user.
    """

    def __init__(self, identifier):
        """
        Initializes a User instance.

        Args:
            identifier (str): Identifier of the user.
        """
        self.identifier = identifier

    def get_identifier(self):
        """
        Returns the identifier of the user.

        Returns:
            str: The identifier.
        """
        return self.identifier

    def public_method(self):
        """
        Example of a public method.
        """
        pass

class MobileUser(User):
    """
    Represents a user with a mobile number.
    """

    def validate(self):
        """
        Validates the mobile number.

        Returns:
            bool: True if the mobile number is valid, False otherwise.
        """
        return len(self.identifier) == 10 and self.identifier.isdigit()

class EmailUser(User):
    """
    Represents a user with an email address.
    """

    def validate(self):
        """
        Validates the email address.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        validation_condition = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.search(validation_condition, self.identifier))

if __name__ == "__main__":
    ACCOUNT_SID = "AC74d3234c1b27da3f53a19340e214c05f"
    AUTH_TOKEN = "33b78e74d180fd56a28dc7c4c6ab113b"
    TWILIO_NUMBER = '+14705162791'

    OTP_SERVICE = OTPService(ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER)

    MOBILE_USER = MobileUser(input("Enter the Mobile number:"))
    EMAIL_USER = EmailUser(input("Enter the Email:"))

    OTP_SERVICE.send_otp_to_mobile_user(MOBILE_USER)
    OTP_SERVICE.send_otp_to_email_user(EMAIL_USER)
