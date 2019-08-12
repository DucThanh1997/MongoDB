from flask import Flask
from flask_restful import Api

from resources import Student

app = Flask(__name__)
api = Api(app)


api.add_resource(Student, "/student")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
