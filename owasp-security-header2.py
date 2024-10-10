import requests

# Replace with your Envoy proxy URL
envoy_url = 'https://assistant.disearch.ai'

# Sending a GET request to the Envoy proxy
try:
    response = requests.get(envoy_url)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        # Check for the presence and values of security headers
        security_headers = {
            "X-XSS-Protection": "1; mode=block",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "no-referrer",
            "X-Download-Options": "noopen",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
        }

        for header, expected_value in security_headers.items():
            if header in response.headers:
                actual_value = response.headers[header]
                print(f"{header} is present with value: {actual_value}")
                if actual_value == expected_value:
                    print(f"✔️ {header} has the expected value.")
                else:
                    print(f"❌ {header} does NOT have the expected value. Expected: '{expected_value}', Found: '{actual_value}'")
            else:
                print(f"❌ {header} is missing.")

    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
