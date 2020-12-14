# Government Grant Disbursement API #

This is a RESTful API which allows users to decide which group(s) of households are eligible for various government grants.

*Note that all grants mentioned here are fictitious and do not reflect actual grants that are being worked on or implemented by any government ministries.*

## Installation ##

The API is built using Python and Flask (using Flask-SQLAlchemy as the ORM), and requires the following libraries:

```
pip install Flask
pip install Flask-RESTful
pip install Flask-SQLAlchemy
```

## Running the Application ##

The application uses SQLite3, a lightweight disk-based database which does not require additional start-up steps. Once the application is executed, a database file ```database.db``` will automatically be created. Subsequent use of the application will read from/write to this database file. Start the application by running the following command:

```
python app.py
```

## Available Endpoints

The following endpoints allow objects, namely Households and Members, to be manipulated upon requests:

Markup : - Show all households : code(GET /households)
Markup : - Create a household : code(POST /households)
Markup : - Show household of specific id: code(GET /household/<string:id>)
Markup : - Update household of specific id: code(PUT /household/<string:id>)
Markup : - Delete household of specific id: code(DELETE /household/<string:id>)
Markup : - Show all members: code(GET /members)
Markup : - Create a member: code(POST /members)
Markup : - Show member of specific id: code(GET /member/<string:id>)
Markup : - Update member of specific id: code(PUT /member/<string:id>)
Markup : - Delete member of specific id: code(DELETE /member/<string:id>)       
Markup : - Show all households eligible for a selected grant: code(GET /households/grant?grant=<string:id>)

## API Responses



## Assumptions
