import requests
import time

class TempMail:
    def __init__(self):
        self.base_url = 'https://www.temp-mail.org/en/api/'

    def generate_email(self):
        try:
            response = requests.get(self.base_url + 'request')
            if response.status_code == 200:
                data = response.json()
                self.email = data['email']
                self.token = data['token']
                print(f"Generated email: {self.email}")
                print(f"Token: {self.token}")
            else:
                print(f"Failed to generate email. Status code: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred during email generation: {e}")

    def fetch_emails(self):
        try:
            if not hasattr(self, 'email'):
                raise Exception("No email generated")

            print("Waiting for emails...")
            time.sleep(10)  # Waiting for emails to arrive
            response = requests.get(self.base_url + f'mail/id/{self.token}/format/json/')
            if response.status_code == 200:
                emails = response.json()
                if emails:
                    if len(emails) > 0:
                        print(f"Received {len(emails)} email(s):")
                        for idx, email in enumerate(emails):
                            print(f"Email {idx + 1}:")
                            print(f"From: {email['mail_from']}")
                            print(f"Subject: {email['subject']}")
                            print(f"Body: {email['body']}")
                            print("-" * 20)
                    else:
                        print("No emails received yet")
                else:
                    print("No emails found in response")
            else:
                print(f"Failed to fetch emails. Status code: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred during email fetching: {e}")

# Пример использования:
temp_mail = TempMail()
temp_mail.generate_email()
temp_mail.fetch_emails()
