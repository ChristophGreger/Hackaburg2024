import requests
import json

def send(data) -> dict:
    try:
        url = "http://192.168.220.183:8080/general/addoccasion"
        response = requests.post(url, json=data)

        print("Status Code", response.status_code)
        if response.content:
            print("JSON Response ", response.content)
            return response.json()
        return {}
    except:
        return {}
