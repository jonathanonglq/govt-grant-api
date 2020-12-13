from flask_restful import Resource, reqparse
from models import Household, Member, GrantQuery, HOUSEHOLD_CHOICES, OCCUPATION_CHOICES, MARITAL_STATUS_CHOICES, GENDER_CHOICES

class HouseholdController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("type",
                        required=True,
                        choices=HOUSEHOLD_CHOICES,
                        help="This household must have a household type - HDB, Condominium or Landed."
                        )

    def get(self, name):

        household = Household.find_by_name(name)
        if household:
            return {"data":household.json(), "message": None}, 200
        return {"data":None, "message": "Household not found."}, 404

    def post(self, name):
        data = HouseholdController.parser.parse_args()
        household = Household(name, data["type"])
        try:
            household.save_to_db()
        except:
            return {"data":None, "message": "An error occurred while creating the household."}, 500
        return {"data":household.json(), "message": None}, 201

    def delete(self, name):
        household = Household.find_by_name(name)
        if household:
            household.delete_from_db()
            return {"data":None, "message": "Household deleted."}, 200
        return {"data":None, "message": "Household not found."}, 404


class HouseholdList(Resource):
    def get(self):
        return {"data": list(map(lambda x: x.json(), Household.query.all())), "message": None}, 200


class MemberController(Resource):
    parser = reqparse.RequestParser()
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
    parser.add_argument("spouse",
                        required=True,
                        help="Enter the name of your spouse."
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

    def get(self, name):
        member = Member.find_by_name(name)
        if member:
            return {"data":member.json(), "message": None}, 200
        return {"data":None, "message": "Member not found."}, 404

    def post(self, name):
        # if Member.find_by_name(name):
        #     return {"message": "An member with name "{}" already exists.".format(name)}, 400

        data = MemberController.parser.parse_args()

        if Household.find_by_ids([data["household_id"]])[0] is None:
            return {"data":None, "message": "Household not found."}, 404

        member = Member(name, data["gender"], data["marital_status"], data["spouse"], data["occupation_type"], data["annual_income"], data["dob"], data["household_id"])

        try:
            member.save_to_db()
        except:
            return {"data":None, "message": "An error occurred while inserting the member."}, 500

        return {"data":member.json(), "message": None}, 201


    def delete(self, name):
        member = Member.find_by_name(name)
        if member:
            member.delete_from_db()
            return {"data":None, "message": "Member deleted."}, 200
        return {"data":None, "message": "Member not found."}, 404

    def put(self, name):
        data = MemberController.parser.parse_args()

        if Household.find_by_ids([data["household_id"]])[0] is None:
            return {"data":None, "message": "Household not found."}, 404

        member = Member.find_by_name(name)

        if member:
            member.gender = data["gender"]
            member.marital_status = data["marital_status"]
            member.spouse = data["spouse"]
            member.occupation_type = data["occupation_type"]
            member.annual_income = data["annual_income"]
            member.dob = data["dob"]
            member.household_id = data["household_id"]
            member.save_to_db()
            return {"data":member.json(), "message": "Member has been updated."}, 204

        member = Member(name, data["gender"], data["marital_status"], data["spouse"], data["occupation_type"], data["annual_income"], data["dob"], data["household_id"])
        member.save_to_db()
        return {"data":member.json(), "message": "Member has been created."}, 201


class MemberList(Resource):
    def get(self):
        return {"data": list(map(lambda x: x.json(), Member.query.all())), "message": None}, 200

class GrantSearch(Resource):
    def get(self, grant):
        result = GrantQuery.eligible_households(grant)
        households = Household.find_by_ids(result)
        return {"data":list(map(lambda x: x.json(), households)), "message": None}, 200
        # return result
