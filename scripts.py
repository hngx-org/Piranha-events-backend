import requests
import time

# Ngrok tunnel URL
ngrok_url = 'https://d039-197-232-79-158.ngrok-free.app'

def keep_ngrok_alive():
    try:
        # Send a GET request to your Ngrok tunnel URL
        response = requests.get('https://d039-197-232-79-158.ngrok-free.app')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(f'Ping successful at {time.ctime()}')
        else:
            print(f'Error: Status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    # Run the script indefinitely, pinging Ngrok every 5 minutes
    while True:
        keep_ngrok_alive()
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)