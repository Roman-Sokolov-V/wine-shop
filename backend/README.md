# Pet Shelter

## Setup with Docker (recommended)

### Install Docker

#### For Windows:
1. Visit the official Docker documentation:  
   [https://docs.docker.com/desktop/setup/install/windows-install/](https://docs.docker.com/desktop/setup/install/windows-install/)
2. Download the appropriate installer for your PC.
3. Install Docker on your system.
4. Verify the installation by running the following command:  
   ```bash
   docker --version


If Docker is installed correctly, you’ll see something like:

```
Docker version 24.8.6, build ...
```

### Run the Backend in Docker

~~1. Rename the file `.env.sample` to `.env`.~~  
~~2. ⚠️ **IMPORTANT:** After every `git pull develop`, always check for changes in the `.env` file.~~  
3. Navigate to the backend directory:
~~
   ```bash
   cd backend/
   ```
4. Start the containers:

~~docker compose up --build~~
```  bash
   python run.py
```
5. When finished working, stop the containers:

   ```bash
   docker compose down
   ```
> **Note:**
> If something goes wrong when starting the containers, it might mean you forgot to stop them last time.
> Try running `docker compose down` and then start again with `docker compose up --build`.
6. Create a superuser who will have access to the panel administrative
  ```bash
   docker compose exec shelter python manage.py createsuperuser
```
Admin panel  http://127.0.0.1:8000/admin/


## Documentation
Swagger:
http://127.0.0.1:8000/api/v1/swagger/  
Redoc: 
http://127.0.0.1:8000/api/v1/redoc/ 

endpoints for now:

POST http://127.0.0.1:8000/api/v1/pets/ - create pet, also available upload several photos in mode form-data with keys "images"

GET http://127.0.0.1:8000/api/v1/pets/ - list all pets - filters available  
GET http://127.0.0.1:8000/api/v1/pets/id/ - retrieve pet by id  
DELETE http://127.0.0.1:8000/api/v1/pets/id/  - delete pet by id (staff only)  
PATCH http://127.0.0.1:8000/api/v1/pets/id/  - partial update pet by id (staff only)

POST http://127.0.0.1:8000/api/v1/pets/upload/ - add photo no pet - multipart/formdata (staff only)
GET http://127.0.0.1:8000/api/v1/pets/upload/ - list all pets photo (staff only)


POST http://127.0.0.1:8000/api/v1/users/ - create (register) user  
POST http://127.0.0.1:8000/api/v1/users/login/ - login user - create and return token  
POST http://127.0.0.1:8000/api/v1/users/logout/ - logout user - delete token (authentification needed)  


GET http://127.0.0.1:8000/api/v1/users/ - list all users (staff only)   
GET http://127.0.0.1:8000/api/v1/users/id/ - retrieve user by id (request.user or staff)  
PATCH http://127.0.0.1:8000/api/v1/users/id/ - partial update user by id (request.user or staff)  
PUT http://127.0.0.1:8000/api/v1/users/id/ - Update user by id (request.user or staff)  
DELETE http://127.0.0.1:8000/api/v1/users/id/ - delete user by id (staff only)  



## Mail service
Sign Up https://mailtrap.io and select Sandbox  
Open Settings by backend/config/settings/dev.py  
Find Section # Mail conf  
Edit EMAIL_HOST_USER and EMAIL_HOST_PASSWORD values provided by Mailtrap service when registering

### Save data from db to file
docker exec shelter python manage.py dumpdata > file_name.json

### Load db with data from file
docker exec shelter python manage.py loaddata file_name.json