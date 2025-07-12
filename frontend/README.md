# Adaptable - Pet Adoption Platform (Frontend)

![License](https://img.shields.io/badge/license-MIT-blue.svg)

Welcome to the frontend repository for **Adaptable**, a modern web platform designed to revolutionize the pet adoption process. Our mission is to connect loving homes with animals in need by providing a centralized, user-friendly, and technologically advanced platform for shelters and adopters.

## About The Project

Every year, millions of wonderful, loving animals wait in shelters for a second chance. Adaptable was created to bridge the gap between these pets and potential adopters. We tackle the common frustrations of the adoption journey—like visiting multiple shelters and browsing outdated websites—by creating a single, reliable, and seamless experience.

By leveraging modern technology, including an AI-powered assistant, we make finding and adopting a pet easier and more joyful than ever before.

### Key Features

- **Advanced Pet Catalog:** Browse, search, and filter a comprehensive database of adoptable pets with multiple criteria.
- **AI-Powered Pet Matching:** An intelligent agent (in development) that asks personalized questions to recommend the perfect pet for your lifestyle.
- **User Accounts:** Register and log in to save favorite pets, track appointments, and manage adoption applications.
- **Seamless Application Process:** Apply for adoptions and schedule shelter visits directly through the platform.
- **Collaborative Platform:** A space for shelters to join forces, expand their reach, and find homes for more animals.
- **Community Engagement:** Opportunities for users to get involved, donate, and sign up for newsletters.

### Built With

This project is built with a modern frontend stack, ensuring a fast, scalable, and maintainable application.

- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [React Router](https://reactrouter.com/)
- [SCSS](https://sass-lang.com/)
- [Bulma CSS Framework](https://bulma.io/)

## Getting Started

To get a local copy up and running, please follow these simple steps.

### Prerequisites

Make sure you have Node.js and npm installed on your machine.

- **npm**
  ```sh
  npm install npm@latest -g
  ```

### Installation

1.  **Clone the repository.** If you are part of the main project, you can clone the entire repository. This README is for the `frontend` directory.

2.  **Navigate to the frontend directory.**

    ```sh
    cd frontend
    ```

3.  **Install NPM packages.** This will install all the necessary project dependencies.

    ```sh
    npm install
    ```

4.  **Set up Environment Variables.**
    Create a `.env` file in the root of the `frontend` directory and add the base URL for the backend API.

    ```
    REACT_APP_PET_API_BASE_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
    ```

5.  **Start the development server.**
    This will run the app in development mode.
    ```sh
    npm start
    ```
    Open [http://localhost:3000](http://localhost:3000) to view it in your browser. The page will reload when you make changes.

## Project Structure

The `src` folder is organized to maintain a clean and scalable codebase:

- **/api**: Contains all functions related to making API calls to the backend.
- **/app**: Includes the Redux store configuration and hooks.
- **/components**: Reusable React components used throughout the application (e.g., `Header`, `Footer`, `Modal`).
- **/features**: Redux slices for managing different parts of the application state (e.g., `authentication`, `pets`).
- **/modules**: Major application pages/routes (e.g., `HomePage`, `CatalogPage`, `AccountPage`).
- **/styles**: Global styles, variables, and mixins using SCSS.
- **/types**: TypeScript type definitions and interfaces for data structures.
- **/utils**: Helper functions and utilities.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/your_username/your_repository](https://github.com/your_username/your_repository)
