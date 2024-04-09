
# Drew's Web Portal

This project is a web portal built using Vue.js for the frontend and Node.js for the backend. It provides features for user registration, login, and profile management.


## Features

- **User Registration**: Allows users to register by providing their name, email, password, and optional phone number.
- **Email Confirmation**: Once registered, users will receive a welcome and confirmation email.
- **Login**: Users can log in using their email and password.
- **Profile Management**: Once logged in, users can manage their profile information.


## Project Structure
The project consists of two main parts:

1. **Frontend**: Built using Vue.js, the frontend provides the user interface for registration, login, and profile management.
   - Componenet files: `LoginForm.vue`, `RegistrationForm.vue`, `Profile.vue` 
   - Main file: `ProfileApp.vue`
   - Assets: Images, logos, etc.

2. **Backend**: Built using Node.js, the backend handles user authentication and data storage.
   - Flask and SQL logic: `app.py`
   - Integration files: `main.js`, `index.html`
   - Database: SQLite
   - API Endpoints: `/register`, `/login`, `/profile`, `logout`
## Run Locally

Clone the project

```bash
  git clone https://github.com/dmutchnik/Drews-Web-Portal.git
```

Go to the project directory

```bash
  cd Drews-Web-Portal
```

Install dependencies

```bash
  npm install
```

Start the flask server

```bash
  flask start
```

Start the frontend server and access web portal

```bash
  npm run dev
  o
```
## Tech Stack

- **Frontend**:
- Vue.js
- Axios and Fetch for HTTP requests
- Vue Router for routing
- Pixabay API for image selection
- SCSS for styling

- **Backend**:
- Flask
- Mandrill API for emailing
- SQLite for database
- CORS for handling requests from Frontend
- Bcrypt password encryption


## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any enhancements or bug fixes.


## License

This project is licensed under the MIT License - see the [MIT](https://choosealicense.com/licenses/mit/) file for details.

