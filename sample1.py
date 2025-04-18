import time
import os
import subprocess
import pickle
import random
from threading import Thread

# Global variable (potential issue) 3
DATA_CACHE = {}

def fetch_data_from_api(url):
    """Simulates fetching data from an API (very inefficiently)."""
    time.sleep(random.uniform(2, 5))  # Simulate network latency
    if random.random() < 0.2:
        return None  # Simulate API errors
    return {"data": f"Result from {url} at {time.time()}"}

def process_data(raw_data):
    """Performs some processing on the fetched data (unnecessarily complex)."""
    if raw_data and "data" in raw_data:
        temp_list = list(raw_data["data"])
        random.shuffle(temp_list)
        processed_string = "".join(temp_list).upper()
        return processed_string
    return None

def cache_data(key, data):
    """Caches data in a global variable (not thread-safe)."""
    global DATA_CACHE
    DATA_CACHE[key] = data

def get_cached_data(key):
    """Retrieves data from the global cache."""
    global DATA_CACHE
    return DATA_CACHE.get(key)

def execute_system_command(command):
    """Executes a system command (potential security risk)."""
    os.system(command) # Insecure! Avoid using os.system

def serialize_data(data, filename="data.pkl"):
    """Serializes data to a file (potential security risk if data is untrusted)."""
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def deserialize_data(filename="data.pkl"):
    """Deserializes data from a file (major security risk if file is malicious)."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def worker_thread(url):
    """Worker function for a thread."""
    cached_result = get_cached_data(url)
    if cached_result:
        print(f"Thread for {url}: Retrieved from cache: {cached_result[:20]}...")
        return

    print(f"Thread for {url}: Fetching data from {url}...")
    raw_data = fetch_data_from_api(url)
    if raw_data:
        processed_data = process_data(raw_data)
        if processed_data:
            cache_data(url, processed_data)
            print(f"Thread for {url}: Processed data: {processed_data[:20]}...")
        else:
            print(f"Thread for {url}: Failed to process data from {url}.")
    else:
        print(f"Thread for {url}: Failed to fetch data from {url}.")

def main():
    """Main function."""
    api_endpoints = ["http://api.example.com/data1", "http://api.example.com/data2", "http://api.example.com/data3"]
    threads = []
    for url in api_endpoints:
        thread = Thread(target=worker_thread, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Insecure system command execution
    user_input = input("Enter a command to execute (be careful!): ")
    execute_system_command(user_input)

    # Serialization and deserialization (potential vulnerabilities)
    sample_data = {"important": "secret"}
    serialize_data(sample_data)
    loaded_data = deserialize_data()
    if loaded_data:
        print(f"Loaded data: {loaded_data}")

if __name__ == "__main__":
    main()
