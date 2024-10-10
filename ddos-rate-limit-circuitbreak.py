import requests
import concurrent.futures
import time
from collections import Counter

# URL to send requests to
url = "https://assistant.disearch.ai"

# Function to send a single request
def send_request(session):
    try:
        response = session.get(url)
        return response.status_code
    except Exception as e:
        return str(e)

# Main function to send requests in parallel
def main():
    start_time = time.time()  # Start time

    # Using a session for efficient connections
    with requests.Session() as session:
        # Using ThreadPoolExecutor to send requests concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:  # Adjust number of workers
            # Create a list of futures for 5000 requests (to stress test the circuit breaker)
            futures = [executor.submit(send_request, session) for _ in range(5000)]  # Increase request count
            
            # Retrieve the results as they complete
            results = []
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

    end_time = time.time()  # End time
    duration = end_time - start_time  # Duration of the requests

    # Count the frequency of each status code
    status_counts = Counter(results)

    # Display results
    print(f"Total requests sent: {len(results)}")
    print(f"Total time taken: {duration:.2f} seconds")
    print("\nResponse status codes:")
    for status_code, count in status_counts.items():
        print(f"  Status Code: {status_code} - Count: {count}")

if __name__ == "__main__":
    main()
