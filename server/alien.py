import io
import json
import os
import string
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
import requests
from openai import OpenAI
from PIL import Image

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

NAMES = [
    "Zorvynex",
    "Krellithar",
    "Thaloxa",
    "Vyntrix",
    "Omarak",
    "Xilenth",
    "Dravokar",
    "Qelthori",
    "Nyxora",
    "Aztrion",
    "Phorvix",
    "Yraxal",
    "Tzorrek",
    "Lixavor",
    "Chyrron",
    "Uxiltra",
    "Malkithis",
    "Kronvaar",
    "Zynarrax",
    "Belthorax",
    "Veltraxion",
    "Korvethis",
    "Xathorin",
    "Pryllith",
    "Zynquar",
    "Droxelis",
    "Lomaraen",
    "Ultharek",
    "Quaravex",
    "Xylandor",
    "Frylthara",
    "Nymexis",
    "Voktril",
    "Chirvessa",
    "Omralith",
    "Zaruketh",
    "Torvalis",
    "Ekrizion",
    "Sylthoran",
    "Brethix",
]


SYSTEM_PROMPT = """
You are a language model who is tasked with generating information about an alien. 

These aliens are trying to enter a nightclub similar to berghain in berlin. You will always be told whether or not they should be allowed entry into this nightclub, and their name. 

These aliens will have a set of items on their person, this could include drugs, kink items, and other things people may bring with them to a nightclub. 

Make sure you generate a diverse descriptions, giving something new everytime, and taking care not to generate similar descriptions in the same session.

You must always respond in JSON, using the following schema: 

{
    "text-to-image": [A physical description of the alien which is later fed into a text-to-image model, must not exceed 77 tokens], 
    "species": [The species of the alien],
    "items": [A list of items the alien has on them],
    "demeanor": [How the alien acts while being interrogated by the bouncer],
}
"""


@dataclass
class Alien:
    let_in: bool = field(
        default_factory=lambda: bool(np.random.choice([True, False], p=[0.75, 0.25]))
    )
    image_url: Optional[str] = None
    description: Optional[str] = None
    name: str = field(default_factory=lambda: np.random.choice(NAMES))
    species: Optional[str] = None
    items: Optional[List[str]] = None
    demeanor: Optional[str] = None
    alien_id: str = field(
        default_factory=lambda: "".join(
            [np.random.choice(list(string.ascii_letters)) for i in range(32)]
        )
    )

    def __post_init__(self):
        self.populate_information()

    def generate_information(self):
        prompt = f"Generate information about an alien named {self.name} who should {'not' if not self.let_in else ''} be let into this club."
        messages = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {"role": "user", "content": prompt},
            ],
            model="gpt-4o-mini",
        )
        return messages.choices[0].message.content

    def populate_information(self):
        information = json.loads(self.generate_information())

        self.description = information["text-to-image"]
        self.species = information["species"]
        self.items = information["items"]
        self.demeanor = information["demeanor"]

    def __str__(self):
        tmp = {
            "let_in": self.let_in,
            "image_url": self.image_url,
            "description": self.description,
            "name": self.name,
            "species": self.species,
            "items": self.items,
            "demeanor": self.demeanor,
            "alien_id": self.alien_id,
        }
        return json.dumps(tmp, ensure_ascii=False)

    def generate_art(self):
        if self.description is None:
            self.populate_information()

        print("Generating image")
        response = client.images.generate(
            model="dall-e-3",
            prompt=self.description
            + " Make sure you only generate a single alien with their head in the center of the frame, do not include a background, or any other elements in the image.",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        print("Downloading")
        res = requests.get(response.data[0].url)
        print("Converting to image")
        return Image.open(io.BytesIO(res.content))


if __name__ == "__main__":
    a = Alien()
    print(a)
    a.generate_art().show()
