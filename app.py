from flask import Flask
from flask_restful import Api

from resources import HouseholdList, Household, MemberList, Member
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

# create db
@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(HouseholdList, '/households')
api.add_resource(Household, '/household/<string:name>')
api.add_resource(MemberList, '/members')
api.add_resource(Member, '/member/<string:name>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
