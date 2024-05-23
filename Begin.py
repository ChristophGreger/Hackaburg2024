from openai import OpenAi

import recordaudio
from openai import OpenAI

while True:

    text = recordaudio.record()

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=300,
        temperature=0,
        messages=[
            {"role": "system",
             "content": "Frag immer nach, wenn du nicht sicher bist, welche Daten in eine Funktion einzufügen sind. Mache nie Annahmen. Stelle sicher, dass Tage vom Nutzer sicher festgelegt werden."},
            {"role": "user", "content": text}
        ],
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
                                "description": "Das Datum, ab dem der Nutzer die Beschäftigung gerne machen würde. Beispiel: '10/11/2022' (DD/MM/YYYY). Wenn nötig berechne das Datum anhand des aktuellen Datums. Heute ist der 21.April 2024"
                            },
                            "enddatum": {
                                "type": "string",
                                "description": "Das Datum, bis zu dem der Nutzer die Beschäftigung spätestens machen wollen würde. Beispiel: '10/11/2022' (DD/MM/YYYY). Berechne dabei das Datum anhand des aktuellen Datums, wenn nötig."
                            }
                        },
                        "required": ["beschäftigung", "enddatum", "anfangsdatum"],
                    },
                },
            }
        ]
    )

    print(completion.choices[0].message)


    break