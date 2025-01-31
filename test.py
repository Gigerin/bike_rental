import requests

API_BASE_URL = "http://127.0.0.1:8000/api"
EMAIL = "codenamedelta228@gmail.com"
PASSWORD = "80808080"


def get_token(email, password):
    url = f"{API_BASE_URL}/token/"
    response = requests.post(url, data={"email": email, "password": password})
    response.raise_for_status()
    return response.json()["access"]


def get_available_bikes(token):
    url = f"{API_BASE_URL}/bikes/available/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def rent_bike(token, bike_id, price):
    url = f"{API_BASE_URL}/bikes/rent/{bike_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"price": price}
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


def return_bike(token, bike_id):
    url = f"{API_BASE_URL}/bikes/return/{bike_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_rent_history(token):
    url = f"{API_BASE_URL}/bikes/get_rent_history"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
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
        bike_id = bike_to_rent["id"]
        rented_until = "2024-08-01T20:57:12.114502"
        rented_from = "2024-08-01T19:57:12.114502"
        price = 1000
        rent_response = rent_bike(token, bike_id, 1000)
        print(f"Bike rented successfully: {rent_response}")
        return_response = return_bike(token, bike_id)
        print(f"Bike returned successfully: {return_response}")
        history_response = get_rent_history(token)
        print(f"Last Rent: {history_response[-1]}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
