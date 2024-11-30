import dataclasses
import json
import random
from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class Species(str, Enum):
    Human = "human"
    Splorvax = "splorvax"
    Zarnakins = "zarnakins"
    Phlorgs = "phlorgs"
    Nixogoths = "nixogoths"
    Chorvulans = "chorvulans"
    Shoggoth = "shoggoth"
    Xenomorph = "xenomorph"
    Vogons = "vogons"


@dataclass
class Alien:
    risk: float = 0.0
    heat: float = 0.0
    intoxication: float = 0.0
    species: Species = Species("human")
    let_in: bool = True
    art: np.ndarray = field(default_factory=lambda: np.zeros(1))

    def __post_init__(self):
        self.risk = np.abs(np.random.normal(0, 1))
        self.heat = np.abs(np.random.normal(0, 1))
        self.species = Species(random.choice(list(Species)))

    def to_json(self):
        def convert(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()

            return obj

        serializable_dict = dataclasses.asdict(
            self, dict_factory=lambda items: {k: convert(v) for k, v in items}
        )
        return json.dumps(serializable_dict)


if __name__ == "__main__":
    print(Alien().to_json())
