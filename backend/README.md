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

1. Rename the file `.env.sample` to `.env`.
2. ⚠️ **IMPORTANT:** After every `git pull develop`, always check for changes in the `.env` file.
3. Navigate to the backend directory:

   ```bash
   cd backend/
   ```
4. Start the containers:

   ```bash
   docker compose up --build
   ```
5. When finished working, stop the containers:

   ```bash
   docker compose down
   ```

> **Note:**
> If something goes wrong when starting the containers, it might mean you forgot to stop them last time.
> Try running `docker compose down` and then start again with `docker compose up --build`.


endpoints for now:

POST http://127.0.0.1:8000/api/v1/pets/ - create pet  
GET http://127.0.0.1:8000/api/v1/pets/ - list all pets  
GET http://127.0.0.1:8000/api/v1/pets/1/ - retrieve pet by id  
DELETE http://127.0.0.1:8000/api/v1/pets/1/  - delete pet by id
PATCH http://127.0.0.1:8000/api/v1/pets/1/  - partial update pet by id












