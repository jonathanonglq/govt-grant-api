# Government Grant Disbursement API #

This is a RESTful API which allows users to decide which group(s) of households are eligible for various government grants*.

*\*Note that all grants mentioned here are fictitious and do not reflect actual grants that are being worked on or implemented by any government ministries.*

## Installation ##

The API is built using Python and Flask (using Flask-SQLAlchemy as the ORM), and requires the following libraries to be installed:

```
pip install Flask
pip install Flask-RESTful
pip install Flask-SQLAlchemy
```

## Running the Application ##

The application uses SQLite3, a lightweight disk-based database which does not require additional start-up steps. Once the application is started up and a request is executed, a database file ```database.db``` will automatically be created. Subsequent use of the application will read from/write to this database file. Start the application by running the following command:

```
python app.py
```

## Available Endpoints

The following endpoints allow objects, namely Households and Members, to be manipulated upon requests:

##### Household-related endpoint(s):
- Show all households : ```GET /households)```
- Create a household : ```POST /households)```
- Show household of specific id: ```GET /household/<string:id>)```
- Update household of specific id: ```PUT /household/<string:id>)```
- Delete household of specific id: ```DELETE /household/<string:id>)```

##### Member-related endpoint(s):
- Show all members: ```GET /members)```
- Create a member: ```POST /members)```
- Show member of specific id: ```GET /member/<string:id>)```
- Update member of specific id: ```PUT /member/<string:id>)```
- Delete member of specific id: ```DELETE /member/<string:id>)```       

##### Grant-related endpoint(s):
- Show all households eligible for a selected grant: ```GET /households/grant?grant=<string:grant>)```

## Object Fields

##### Household:
- ```household_id``` - Unique identifier automatically assigned by database
- ```name``` - Name of household
- ```type``` - Type of household: 'HDB', 'Condominium', or 'Landed'
- ```members``` - Members belonging to the household (initiated as an empty list when a household is created)

##### Members:
- ```member_id``` - Unique Identifier automatically assigned by database
- ```household_id``` - Unique Identifier of the household this member belongs to
- ```name``` - Name of member
- ```gender```- Gender of member: 'M' or 'F'
- ```marital_status``` - Marital status of member: 'Married', 'Single', 'Divorced', or 'Widowed'
- ```spouse_id``` - Unique Identifier of spouse ('0' if not applicable)
- ```occupation_type``` - Occupation status of member: 'Employed', 'Unemployed', or 'Student'
- ```annual_income``` - Annual income of member
- ```dob``` - date of birth in the format YYYY-MM-DD

## Grant Eligibility
The list of grant types (and the corresponding query string) available are:
- Student Encouragement Bonus (```StudentEncouragementBonus```)
  - Households with children younger than 16 years old
  - Households with annual income of less than $150,000
- Family Togetherness Scheme (```FamilyTogethernessScheme```)
  - Households with husband and wife
  - Households with children younger than 18 years old
- Elder Bonus (```ElderBonus```)
  - Households with family members above the age of 50
  - HDB Household
- Baby Sunshine Grant (```BabySunshineGrant```)
  - Households with children younger than 5 years old
- YOLO GST Grant (```YOLOGSTGrant```)
  - Households with annual income of less than $100,000
  - HDB Household
- Custom Grant with customisable filters (```CustomGrant```)
  - ```housing_type```
  - ```max_total_income```
  - ```max_household_size```

## Assumptions and Notes
- Empty households are not qualified for grants.
- Members cannot exist without a household (i.e. member(s) must be assigned the unique identifier of an existing household at point of creation).
- Deleting a household will delete all members within that household.
- The **Student Encouragement Bonus** function assumes that any household with member(s) below 16 years old qualify (in addition to meeting the household annual income criterion), even if there are no "parents" in the household.
- The **Family Togetherness Scheme** function assumes that the husband and wife within the household are 18 years old and older, and regards any other member(s) within the household that are younger than 18* years old as their "children".
- The **Baby Sunshine Grant** function assumes that any household with member(s) below 5 years old qualify, even if there are no "parents" in the household.
- The **Custom Grant** function assumes that an unapplied filter would mean defaulting to all possible values (e.g. 'HDB', 'Condominium', 'Landed' for ```housing_type```).

*\*The minimum age of marriage in Singapore is 18, unless the Ministry of Social and Family Development grants a special marriage licence with the necessary parental consent so that a minor can marry.*

## Example of API Responses
#### 1. Getting all households:
**Method**: ```GET```\
**URL** : ```/households```\
**Response** : ```200 OK```\
**Content Example**:
```javascript   
{
    "data": [
        {
            "household_id": 1,
            "name": "household_1",
            "type": "HDB",
            "members": [
                {
                    "member_id": 1,
                    "household_id": 1,
                    "name": "Sarah Lee",
                    "gender": "F",
                    "marital_status": "Married",
                    "spouse_id": 2,
                    "occupation type": "Student",
                    "annual income": 0.0,
                    "date of birth:": "1990-01-01"
                },
                {
                    "member_id": 2,
                    "household_id": 1,
                    "name": "Tommy Lee",
                    "gender": "M",
                    "marital_status": "Married",
                    "spouse_id": 1,
                    "occupation type": "Employed",
                    "annual income": 50000.0,
                    "date of birth:": "1988-05-01"
                }
            ]
        },
        {
            "household_id": 2,
            "name": "household_2",
            "type": "Landed",
            "members": [
                {
                    "member_id": 3,
                    "household_id": 2,
                    "name": "Ronald Ong",
                    "gender": "M",
                    "marital_status": "Single",
                    "spouse_id": 0,
                    "occupation type": "Employed",
                    "annual income": 80000.0,
                    "date of birth:": "1984-05-01"
                }
            ]
        }
    ],
    "message": null
}
```
#### 2. Creating an empty household ("household_id" is automatically assigned):

**Method**: ```POST```\
**URL** : ```/households```\
**Body** :
```
"name": "household_1"
"type": "HDB"
```
**Response** : ```201 CREATED```\
**Content Example**:
```javascript   
{
    "data": {
        "household_id": 1,
        "name": "household_1",
        "type": "HDB",
        "members": []
    },
    "message": null
}
```
#### 3. Getting a household of a specific id:

**Method**: ```GET```\
**URL** : ```/household/<household_id>```\
**Response** : ```200 OK```\
**Content Example**:
```javascript   
{
    "data": {
        "household_id": 2,
        "name": "household_2",
        "type": "Landed",
        "members": [
            {
                "member_id": 3,
                "household_id": 2,
                "name": "Ronald Ong",
                "gender": "M",
                "marital_status": "Single",
                "spouse_id": 0,
                "occupation type": "Employed",
                "annual income": 80000.0,
                "date of birth:": "1984-05-01"
            }
        ]
    },
    "message": null
}
```
#### 4. Deleting a household (all members within the household are also deleted):

**Method**: ```DELETE```\
**URL** : ```/household/<household_id>```\
**Response** : ```200 OK```\
**Content Example**:
```javascript   
{
    "data": null,
    "message": "Household deleted."
}
```
#### 5. Creating a member within a household ("member_id" is automatically assigned):

**Method**: ```POST```\
**URL** : ```/members```\
**Body** :
```
"name" : "James Lee",
"gender" : "M",
"marital_status" : "Single",
"spouse_id" : 0,
"occupation_type" : "Employed",
"annual_income" : 50000,
"dob" : "1982-01-01",
"household_id":1
```
**Response** : ```201 CREATED```\
**Content Example**:
```javascript
{
    "data": {
        "member_id": 1,
        "household_id": 1,
        "name": "James Lee",
        "gender": "M",
        "marital_status": "Single",
        "spouse_id": 0,
        "occupation type": "Employed",
        "annual income": 50000.0,
        "date of birth:": "1982-01-01"
    },
    "message": null
}
```
#### 6. Getting a member of a specific id:

**Method**: ```GET```\
**URL** : ```/member/<member_id>```\
**Response**: ```200 OK ```\
**Content Example**:
```javascript
{
    "data": {
        "member_id": 1,
        "household_id": 1,
        "name": "Victoria Lee",
        "gender": "F",
        "marital_status": "Single",
        "spouse_id": 0,
        "occupation type": "Student",
        "annual income": 0.0,
        "date of birth:": "1999-01-01"
    },
    "message": null
}
```
#### 7. Deleting a member of a specific id:

**Method**: ```DELETE```\
**URL** : ```/member/<member_id>```\
**Response**: ```200 OK ```\
**Content Example**:
```javascript
{
    "data": null,
    "message": "Member deleted."
}
```
#### 8. Getting households eligible for the Elder Bonus:

**Method**: ```GET```\
**URL** : ```households/grant?grant=ElderBonus```\
**Response**: ```200 OK ```\
**Content Example**:
```javascript
{
    "data": [
        {
            "household_id": 1,
            "name": "household_1",
            "type": "HDB",
            "members": [
                {
                    "member_id": 1,
                    "household_id": 1,
                    "name": "Ronald Ong",
                    "gender": "M",
                    "marital_status": "Widowed",
                    "spouse_id": 0,
                    "occupation_type": "Employed",
                    "annual_income": 75000.0,
                    "dob:": "1969-06-06"
                },
                {
                    "member_id": 2,
                    "household_id": 1,
                    "name": "Sandra Ong",
                    "gender": "F",
                    "marital_status": "Single",
                    "spouse_id": 0,
                    "occupation_type": "Employed",
                    "annual_income": 45000.0,
                    "dob:": "1995-06-06"
                }
            ]
        }
    ],
    "message": null
}
```
#### 9. Getting households eligible for a user-specified Custom Grant:
**Search Parameters:**
- ```housing_type```= 'HDB'
- ```max_total_income``` = 50,000
- ```max_household_size``` = 2

**Method**: ```GET```\
**URL** : ```households/grant?housing_type=HDB&max_total_income=50000&max_household_size=2&grant=CustomGrant```\
**Response**: ```200 OK ```\
**Content Example**:
```javascript
{
    "data": [
        {
            "household_id": 1,
            "name": "household_1",
            "type": "HDB",
            "members": [
                {
                    "member_id": 3,
                    "household_id": 1,
                    "name": "Quincy Tay",
                    "gender": "M",
                    "marital_status": "Married",
                    "spouse_id": 4,
                    "occupation_type": "Employed",
                    "annual_income": 18000.0,
                    "dob:": "1974-05-01"
                },
                {
                    "member_id": 4,
                    "household_id": 1,
                    "name": "Patricia Tay",
                    "gender": "F",
                    "marital_status": "Married",
                    "spouse_id": 3,
                    "occupation_type": "Employed",
                    "annual_income": 15000.0,
                    "dob:": "1979-03-01"
                }
            ]
        }
    ],
    "message": null
}
```
