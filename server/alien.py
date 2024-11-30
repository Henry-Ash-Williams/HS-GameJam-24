import dataclasses
import io
import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
import requests
import torch
from openai import OpenAI
from PIL import Image

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
device = torch.device(
    "mps"
    if torch.backends.mps.is_available()
    else "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


SYSTEM_PROMPT = """
You are a language model who is tasked with generating information about an alien. 

These aliens are trying to enter a nightclub similar to berghain in berlin. You will always be told whether or not they should be allowed entry into this nightclub. 

These aliens will have a set of items on their person, this could include drugs, kink items, and other things people may bring with them to a nightclub. 

You must always respond in JSON, using the following schema: 

{
    "text-to-image": [A physical description of the alien which is later fed into a text-to-image model, must not exceed 77 tokens], 
    "name": [The name of the alien], 
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
    art: Optional[np.ndarray] = None
    description: Optional[str] = None
    name: Optional[str] = None
    species: Optional[str] = None
    items: Optional[List[str]] = None
    demeanor: Optional[str] = None

    def generate_information(self):
        var_desc = (
            "This alien should look like they have some malicous intent"
            if not self.let_in
            else "This alien should look like they do not have any malicious intent"
        )
        prompt = f"Generate information about an alien who should {'not' if not self.let_in else ''} be let into this club."
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

        self.description = (
            information["text-to-image"]
            + " Make sure you only generate a single alien with their head in the center of the frame, do not include a background, or any other elements in the image."
        )
        self.name = information["name"]
        self.species = information["species"]
        self.items = information["items"]
        self.demeanor = information["demeanor"]

    def to_json(self):
        def convert(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        serializable_dict = dataclasses.asdict(
            self, dict_factory=lambda items: {k: convert(v) for k, v in items}
        )
        return json.dumps(serializable_dict)

    def generate_art(self):
        if self.description is None:
            self.populate_information()

        response = client.images.generate(
            model="dall-e-3",
            prompt=self.description,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        res = requests.get(response.data[0].url)
        image = Image.open(io.BytesIO(res.content))
        self.art = np.array(image)
