import requests

API_BASE_URL = 'http://127.0.0.1:8000/api'
EMAIL = 'codenamedelta228@gmail.com'
PASSWORD = 'gigeriniscool123'

def get_token(email, password):
    url = f'{API_BASE_URL}/token/'
    response = requests.post(url, data={'email': email, 'password': password})
    print(response.json())
    response.raise_for_status()
    return response.json()['access']

def get_available_bikes(token):
    url = f'{API_BASE_URL}/bikes/available/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def rent_bike(token, bike_id, rented_until):
    url = f'{API_BASE_URL}/bikes/rent/{bike_id}/'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'rented_until': rented_until}
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    try:
        token = get_token(EMAIL, PASSWORD)
        available_bikes = get_available_bikes(token)
        
        if not available_bikes:
            print("No bikes available for rent.")
            return

        # Предположим, мы арендуем первый доступный велосипед
        bike_to_rent = available_bikes[0]
        bike_id = bike_to_rent['id']
        rented_until = '2024-12-31T23:59:59Z'  # Установите нужную дату и время

        rent_response = rent_bike(token, bike_id, rented_until)
        print(f"Bike rented successfully: {rent_response}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

