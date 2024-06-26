import requests
import time

class TempMail:
    def __init__(self):
        self.base_url = 'https://api.mail.tm'
        self.email = None
        self.password = None
        self.token = None
        self.inbox_id = None

    def generate_email(self):
        try:
            response = requests.post(f'{self.base_url}/accounts', json={})
            if response.status_code == 201:
                data = response.json()
                self.email = data['address']
                self.password = data['password']
                self.inbox_id = data['id']
                print(f"Generated email: {self.email}")
            else:
                print(f"Failed to generate email. Status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Exception occurred during email generation: {e}")

    def authenticate(self):
        try:
            response = requests.post(f'{self.base_url}/token', json={'address': self.email, 'password': self.password})
            if response.status_code == 200:
                self.token = response.json()['token']
                print(f"Authenticated. Token: {self.token}")
            else:
                print(f"Failed to authenticate. Status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Exception occurred during authentication: {e}")

    def fetch_emails(self):
        try:
            if not self.token:
                raise Exception("No token available. Authenticate first.")

            headers = {'Authorization': f'Bearer {self.token}'}
            print("Waiting for emails...")
            time.sleep(10)  # Waiting for emails to arrive
            response = requests.get(f'{self.base_url}/messages', headers=headers)
            if response.status_code == 200:
                emails = response.json()['hydra:member']
                if len(emails) > 0:
                    print(f"Received {len(emails)} email(s):")
                    for idx, email in enumerate(emails):
                        print(f"Email {idx + 1}:")
                        print(f"From: {email['from']['address']}")
                        print(f"Subject: {email['subject']}")
                        print(f"Body: {email['intro']}")
                        print("-" * 20)
                else:
                    print("No emails received yet")
            else:
                print(f"Failed to fetch emails. Status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Exception occurred during email fetching: {e}")

# Пример использования:
temp_mail = TempMail()
temp_mail.generate_email()
temp_mail.authenticate()
temp_mail.fetch_emails()
