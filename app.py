from flask import Flask
from flask_restful import Api
from resources import HouseholdListController, HouseholdController, MemberListController, MemberController, GrantSearch
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

# create db
@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(HouseholdListController, '/households')
api.add_resource(HouseholdController, '/household/<string:id>')
api.add_resource(MemberListController, '/members')
api.add_resource(MemberController, '/member/<string:id>')
api.add_resource(GrantSearch, '/households/grant')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
