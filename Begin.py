import recordaudio
from openai import OpenAI
import json
import texttospeech
import data
import send


def run():
    while True:
        alreadymessages = [{"role": "system",
                            "content": "Frag immer nach, wenn du nicht sicher bist, welche Daten in eine Funktion einzufügen sind. Mache nie Annahmen. Heute ist der 24.05.2024. Der Wochentag heute ist Freitag. Benutze in deiner Antwort keine Sonderzeichen. Antworte nicht in langen Antworten!"}]

        arguments = ""

        while True:
            text = recordaudio.record()

            client = OpenAI()

            alreadymessages.append({"role": "user", "content": text})

            completion = client.chat.completions.create(
                model="gpt-4-turbo",
                max_tokens=300,
                temperature=0,
                messages=alreadymessages,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "bekunde_interesse",
                            "description": "Erlaubt es dem Nutzer, sich in eine Liste einzutragen, um eine Freizeitbeschäftigung zu machen.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "activity": {
                                        "type": "string",
                                        "description": "Die Beschäftigung, die der Nutzer machen möchte.",
                                    },
                                    "startTime": {
                                        "type": "string",
                                        "description": "Das Datum, ab dem der Nutzer die Beschäftigung gerne machen würde. Beispiel: '25/05/2024' (DD/MM/YYYY)"
                                    },
                                    "endTime": {
                                        "type": "string",
                                        "description": "Das Datum, bis zu dem der Nutzer die Beschäftigung spätestens machen wollen würde. Beispiel: '25/05/2024' (DD/MM/YYYY)"
                                    }
                                },
                                "required": ["activity", "endTime", "startTime"],
                            },
                        },
                    }
                ]
            )

            # Get the message from the completion
            message = completion.choices[0].message

            # Convert the message to JSON
            if message.tool_calls:
                arguments = message.tool_calls[0].function.arguments
                break
            else:
                alreadymessages.append({"role": "assistant", "content": message.content})
                print(message.content)
                texttospeech.texttospeech(message.content)
                continue

        print(arguments)

        # Hier müssen jetzt die Sachen an den Server geschickt werden
        # Ip adresse von henrik: 192.168.220.183
        tosend = json.loads(arguments)
        tosend["organizer"] = data.BenutzerID
        print(tosend)
        response = send.send(tosend)
        print("Sent")

        arguments = json.loads(arguments)

        print(arguments)


        print("Response")
        print(response)

        if response != None and "forbidden" in response.keys():
            vorlesen = f"Es tut mir leid, aber du kannst dich nur für eine Aktivität glechzeitig eintragen. Deine letzte Anfrage wurde daher ignoriert."
            texttospeech.texttospeech(vorlesen)
            continue

        vorlesen = f"Ich habe für dich die Aktivität {arguments['activity']} eingetragen. Sie findet zwischen dem {arguments['startTime']} und dem {arguments['endTime']} statt."

        texttospeech.texttospeech(vorlesen)
