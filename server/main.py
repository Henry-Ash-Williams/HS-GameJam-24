import os

from alien import Alien
from flask import Flask, abort, jsonify

app = Flask(__name__)

aliens = {}


@app.route("/generate-artwork/<id>", methods=["GET"])
def generate_artwork(id: str):
    try:
        alien = aliens[id]
    except:
        abort(404, "Could not find an alien with that ID")

    image = alien.generate_art()
    image.save(f"{alien.alien_id}.png")
    alien.image_url = os.path.join(os.getcwd(), f"{alien.alien_id}.png")
    return jsonify(str(alien))


@app.route("/generate-alien", methods=["GET"])
def generate_alien():
    alien = Alien()
    aliens[alien.alien_id] = alien
    return jsonify(str(alien))


if __name__ == "__main__":
    app.run(debug=True)
