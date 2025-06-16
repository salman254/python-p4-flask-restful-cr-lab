#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# GET /plants and POST /plants
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [ 
            {
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                "price": plant.price
            } for plant in plants 
        ], 200

    def post(self):
        data = request.get_json()
        plant = Plant(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price")
        )
        db.session.add(plant)
        db.session.commit()
        return {
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": plant.price
        }, 201

# GET /plants/<id>
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return {
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": plant.price
        }, 200

# Route registration
api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
