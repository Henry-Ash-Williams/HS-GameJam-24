import os

from alien import Alien
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/generate-alien", methods=["GET"])
def generate_alien():
    print("Generating image")
    alien = Alien()
    image = alien.generate_art()
    image.save(f"{alien.alien_id}.png")
    alien.image_url = os.path.join(os.getcwd(), f"{alien.alien_id}.png")
    return jsonify(str(alien))


if __name__ == "__main__":
    app.run(debug=True)
