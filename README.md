# 🐾 Animal Shelter Website

## 🌟 Overview

A full-stack web application for animal shelter management and pet adoption. This project enables 
shelters to manage pets, process adoptions, and connect loving animals with new families. It features
a modern React frontend and a Django backend, all containerized with Docker for easy deployment.

### Key Goals
- **Connect Animals with Families**: Help homeless animals find loving homes
- **Streamline Adoption Process**: Simplify the adoption workflow for both shelters and adopters
- **Increase Shelter Support**: Provide easy ways for people to donate and volunteer
- **Educate the Community**: Share information about animal care and welfare

## ✨ Features

### For Visitors/Adopters
- 🔍 **Browse Available Pets**: Search and filter animals by type, age, size, and characteristics
- 📱 **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- 💝 **Adoption Applications**: Submit adoption requests online
- 💰 **Donation System**: Support the shelter through secure online donations
- 📚 **Educational Content**: Learn about pet care, training, and animal welfare
- 📧 **Contact Integration**: Easy communication with shelter staff

### For Shelter Staff
- 🏥 **Pet Management**: Add, update, and list pets available for adoption, including multiple photos.
- 📋 **Adoption Applications:** Submit and review detailed adoption forms online.
- 📝 **Content Management**: Update shelter information and news
- 👥 **User Management**: Register, login, and manage user accounts with authentication.
- **Admin Panel:** Manage users, pets, and adoption requests via a secure admin interface.
- **Donation Support:** Information for donations and QR code for fast support.
- **API Documentation:** Swagger and Redoc docs for all backend endpoints.
- **Helpful Information:** Educational resources on why to adopt, how to help, and support for animal welfare partners.

## Technologies Used

- **Frontend:** React, TypeScript, Bulma, SCSS
- **Backend:** Django, Django REST Framework, Celery, Celery-beat, Redis, Docker
- **Database:** (Configured in Docker, e.g., PostgreSQL)
- **Mail Service:** Configurable via Mailtrap for development/testing
- **Other:** Docker Compose for local development

### Additional Tools
- **API Testing**: Postman
- **Version Control**: Git
- **Deployment**: Docker + AWS(E2C) /github.io
- **CI/CD**: GitHub Actions (for beckend)


## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed

### Backend Setup

1. Rename `.env.sample` to `.env` and configure environment variables as needed.
2. From project root, navigate to backend directory:
    ```bash
    cd backend/
    ```
3. Build and start backend services:
    ```bash
    docker compose up --build
    ```
4. (If needed, stop with `docker compose down`)
5. Create a superuser for admin access:
    ```bash
    docker compose exec shelter python manage.py createsuperuser
    ```
6. Access the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

#### API Documentation

- Swagger UI: [http://127.0.0.1:8000/api/v1/swagger/](http://127.0.0.1:8000/api/v1/swagger/)
- Redoc: [http://127.0.0.1:8000/api/v1/redoc/](http://127.0.0.1:8000/api/v1/redoc/)

#### Mail Service

- Register at [Mailtrap](https://mailtrap.io/) for email testing.
- Edit `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `backend/config/settings/dev.py` with Mailtrap credentials.

#### Database Management

- Save DB to file:
    ```bash
    docker exec shelter python manage.py dumpdata > file_name.json
    ```
- Load DB from file:
    ```bash
    docker exec shelter python manage.py loaddata file_name.json
    ```

### Frontend Setup

1. From project root, go to frontend directory:
    ```bash
    cd frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start local server:
    ```bash
    npm start
    ```
4. Visit `http://localhost:3000` in your browser.

## Example API Endpoints

- `POST /api/v1/pets/` — Create a pet (with photo upload)
- `GET /api/v1/pets/` — List all pets with filters
- `GET /api/v1/pets/<id>/` — Retrieve pet by ID
- `POST /api/v1/users/` — Register user
- `POST /api/v1/users/login/` — Login user (returns token)
- `POST /api/v1/adoption/adoption_form/` — Submit adoption form (auth required)

For a full list, see Swagger/Redoc docs above.

## Why Adopt?

Adopting saves lives, supports animal welfare, and is often more cost-effective than buying from breeders. Many shelter pets are well-socialized and ready for a loving home.

## How to Help

- **Adopt:** Give a pet a second chance.
- **Donate:** Your support helps provide food, medical care, and shelter.
- **Volunteer:** Contact us to learn about volunteering opportunities.
- **Share:** Spread the word about our cause.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Repository:** [github.com/Roman-Sokolov-V/wine-shop](https://github.com/Roman-Sokolov-V/wine-shop)


A comprehensive web application for animal shelters that allows users to browse adoptable pets, learn about animals, and support the shelter through donations and adoptions.


## 🔮 Future Enhancements

- [ ] Mobile app development
- [ ] Integration with social media platforms
- [ ] Advanced matching algorithm for pets and adopters
- [ ] Volunteer management system
- [ ] Multi-language support
- [ ] Real-time chat system


## 📧 Contact

For questions, suggestions, or support, please contact:

- **Project Maintainer (frontend)**: Sviatoslav Podolskyi
- **Email**: [your-email@example.com]
- **GitHub**: 


- **Project Maintainer (backend)**: Roman Sokolov
- **Email**: [gnonasis@gmail.com]
- **GitHub**: [@Roman-Sokolov-V](https://github.com/Roman-Sokolov-V)


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All the volunteers and staff who help animals find loving homes
- The open-source community for providing excellent tools and libraries
- Animal welfare organizations for their dedication to helping animals in need

---

**Made with ❤️ for animals in need**

*Every adoption saves a life and makes room for another rescue. Thank you for supporting animal welfare!*