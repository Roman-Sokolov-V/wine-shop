# wine-shop

Setup

`cd backend/`  
`python -m venv venv`  
`venv\scripts\activate`  Windows  
`source venv/scripts/activate` Mac  
`source venv/bin/activate` Linux  
`poetry install`  
`python manage.py makemigrations`  
`python manage.py migrate`  
`python manage.py runserver`

endpoints for now:

POST http://127.0.0.1:8000/api/v1/pets/ - create pet  
GET http://127.0.0.1:8000/api/v1/pets/ - list all pets  
GET http://127.0.0.1:8000/api/v1/pets/1/ - retrieve pet by id  
DELETE http://127.0.0.1:8000/api/v1/pets/1/  - delete pet by id
PATCH http://127.0.0.1:8000/api/v1/pets/1/  - partial update pet by id

