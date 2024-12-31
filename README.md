# Social Network Application with Flask

This is a simple social network application built using Flask, SQLAlchemy, and Flask-Login. The app allows users to register, log in, post content, and view posts from other users.

## Features:
- **User Authentication**: Users can register, log in, and log out.
- **Post Creation**: Authenticated users can create posts.
- **Recent Posts Feed**: Displays a list of recent posts made by all users.
- **Basic User Profile**: Each user has a basic profile with their posts.

## Technologies Used:
- **Flask**: A micro web framework used to build the application.
- **SQLAlchemy**: An ORM for database interactions, providing a Pythonic way to interact with the database.
- **Flask-Login**: A tool for handling user sessions and authentication.

## Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/social-network-flask.git
   ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3.  Set up the database:
    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```
4.  Run the application
    ```
    flask run
    ```
5.  Open your browser and go to http://127.0.0.1:5000 to start using the app.

## License:
This project is licensed under the MIT License - see the LICENSE file for more details.
