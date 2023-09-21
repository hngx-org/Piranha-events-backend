<!-- ## Group Membership Management

### Add User to Group

**Endpoint:** `groups/<int:groupId>/members/<int:userId>`
**Method:** POST
**Description:** Adds a user to a group.

### Remove User from Group

**Endpoint:** `groups/<int:groupId>/members/<int:userId>`
**Method:** DELETE
**Description:** Removes a user from a group.

### List Group Members

**Endpoint:** `groups/<int:groupId>/members/`
**Method:** GET
**Description:** Lists all members of a group.

Each endpoint requires the group ID and, for adding/removing a user, the user ID. The group and user IDs should be replaced with the actual IDs in the URL.
 -->


## Events App API Documentation

### Installation

### To set up the Events app API, follow these steps:
**Clone the repository:**

    ```bash

        git clone <repository_url>
        cd <repository_directory>
    ```

**Create a virtual environment:**

    ```bash

    python3 -m venv venv
    ```

**Activate the virtual environment:**

    ```sh
        Linux: source venv/bin/activate   
        
        Windows: source venv\Scripts\activate
    ```

**Install dependencies:**

    ```bash

    pip install -r requirements.txt
    ```

**Run migrations:**

    ```bash

    python manage.py migrate
    ```
**Start the Django server:**

    ```bash

    python manage.py runserver
    ```

### The API should now be running at http://localhost:8000/.




# Events Endpoints

### List Events
- Endpoint: https://team-piranha.onrender.com/api/events/

- Method: GET

- Description: Returns a list of events.
- Example
    ```
    bash

    curl -X GET https://team-piranha.onrender.com/api/events/
    ```

### Create Event

**Endpoint: https://team-piranha.onrender.com/api/events/**

**Method: POST**

**Parameters:**

- title (string): Event title
- description (string): Event description
- location (string): Event location
- start_date (string): Event start date (YYYY-MM-DD)
- end_date (string): Event end date (YYYY-MM-DD)
- start_time (string): Event start time (HH:MM:SS)
- end_time (string): Event end time (HH:MM:SS)
- creator_id (integer): Creator's ID

**Description: Saves the event to the database.**
- Example
- 
    ```bash

    curl -X POST https://team-piranha.onrender.com/api/events/ -d "title=Sample Event" -d "description=This is a sample event" -d "location=Sample Location" -d "start_date=2023-09-21" -d "end_date=2023-09-22" -d "start_time=10:00:00" -d "end_time=12:00:00" -d "creator_id=1"
    ```