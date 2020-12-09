from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import datetime

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
    marital_status_choices = ('Married','Single','Divorced','Widowed')

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
        parser.add_argument('marital_status', required=True, choices=Household.marital_status_choices)
        parser.add_argument('spouse', required=True)
        parser.add_argument('occupation_type', required=True, choices=Household.occupation_choices)
        parser.add_argument('annual_income', required=True, type=int)
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

class GrantSearch(Resource):
    grant_choices = ('Student Encouragement Bonus','Family Togetherness Scheme','Elder Bonus'\
        ,'Baby Sunshine Grant','YOLO GST Grant')

    def age(DOB):
        return (datetime.datetime.now() - datetime.datetime.strptime(DOB,'%d/%m/%Y')).days/365.25

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('grant', required=True, choices=GrantSearch.grant_choices)

        data = parser.parse_args()

        #Student Encouragement Bonus
        if data['grant'] == 'Student Encouragement Bonus':

            target_id_1 = []
            for household in households:
                for member in household['members']:
                    if GrantSearch.age(member['DOB']) < 16:
                        target_id_1.append(household['id'])
                        break

            target_id_2 = []
            for household in households:
                total_income = 0
                for member in household['members']:
                    total_income += member['annual_income']
                if total_income < 150000:
                    target_id_2.append(household['id'])

            target_id = list(set(target_id_1).intersection(set(target_id_2)))
            eligible_households = list(filter(lambda x: x['id'] in target_id, households))
            return{'households': eligible_households}, 200

        #Family Togetherness Scheme
        if data['grant'] == 'Family Togetherness Scheme':

            target_id_1 = []
            for household in households:
                for i in range(len(household['members'])):
                    if household['members'][i]['marital_status'] == 'Married':
                        for j in range(i+1, len(household['members'])):
                            if ((household['members'][i]['spouse'] == household['members'][j]['name'])&\
                                (household['members'][i]['name'] == household['members'][j]['spouse'])):
                                target_id_1.append(household['id'])
                                break
            target_id_2 = []
            for household in households:
                for member in household['members']:
                    if GrantSearch.age(member['DOB']) < 18:
                        target_id_2.append(household['id'])
                        break

            target_id = list(set(target_id_1).intersection(set(target_id_2)))
            eligible_households = list(filter(lambda x: x['id'] in target_id, households))
            return{'households': eligible_households}, 200

        #Elder Bonus
        if data['grant'] == 'Elder Bonus':
            target_id = []
            for household in households:
                for member in household['members']:
                    if GrantSearch.age(member['DOB']) > 50:
                        target_id.append(household['id'])
                        break

            eligible_households = list(filter(lambda x: x['id'] in target_id, households))
            return{'households': eligible_households}, 200

        #Baby Sunshine Grant
        if data['grant'] == 'Baby Sunshine Grant':
            target_id = []
            for household in households:
                for member in household['members']:
                    if GrantSearch.age(member['DOB']) < 5:
                        target_id.append(household['id'])
                        break

            eligible_households = list(filter(lambda x: x['id'] in target_id, households))
            return{'households': eligible_households}, 200

        # YOLO GST Grant
        if data['grant'] == 'YOLO GST Grant':
            target_id = []
            for household in households:
                total_income = 0
                for member in household['members']:
                    total_income+= member['annual_income']
                if total_income < 100000:
                    target_id.append(household['id'])

            eligible_households = list(filter(lambda x: x['id'] in target_id, households))
            return {'households': eligible_households}, 200

api.add_resource(HouseholdList, '/household')
api.add_resource(Household, '/household/<string:id>')
api.add_resource(MemberList, '/household/<string:id>/members')
api.add_resource(GrantSearch, '/household/grantsearch')

if __name__ == '__main__':
    app.run(debug=True)
