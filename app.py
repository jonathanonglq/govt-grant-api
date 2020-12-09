from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

with open('data.json') as json_file:
    households = json.load(json_file)

class HouseholdList(Resource):
    def get(self):
        return {'households': households}, 200

class Household(Resource):

    household_choices = ('Landed','Condominium','HDB')
    occupation_choices = ('Employed','Unemployed','Student')

    def get(self, id):
        household = next(filter(lambda x: x['id'] == id, households), None)
        if household:
            return {'household': household}, 200
        return {'message': "A household with id '{}' does not exist.".format(id)}, 404

    def post(self, id):
        if next(filter(lambda x: x['id'] == id, households), None):
            return {'message': "A household with id '{}' already exists.".format(id)}, 400

        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True, choices=Household.household_choices)
        data = parser.parse_args()

        household = {'id': id, 'type': data['type'], 'members':[]}
        households.append(household)
        return household, 201

    def delete(self, id):
        global households
        if next(filter(lambda x: x['id'] == id, households), None) == None:
            return {'message': "A household with id '{}' does not exist.".format(id)}, 404

        households = list(filter(lambda x: x['id'] != id, households))
        return {'message': 'Household deleted'}, 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True, choices=Household.household_choices)
        data = parser.parse_args()

        household = next(filter(lambda x: x['id'] == id, households), None)

        if household is None:
            household = {'id': id, 'type': data['type'], 'members':[]}
            households.append(household)
        else:
            household.update(data)
        return household, 200

class MemberList(Resource):

    def post(self, id):

        if next(filter(lambda x: x['id'] == id, households), None) == None:
            return {'message': "A household with id '{}' does not exist.".format(id)}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('gender', required=True)
        parser.add_argument('marital_status', required=True)
        parser.add_argument('spouse', required=True)
        parser.add_argument('occupation_type', required=True, choices=Household.occupation_choices)
        parser.add_argument('annual_income', required=True)
        parser.add_argument('DOB', required=True)

        data = parser.parse_args()
        new_member = {'name': data['name'], 'gender': data['gender'], 'marital_status':data['marital_status'], 'spouse':data['spouse'],\
                        'occupation_type': data['occupation_type'], 'annual_income': data['annual_income'], 'DOB': data['DOB']
                    }

        for household in households:
            if household['id'] == id:
                if next(filter(lambda x: x['name'] == data['name'], household['members']), None):
                    return {'message': "A member with the name '{}' already exists in this household.".format(data['name'])}, 400

                household['members'].append(new_member)

        return household, 201

    def delete(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)

        data = parser.parse_args()
        for household in households:
            if household['id'] == id:
                for member in household['members']:
                    if member['name'] == data['name']:
                        household['members'] = list(filter(lambda x: x['name'] != data['name'], household['members']))
                        return {'message':'member deleted'}, 200

                return {'message': 'member not found'}, 404

        return {'message': 'household not found'}, 404


api.add_resource(HouseholdList, '/household')
api.add_resource(Household, '/household/<string:id>')
api.add_resource(MemberList, '/household/<string:id>/members')

if __name__ == '__main__':
    app.run(debug=True)
