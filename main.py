import requests
import re
import time
import datetime
import threading

class Faucet:
    def __init__(self, data: dict) -> None:
        """
        Format for the data:
        [
            {
                "proxy": {
                    "http": "http://username:password@ip:port",
                    "https": "http://username:password@ip:port"
                },
                "address": "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE"
            },
            {
                "proxy": None,
                "address": "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE"
            }
        ]
        """
        self.data = data
    
    def send_request(self, data: dict):
        url: str = "https://faucet-api.testnet.tabichain.com/api/faucet"
        payload = {
            "address": data["address"]
        }
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            response = requests.post(url, json=payload, proxies=data["proxy"])
            if response.status_code == 200:
                print(f"{timestamp}: address -> {data['address']}: Request sent successfully")
                print(f"{timestamp}: address -> {data['address']}: Response: ", response.json())
            elif response.status_code == 429:
                print(f"{timestamp}: address -> {data['address']}: Too many requests. Please wait for 2 hours")
                time.sleep(7200) # If too many requests are sent, wait for 2 hours before sending the next request
            else:
                print("<------------------------->  ERROR  <------------------------->")
                print(f"{timestamp}: address -> {data['address']}: Request failed. Status code: ", response.status_code)
                print(f"{timestamp}: address -> {data['address']}: Response: ", response.json())
                print("<------------------------->  ERROR  <------------------------->")
        except Exception as e:
            print(f"{timestamp}: address -> {data['address']}: An error occurred: {e}")
    
    def process(self, data: dict):
        time.sleep(5) # Wait for 5 seconds
        while True:
            self.send_request(data)
            time.sleep(125) # 2 minutes and 5 seconds

    def run(self):
        count_proxies = sum([1 for data in self.data if data["proxy"] is not None])
        print("<------------------------->  START PROGRAM  <------------------------->")
        print(f"Total addresses: {len(self.data)}.")
        print(f"Total addresses with proxies: {count_proxies}.")
        print(f"Total claims in 1 hour per address: {3600/125} Tabi tokens.")
        print(f"Total claims in 24 hours per address: {86400/125} Tabi tokens.")
        print(f"Total claims in 1 hour for all addresses: {len(self.data) * 3600/125} Tabi tokens.")
        print(f"Total claims in 24 hours for all addresses: {len(self.data) * 86400/125} Tabi tokens.")
        print()
        print("You can see additional information in the console.")
        print('Press "Ctrl + C" to stop the program.')
        print()
        print("Starting the threads...")
        print("Info for each address:")
        for data in self.data:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if data["proxy"] is None:
                print(f"{timestamp}: address -> {data['address']}: Proxy is not available..")
            else:
                print(f"{timestamp}: address -> {data['address']}: Proxy is available.")
        print("<------------------------->  START PROGRAM  <------------------------->")
        input("Press Enter to start the program...")
        print()
        for data in self.data:
            threading.Thread(target=self.process, args=(data,)).start() # Start the threads for each address

def validate_format(s):
    pattern = r'^[^:]+:[^:]+:[^:]+:[^:]+:[^:]+$'
    if re.match(pattern, s):
        return True
    else:
        return False

def get_data(filename: str):
    mas = []
    with open(f"{filename}.txt", "r") as file:
        data = file.readlines()
    for element in data:
        element.strip()
        if not validate_format(element):
            print("<------------------------->  ERROR  <------------------------->")
            print("Invalid format in the file")
            print(f"Error in the following line: {element}")
            print("<------------------------->  ERROR  <------------------------->")
            print("Exiting the program...")
            exit(1)
        element_split = element.split(":")
        if element_split[0].lower() == "none" or element_split[1].lower() == "none" or element_split[2].lower() == "none" or element_split[3].lower() == "none":
            proxy = None
        else:
            proxy = {
                "http": f"http://{element_split[2]}:{element_split[3]}@{element_split[0]}:{element_split[1]}",
                "https": f"http://{element_split[2]}:{element_split[3]}@{element_split[0]}:{element_split[1]}"
            }
        address = element_split[4].strip()
        mas.append({
            "proxy": proxy,
            "address": address
        })
    return mas

if __name__ == "__main__":
    filename = "data"
    data = get_data(filename)
    faucet = Faucet(data)
    faucet.run()