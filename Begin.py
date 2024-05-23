from openai import OpenAI

import recordaudio
from openai import OpenAI
import json
import texttospeech
import send

while True:
    alreadymessages = [{"role": "system",
                        "content": "Frag immer nach, wenn du nicht sicher bist, welche Daten in eine Funktion einzufügen sind. Mache nie Annahmen. Stelle sicher, dass Tage vom Nutzer sicher festgelegt werden."}]

    arguments = ""

    while True:
        text = recordaudio.record()

        client = OpenAI()

        alreadymessages.append({"role": "user", "content": text})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
                                "beschaftigung": {
                                    "type": "string",
                                    "description": "Die Beschäftigung, die der Nutzer machen möchte.",
                                },
                                "anfangsdatum": {
                                    "type": "string",
                                    "description": "Das Datum, ab dem der Nutzer die Beschäftigung gerne machen würde. Beispiel: '10/11/2022' (DD/MM/YYYY). Wenn nötig berechne das Datum anhand des aktuellen Datums. Heute ist der 24.Mai 2024 und heute ist ein Freitag."
                                },
                                "enddatum": {
                                    "type": "string",
                                    "description": "Das Datum, bis zu dem der Nutzer die Beschäftigung spätestens machen wollen würde. Beispiel: '10/11/2022' (DD/MM/YYYY). Berechne dabei das Datum anhand des aktuellen Datums, wenn nötig. Heute ist der 24.Mai 2024 und heute ist ein Freitag."
                                }
                            },
                            "required": ["beschaftigung", "enddatum", "anfangsdatum"],
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
    tosend["Benutzerid"] = 12354
    send.send(tosend)

    arguments = json.loads(arguments)

    vorlesen = f"Ich habe für dich die Aktivität {arguments['beschaftigung']} eingetragen. Sie findet vom {arguments['anfangsdatum']} bis zum {arguments['enddatum']} statt."

    texttospeech.texttospeech(vorlesen)
