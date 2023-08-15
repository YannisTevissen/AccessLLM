import requests, os


def find_place_from_name(name: str):
    url = 'https://places.googleapis.com/v1/places:searchText'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': os.environ['GOOGLE_CLOUD_API_KEY'],  # Replace with your actual API key
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.websiteUri'
    }

    data = {
        "textQuery": name
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        # Process the result as needed
        print(result)
        return result
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    find_place_from_name("500 diables")