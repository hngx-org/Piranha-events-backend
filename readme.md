# HNG Internship Mobile Application - Team Pinranha

Welcome to the HNG Internship mobile application developed by Team Pinranha! This application serves as an events platform, allowing users to create accounts, organize events, form groups, and participate in various activities within the HNG Internship community.

## Backend Information

The backend of this mobile application is built using Django, a powerful web framework in Python. It provides a solid foundation for managing the application's data, user authentication, and event-related functionalities.

### Functions

1. **Account Management**
   - **Create Account:** Users can create a new account by providing necessary information.
   - **Login:** Registered users can log into their accounts securely.
   - **Logout:** Users can safely log out of their accounts.

2. **Event Management**
   - **Create Events:** Users can create new events, providing event details and inviting others to participate.
   - **Join Events:** Users can join events created by other users within the application.

3. **Group Management**
   - **Create Groups:** Users can create different groups for specific interests or communities.
   - **Add Friends to Groups:** Users can add friends to these groups, enhancing collaboration and interaction.

4. **Event Overview**
   - **General Page:** A dedicated page showcasing all events, enabling users to explore and participate in various activities.

## How to Run the Application

1. Clone the repository:git clone

   ```          https://github.com/TeamPinranha/hng-internship-app.git
   ```

2. Navigate to the project
   ```
   directory:cd hng-internship-app
   ```
   
3. Set up a virtual environment (optional but recommended):python3 -m venv venv4. Activate the virtual environment:
- **Windows:**
  ```
  venv\Scripts\activate
  ```
- **Unix or MacOS:**
  ```
  source venv/bin/activate
  ```

5. Install dependencies:pip install -r requirements.txt6. Run the Django server:python manage.py runserver7. Open the application on your preferred web browser at `http://127.0.0.1:8000/`.

## Contributors

- Team Pinranha: Members who contributed to the development of this application.

Feel free to explore, contribute, and enhance the functionality of this application. If you have any questions or encounter issues, please reach out to the development team. Happy coding!