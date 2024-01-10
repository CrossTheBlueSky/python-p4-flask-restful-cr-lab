#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/plants', methods=['GET', 'POST'])
def plants():
    if request.method == 'GET':
        plants = Plant.query.all()
        plant_response = []
        for plant in plants:
            plant_response.append(plant.to_dict())
        
        return make_response(plant_response, 200)
    
    if request.method == 'POST':
        new_plant = Plant(
            name = request.json.get('name'),
            image = request.json.get('image'),
            price = request.json.get('price')
            )
        db.session.add(new_plant)
        db.session.commit()


@app.route('/plants/<int:id>')
def get_plant_by_id(id):
    plant = Plant.query.filter(Plant.id == id).first().to_dict()
    print(plant)
    return make_response(plant, 200)


class Plants(Resource):
    pass

class PlantByID(Resource):
    pass
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
