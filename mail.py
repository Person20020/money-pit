from dotenv import load_dotenv
from mailjet_rest import Client
import os
import random


load_dotenv("website/.env")

api_key_public = os.getenv("MJ_API_KEY_PUBLIC")
api_key_private = os.getenv("MJ_API_KEY_PRIVATE")
sender_email = os.getenv("SENDER_EMAIL")

# Temp email for testing
recipient_email = "5o9r7x@hack.af"

mailjet = Client(auth=(api_key_public, api_key_private), version='v3.1')


if not api_key_public or not api_key_private or not sender_email:
    raise ValueError("Environment variables MJ_API_KEY_PUBLIC, MJ_API_KEY_PRIVATE, and SENDER_EMAIL must be set.")


def send_email(recipient_email):
    code = f"{random.randint(0, 999999):06}"
    email = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <div class="container mx-auto m-5 mt-10 bg-slate-800">
                <h1>
                    Reset Password
                </h1>
                <h3>
                    We have received a request to reset your password. Please use the code below to reset your password:
                </h3>
                <div style="padding: 2px; padding-left: 12px; padding-right: 4px; background-color: #374151; border-radius: 8px; color: #cbd5e1;">
                    <p><strong>{code}</strong></p>
                </div>
                <p>
                    If you did not request this, you can safely ignore this email.
                </p>
            </div>
        </body>
        </html>
        """
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": f"{sender_email}",
                                    "Name": "Money Pit"
                            },
                            "To": [
                                    {
                                            "Email": f"{recipient_email}",
                                            "Name": "You"
                                    }
                            ],
                            "Subject": "Password Reset",
                            "TextPart": "Here is your password code.",
                            "HTMLPart": f"{email}",
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

send_email(recipient_email)