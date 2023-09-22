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
#### Clone the repository:

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
    
    Windows: venv\Scripts\activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
             OR
pip freeze > requirements.txt            
```

**Run migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Start the Django server:**

```bash
python manage.py runserver
```

### The API should now be running at http://localhost:8000/.


# Login User to the app

### Login User

- Endpoint: https://team-piranha.onrender.com/api/login/
- Method: POST
- Description: Logs a user in to the event app.

- Parameters:
- Email: string
- pass_id: string

# Events Endpoints

### List Events
- Endpoint: https://team-piranha.onrender.com/api/events/

- Method: GET

- Description: Returns a list of events.
- Example

```bash

  curl -X GET https://team-piranha.onrender.com/api/events/
```

### Create Event

**Endpoint: https://team-piranha.onrender.com/api/event/**

**Method: POST**

**Description: Saves the event to the database.**

**Parameters:**

- title (string): Event title
- description (string): Event description
- location (string): Event location
- start_date (string): Event start date (YYYY-MM-DD)
- end_date (string): Event end date (YYYY-MM-DD)
- start_time (string): Event start time (HH:MM:SS)
- end_time (string): Event end time (HH:MM:SS)
- creator_id (integer): Creator's ID

**Example**
  
```bash

curl -X POST https://team-piranha.onrender.com/api/events/ -d "title=Sample Event" -d "description=This is a sample event" -d "location=Sample Location" -d "start_date=2023-09-21" -d "end_date=2023-09-22" -d "start_time=10:00:00" -d "end_time=12:00:00" -d "creator_id=1"
```

### Get user event

**Endpoint: https://team-piranha.onrender.com/api/event/user/{id}**

**Method: GET**

**Description: Get an event posted by a user**

**Parameters:**

- None

**Example**
  
```bash

curl -X 'GET' \'https://team-piranha.onrender.com/api/event/user/1/' 
```

### Get a particular event

**Endpoint: https://team-piranha.onrender.com/api/event/{id}**

**Method: GET**

**Description: Get a saved event by ID**

**Parameters:**

- None

**Example**
  
```bash

curl -X 'GET' \'https://team-piranha.onrender.com/api/event/1/' 
```


## INTERESTED EVENTS
### Add interested event

**Endpoint: https://team-piranha.onrender.com/api/interested_event/**

**Method: POST**

**Description: Saves an interested event to the database.**

**Parameters:**

- user_id: interger
- event_id: interger

**Example**
  
```bash

curl -X 'POST' \'https://team-piranha.onrender.com/api/interested_event/'
```

### Saves a user interested event

**Endpoint: https://team-piranha.onrender.com/api/interested_event/accept/{id}**

**Method: POST**

**Description: Saves an event the user has accepted**

**Parameters:**

- user_id: interger
- event_id: interger
- id: A unique integer value identifying this interested event.


**Example**
  
```bash

curl -X 'POST' \'https://team-piranha.onrender.com/api/interested_event/accept/2/
```


### Gets interested event

**Endpoint: https://team-piranha.onrender.com/api/interested_event/event/{id}**

**Method: GET**

**Description: Gets an event the user has accepted**

**Parameters:**

- None

**Example**
  
```bash

curl -X 'GET' 'https://team-piranha.onrender.com/api/interested_event/event/2/'
```


### Delete interested event

**Endpoint: https://team-piranha.onrender.com/api/interested_event/{id}**

**Method: DELETE**

**Description: Deletes an interested event from the database**

**Parameters:**

- None

**Example**
  
```bash

curl -X 'DELETE' 'https://team-piranha.onrender.com/api/interested_event/1/' 
```






















# Groups Endpoints

### Create Group

- **Endpoint:** `https://team-piranha.onrender.com/api/groups/`

- **Method:** POST

- **Description:** *Creates a new group and saves it to the database.*

- **Parameters:**

  - `title` (string): The title of the group.
  - `description` (string): A brief description of the group.
  - `location` (string): The location or meeting place of the group.
  - `creator_id` (integer): The ID of the user creating the group.

- **Example:**
  ```bash
  curl -X POST `https://team-piranha.onrender.com/api/groups/` \
    -d "title=Sample Group" \
    -d "description=This is a sample group" \
    -d "location=Sample Location" \
    -d "creator_id=1"
  ```

### List Groups

- **Endpoints:** `https://team-piranha.onrender.com/api/groups/`

- **Method:** GET

- **Description:** *Returns a list of groups.*

- **Example:**
```bash
curl -X GET `https://team-piranha.onrender.com/api/groups/`
```

### Get Specific Group

- **Endpoint:** `https://team-piranha.onrender.com/api/groups/<int:pk>/`

- **Method:** GET

- **Description:** *Retrieves details of a specific group.*

- **Example:**
```bash
curl -X GET `https://team-piranha.onrender.com/api/groups/1/`
```

### Update Group
- **Endpoint:** `https://team-piranha.onrender.com/api/groups/<int:pk>/update/`

- **Method:** PUT

- **Description:** *Updates group details.*

- **Example:**
```bash
curl -X PUT https://team-piranha.onrender.com/api/groups/1/update/ \
  -d "title=Updated Group Title" \
  -d "description=Updated group description"
```

### Delete Group
- **Endpoint:** `https://team-piranha.onrender.com/api/groups/<int:pk>/delete/`

- **Method:** DELETE

- **Description:** *Deletes a group.*

- **Example:**
```bash
curl -X DELETE https://team-piranha.onrender.com/api/groups/1/delete/
```

### Add User to Group
- **Endpoint:** `https://team-piranha.onrender.com/api/groups/<int:groupId>/members/<int:userId>/`

- **Method:** POST

- **Description:** *Adds a user to a group.*

- **Example:**
```bash
curl -X POST https://team-piranha.onrender.com/api/groups/1/members/2/
```

### Remove User from Group
- **Endpoint:** `https://team-piranha.onrender.com/api/groups/<int:groupId>/members/<int:userId>/remove/`

- **Method:** DELETE

- **Description:** *Removes a user from a group.*

- **Example:**
```bash
curl -X DELETE https://team-piranha.onrender.com/api/groups/1/members/2/remove/
```

### Group Members List
- **Endpoint:** `https://team-piranha.onrender.com/api/groups/<int:groupId>/members/list/`

- **Method:** GET

- **Description:** *Retrieves a list of members in a group.*

- **Example:**
```bash
curl -X GET https://team-piranha.onrender.com/api/groups/1/members/list/
```

*Each endpoint requires the group ID and, for adding/removing a user, the user ID. The group and user IDs should be replaced with the actual IDs in the URL.*


# Login Endpoint

*This documentation provides details about the "Login" endpoint in our project. The login endpoint allows users to authenticate and obtain a token for access.*

- **Endpoint:** `https://team-piranha.onrender.com/api/login`

- **Method:** POST

- **Description:** *Authenticates a user and provides an access token for authorization.*

- **Parameters:** *To authenticate and obtain a token, you need to provide the following parameters:*

- `email` (string): The user's email address.
- `pass_id` (string): The user's password or identifier for authentication.

**Example**

*To authenticate and obtain a token, you can make a POST request as follows:*

```bash
Copy code
curl -X POST https://team-piranha.onrender.com/api/login/ \

  -d "email=user@example.com" \
  -d "pass_id=yourpassword123"
```

### Response:

*** Upon a successful login, the API will respond with a JSON object containing the access token and user information. The response may look something like this:***

**JSON**

```bash
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "token": "your-access-token",
    "id": 1,
    "name": "John Doe",
    "email": "user@example.com",
    "avatar": "https://team-piranha.onrender.com/api/media/profile.jpg"
  }
}
```

**The response includes the following information:**

- `token`: The access token for authorization.
- `id`: The user's unique identifier.
- `name`: The user's name.
- `email`: The user's email address.
- `avatar`: The URL to the user's avatar image, if available.

*This token can be used for subsequent requests to access protected endpoints that require authentication.*