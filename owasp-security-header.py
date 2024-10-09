import requests

# Replace with your Envoy proxy URL
envoy_url = 'https://envoy.disearch.ai'

# Sending a GET request to the Envoy proxy
try:
    response = requests.get(envoy_url)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        # Check for the presence of security headers
        security_headers = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-XSS-Protection",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "X-Download-Options",
            "Strict-Transport-Security",
            "X-Powered-By"
        ]

        for header in security_headers:
            if header in response.headers:
                print(f"{header} is present with value: {response.headers[header]}")
            else:
                print(f"{header} is missing.")

    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
