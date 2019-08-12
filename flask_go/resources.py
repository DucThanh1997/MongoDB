from flask_restful import reqparse, Resource
from config import db
from flask import jsonify
from bson.json_util import dumps


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("birth_date", type=str)
    parser.add_argument("class", type=list)
    # thử add vài arguement dị vào
    parser.add_argument("class_too", type=dict)

    def post(self):
        data = Student.parser.parse_args()
        student = {
            "name": data["name"],
            "birth date": data["birth_date"],
            "class": data["class"],
            "class_too": data["class_too"],
        }
        try:
            db.student.insert_one(student)
        except:
            return {"messages": "error"}
        return {"messages": "okke"}

    def get(self):
        list = db.student.find()
        return dumps(list)

    def put(self):
        data = Student.parser.parse_args()
        student = db.student.find_one({})

        update_document = db.student.update_one({"_id": student.get("_id")}, {"$set": {"name": data["name"]}})

        return {"messages": "okke"}

    def delete(self):
        db.student.delete_one({"name": "Nam"})
        return {"messages": "okke"}
