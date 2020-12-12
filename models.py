from db import db


class HouseholdModel(db.Model):
    __tablename__ = 'households'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))

    members = db.relationship('MemberModel', cascade = 'all,delete', backref='parent', lazy='dynamic')

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def json(self):
        return {'household_id':self.id, 'name': self.name, 'type': self.type, 'members': [member.json() for member in self.members.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def eligible_households(cls,grant):

        return cls.query.filter_by(name=grant).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class MemberModel(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    gender = db.Column(db.String(80)) # assume only 2 genders, M and F.
    marital_status = db.Column(db.String(80))
    spouse = db.Column(db.String(80))
    occupation_type = db.Column(db.String(80))
    annual_income = db.Column(db.Float(precision=2))
    DOB = db.Column(db.String(80)) # assume DD-MM-YYYY
    household_id = db.Column(db.Integer, db.ForeignKey('households.id'))

    household = db.relationship('HouseholdModel')

    def __init__(self, name, gender, marital_status, spouse, occupation_type, annual_income, DOB, household_id):
        self.name = name
        self.gender = gender
        self.marital_status = marital_status
        self.spouse = spouse
        self.occupation_type = occupation_type
        self.annual_income = annual_income
        self.DOB = DOB
        self.household_id = household_id

    def json(self):
        return {'member_id':self.id, 'name': self.name, 'gender': self.gender, 'marital_status': self.marital_status, 'spouse': self.spouse, \
                'occupation type': self.occupation_type, 'annual income': self.annual_income, 'date of birth:': self.DOB}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
