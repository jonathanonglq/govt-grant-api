from flask_restful import Resource, reqparse, request
from models import Household, Member, GrantQuery, HOUSEHOLD_CHOICES, OCCUPATION_CHOICES, MARITAL_STATUS_CHOICES, GENDER_CHOICES

class HouseholdController(Resource):

    def get(self, id):

        household = Household.find_by_ids([id])[0]
        if household:
            return {"data":household.json(), "message": None}, 200
        return {"data":None, "message": "Household not found."}, 404

    def delete(self, id):
        household = Household.find_by_ids([id])[0]
        if household:
            household.delete_from_db()
            return {"data":None, "message": "Household deleted."}, 200
        return {"data":None, "message": "Household not found."}, 404

    def put(self, id):
        household = Household.find_by_ids([id])[0]
        data = HouseholdListController.parser.parse_args()

        if household:
            household.name = data["name"]
            household.type = data["type"]
            household.save_to_db()
            return {"data":household.json(), "message": "Household has been updated."}, 204

        household = Household(**data)
        household.save_to_db()
        return {"data":household.json(), "message": "Household has been created."}, 201


class HouseholdListController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
                        required=True,
                        help="Please enter a name for this household."
                        )
    parser.add_argument("type",
                        required=True,
                        choices=HOUSEHOLD_CHOICES,
                        help="This household must have a household type - HDB, Condominium or Landed."
                        )
    def get(self):
        return {"data": [x.json() for x in Household.query.all()], "message": None}, 200


    def post(self):
        data = HouseholdListController.parser.parse_args()
        household = Household(**data)
        try:
            household.save_to_db()
        except:
            return {"data":None, "message": "An error occurred while creating the household."}, 500
        return {"data":household.json(), "message": None}, 201


class MemberController(Resource):

    def get(self, id):
        member = Member.find_by_ids([id])[0]
        if member:
            return {"data":member.json(), "message": None}, 200
        return {"data":None, "message": "Member not found."}, 404

    def delete(self, id):
        member = Member.find_by_ids([id])[0]
        if member:
            member.delete_from_db()
            return {"data":None, "message": "Member deleted."}, 200
        return {"data":None, "message": "Member not found."}, 404

    def put(self, id):
        data = MemberListController.parser.parse_args()

        if Household.find_by_ids([data["household_id"]])[0] is None:
            return {"data":None, "message": "Household not found."}, 404

        member = Member.find_by_ids([id])[0]

        if member:
            member.name = data["name"]
            member.gender = data["gender"]
            member.marital_status = data["marital_status"]
            member.spouse_id = data["spouse_id"]
            member.occupation_type = data["occupation_type"]
            member.annual_income = data["annual_income"]
            member.dob = data["dob"]
            member.household_id = data["household_id"]
            member.save_to_db()
            return {"data":member.json(), "message": "Member has been updated."}, 204

        member = Member(**data)
        member.save_to_db()
        return {"data":member.json(), "message": "Member has been created."}, 201


class MemberListController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
                        required=True,
                        help="This member must have a name."
                        )
    parser.add_argument("gender",
                        required=True,
                        choices = GENDER_CHOICES,
                        help="This member must have a gender - M or F."
                        )
    parser.add_argument("marital_status",
                        required=True,
                        choices = MARITAL_STATUS_CHOICES,
                        help="This member must have a marital status - Single, Married, Divorced, or Widowed."
                        )
    parser.add_argument("spouse_id",
                        required=True,
                        help="If applicable, enter the id of your spouse. Otherwise, enter 0."
                        )
    parser.add_argument("occupation_type",
                        required=True,
                        choices = OCCUPATION_CHOICES,
                        help="This member must have an occupation type - Employed, Unemployed, or Student."
                        )
    parser.add_argument("annual_income",
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument("dob",
                        required=True,
                        help="This field cannot be left blank! Enter date of birth in 'YYYY-MM-DD' form."
                        )
    parser.add_argument("household_id",
                        type=int,
                        required=True,
                        help="Every member must have a household_id."
                        )
    def get(self):
        return {"data": [x.json() for x in Member.query.all()], "message": None}, 200

    def post(self):

        data = MemberListController.parser.parse_args()

        if Household.find_by_ids([data["household_id"]])[0] is None:
            return {"data":None, "message": "Household not found."}, 404

        member = Member(**data)

        try:
            member.save_to_db()
        except:
            return {"data":None, "message": "An error occurred while inserting the member."}, 500

        return {"data":member.json(), "message": None}, 201

class GrantSearch(Resource):

    def get(self):
        result = GrantQuery.eligible_households(request.args)
        households = Household.find_by_ids(list(set(result)))
        return {"data":[x.json() for x in households], "message": None}, 200
