from dotenv import load_dotenv
from mailjet_rest import Client
import os
import random
import requests

load_dotenv()


test_mode = os.getenv("DEBUG", "false").lower() == "true"

# Email
sender_email = os.getenv("SENDER_EMAIL")
sender_name = os.getenv("SENDER_NAME", "Money Pit")
mj_api_key_public = os.getenv("MJ_API_KEY_PUBLIC")
mj_api_key_private = os.getenv("MJ_API_KEY_PRIVATE")

if not sender_email:
    raise ValueError("SENDER_EMAIL environment variable is not set.")
if not mj_api_key_public:
    raise ValueError("MJ_API_KEY_PUBLIC environment variable is not set.")
if not mj_api_key_private:
    raise ValueError("MJ_API_KEY_PRIVATE environment variable is not set.")

mailjet = Client(auth=(mj_api_key_public, mj_api_key_private), version='v3.1')



def send_verification_email(recipient_email, recipient_name, ip,):
    # Get the user's location based on IP address
    if test_mode:
        ip = "TEST_IP"
        city = "Test City"
        country = "Test Country"
    else:
        try:
            location_response = requests.get(f"https://ip.hackclub.com/ip/{ip}").json()
            city = location_response.get('city_name')
            country = location_response.get('country_name')
        except Exception as e:
            raise Exception(f"Failed to get location for IP {ip}: {e}")
    
    verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(f"Sending verification email to {recipient_email} with code: {verification_code}")

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
                    We have received a request to reset your password from the ip address {ip} at {city} in the country {country}. Please use the code below to reset your password:
                </h3>
                <div style="padding: 2px; padding-left: 12px; padding-right: 4px; background-color: #374151; border-radius: 8px; color: #cbd5e1;">
                    <p><strong>{verification_code}</strong></p>
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
                                    "Name": f"{sender_name}"
                            },
                            "To": [
                                    {
                                            "Email": f"{recipient_email}",
                                            "Name": f"{recipient_name}"
                                    }
                            ],
                            "Subject": "Password Reset",
                            "TextPart": "Here is your password code.",
                            "HTMLPart": f"{email}",
                    }
            ]
    }
    try:
        result = mailjet.send.create(data=data)
        return result, verification_code
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise Exception(f"Failed to send email: {e}")
