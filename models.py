from db import db
from queries import YOLO_GRANT_QUERY, BABY_GRANT_QUERY, ELDER_BONUS_QUERY, STUDENT_BONUS_QUERY, MANUAL_QUERY

YOLO_GRANT = "YOLOGSTGrant"
BABY_GRANT = "BabySunshineGrant"
ELDER_BONUS = "ElderBonus"
STUDENT_BONUS = "StudentEncouragementBonus"
CUSTOM_GRANT = "CustomGrant"
MAX_CHAR = 80

HOUSEHOLD_CHOICES = ("Landed","Condominium","HDB")
OCCUPATION_CHOICES = ("Employed","Unemployed","Student")
MARITAL_STATUS_CHOICES = ("Married","Single","Divorced","Widowed")
GENDER_CHOICES = ("M","F")

class Household(db.Model):
    __tablename__ = 'households'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_CHAR))
    type = db.Column(db.String(MAX_CHAR))

    members = db.relationship('Member', cascade = 'all,delete', backref='parent', lazy='dynamic')

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def json(self):
        return {'household_id':self.id, 'name': self.name, 'type': self.type, 'members': [member.json() for member in self.members.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_ids(cls, ids):
        return list(cls.query.filter_by(id=id).first() for id in ids)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_CHAR))
    gender = db.Column(db.String(1))
    marital_status = db.Column(db.String(MAX_CHAR))
    spouse_id = db.Column(db.Integer)
    occupation_type = db.Column(db.String(MAX_CHAR))
    annual_income = db.Column(db.Float(precision=2))
    dob = db.Column(db.String(MAX_CHAR)) # assume DD-MM-YYYY
    household_id = db.Column(db.Integer, db.ForeignKey('households.id'))

    households = db.relationship('Household')

    def __init__(self, name, gender, marital_status, spouse_id, occupation_type, annual_income, dob, household_id):
        self.name = name
        self.gender = gender
        self.marital_status = marital_status
        self.spouse_id = spouse_id
        self.occupation_type = occupation_type
        self.annual_income = annual_income
        self.dob = dob
        self.household_id = household_id

    def json(self):
        return {'member_id':self.id, 'household_id':self.household_id, 'name': self.name, 'gender': self.gender, 'marital_status': self.marital_status, 'spouse_id': self.spouse_id, \
                'occupation_type': self.occupation_type, 'annual_income': self.annual_income, 'dob:': self.dob}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_ids(cls, ids):
        return list(cls.query.filter_by(id=id).first() for id in ids)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class GrantQuery():

    @staticmethod
    def eligible_households(args):

        if args["grant"] == YOLO_GRANT:
            result = db.engine.execute(YOLO_GRANT_QUERY)
            return [row[0] for row in result]

        elif args["grant"] == BABY_GRANT:
            result = db.engine.execute(BABY_GRANT_QUERY)
            return [row[0] for row in result]

        elif args["grant"] == ELDER_BONUS:
            result = db.engine.execute(ELDER_BONUS_QUERY)
            return [row[0] for row in result]

        elif args["grant"] == STUDENT_BONUS:
            result = db.engine.execute(STUDENT_BONUS_QUERY)
            return [row[0] for row in result]

        elif args["grant"] == CUSTOM_GRANT:
            try:
                housing_type = args["housing_type"]
            except:
                housing_type = "Landed','Condominium','HDB"
            try:
                max_total_income = args["max_total_income"]
            except:
                max_total_income = 1e30
            try:
                max_household_size = args["max_household_size"]
            except:
                max_household_size = 1e30

            result = db.engine.execute(MANUAL_QUERY.format(housing_type = housing_type, max_total_income = max_total_income, max_household_size = max_household_size))
            return [row[0] for row in result]
