import json
import os
import openai

class API:
    def __init__(self) -> None:
        self.apikey = str(os.getenv('api_key'))

    def _process_text(self, data):
        abilities = data.get('abilities')
        profession = data.get('profession')
        config = data.get('config')
        expected = data.get('expected')
        text = f"""
            Context:
            Create a background history for an enemy character for cthulhu 7th edition RPG based on the given information.
            The values for abilities must be numbers from 0-100 according to the cthulhu keeper's guide book 7th edition.
            You must fill the list of abilities given, according to the cthulhu keeper's guide book 7th edition, and pass me a json with reasonable values for the abilites based on the profession.
            Profession: {profession}
            Abilities: {abilities}
            Base Information (JSON):
            {config}
            Expected Output to fill(JSON):
            {expected}
        """
        return text

    def get_info(self, data):
        openai.api_key = self.apikey
        text = self._process_text(data)
        messages = [
            {"role": "user", "content": text},
        ]
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        return json.loads(reply.replace("'", '"'))
