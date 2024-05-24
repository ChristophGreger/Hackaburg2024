import requests
import data
import json

matchedpersons = []
aktivitat = None
Datum = None

url = "http://192.168.220.183:8080/general/matches"


def get_matches():
    global matchedpersons
    global aktivitat
    global Datum
    # for testing
    mydict = {"id": data.BenutzerID}
    response = requests.post(url, data=json.dumps(mydict))
    mydict = response.json()
    if not mydict:
        matchedpersons.clear()
        aktivitat = None
    else:
        for x in mydict["Participants"]:
            if {"Vorname": x["Forename"], "Nachname": x["Surname"], "Telefonnummer": x["PhoneNumber"]} not in matchedpersons:
                matchedpersons.append({"Vorname": x["Forename"], "Nachname": x["Surname"], "Telefonnummer": x["PhoneNumber"]})

        aktivitat = mydict["Activity"]
        date = mydict["Date"].split("-")
        Datum = f"{date[2][0:2]}.{date[1][0:2]}.{date[0][0:4]}"
