import requests
import data

matchedpersons = [{"Vorname": "Max", "Nachname": "Mustermann", "Telefonnummer": "0123456789"}]
aktivitat = "Fussball"

url = "http://192.168.220.183:8080/general/matches"


def get_matches():
    global matchedpersons
    global aktivitat
    # for testing purpose
    aktivitat = None
    # response = requests.post(url, data=data.BenutzerID)
    # TODO Parse the response and set the global variables matchedpersons and aktivitat
    # print(response.json())
