## Group Membership Management

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
