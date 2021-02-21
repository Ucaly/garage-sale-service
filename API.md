# API Reference

This API reference is organized by endpoints.

---
## Get all saleitems per page

Returns all saleitems.

**URL** : `/saleitems`

**Method** : `GET`

**Request parameters**
- None

**Success responses**

- `200 OK`
- `404 not found`: No saleitem found.

**Response body**
- `saleitems`: List of saleitems.
- `total_saleitems`: Total number of saleitems

**Response sample**

```bash
curl http://127.0.0.1:5000/saleitems
```

```json
{
  "saleitems": [
    {
      "added_at": "Sun, 07 Feb 2021 15:05:07 GMT", 
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", 
      "id": 1, 
      "image": "https://homepages.cae.wisc.edu/~ece533/images/airplane.png", 
      "name": "Airplane model", 
      "price": 50.0, 
      "status": "Pending"
    }, 
    {
      "added_at": "Sun, 07 Feb 2021 15:32:48 GMT", 
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", 
      "id": 6, 
      "image": "https://homepages.cae.wisc.edu/~ece533/images/boat.png", 
      "name": "Classic boat", 
      "price": 150.0, 
      "status": "Available"
    }
], 
  "success": true, 
  "total_saleitems": 17
}

```
---
## Get single saleitem by id

Returns a saleitem by id.  404 if not found.

**URL** : `/saleitems/<int:saleitem_id>`

**Method** : `GET`

**Request parameters**
- `/saleitem_id`: URI parameter. An integer representing a saleitem id. *Required*

**Success responses**
- `200 OK`
- `404 not found`

**Response body** :
- `item`: A single sale item
- `buyers`: A list of users who want to buy
- `total_buyers`: Total number of buyers

**Response sample**

```bash
curl http://127.0.0.1:5000/saleitems/22
```

```json
{
  "buyers": [], 
  "item": {
    "added_at": "Mon, 15 Feb 2021 15:24:17 GMT", 
    "description": "This is a test item and price is 200", 
    "id": 22, 
    "image": "https://picsum.photos/400/600", 
    "name": "Test item 1", 
    "price": 200.0, 
    "status": "Available"
  }, 
  "success": true, 
  "total_buyers": 0
}

```

---
## Create new sale item

Create a new sale item and add to database

**URL** : `/saleitems`

**Method** : `POST`

**Request body**
- `name`: string *Required*
- `price`: string *Required*
- `image`: string 
- `description`: string

**Success responses**
- `200 OK`

**Response body**
- `created`: id of the new question
- `saleitems`: updated list of sale items
- `total_saleitems`: the number of all sale items

**Response sample**

```bash
curl -X POST http://127.0.0.1:5000/saleitems -H 'Content-Type: application/json' -d '{"name":"Fireking blue mug", "price":"15", "image":"https://www.image.com/image-145", "description":"Rare find! Good condition."}'
```

```json
{
  "saleitems": [    
    {
      "added_at": "Mon, 15 Feb 2021 15:24:17 GMT", 
      "description": "This is a test item and price is 200", 
      "id": 22, 
      "image": "https://picsum.photos/400/600", 
      "name": "Test item 1", 
      "price": 200.0, 
      "status": "Available"
    }, 
    {
      "added_at": "Sun, 21 Feb 2021 10:59:08 GMT", 
      "description": "Rare find! Good condition.", 
      "id": 23, 
      "image": "https://www.image.com/image-145", 
      "name": "Fireking blue mug", 
      "price": 15.0, 
      "status": "Available"
    }
  ], 
  "success": true, 
  "total_saleitems": 18
}
```

---
## Delete a sale item

Deletes single sale item from database

**URL** : `/saleitems/<int:saleitem_id>`

**Method** : `DELETE`

**Request parameters**
- `/saleitem_id`: URI parameter. An integer representing a sale item id. *Required*

**Success responses**
- `200 OK`

**Response body** :
- `deleted`: Id of deleted sale item

**Response sample**

```bash
curl -X DELETE http://127.0.0.1:5000/saleitems/2
```

```json
{
  "deleted": 2, 
  "success": true
}
```

---
## Update a sale item

Updates single sale item from database

**URL** : `/saleitems/<int:saleitem_id>`

**Method** : `PATCH`

**Request parameters**
- `/saleitem_id`: URI parameter. An integer representing a sale item id. *Required*

**Success responses**
- `200 OK`

**Response body** :
- `updated`: Id of updated sale item

**Response sample**

```bash
curl -X PATCH http://127.0.0.1:5000/saleitems/2
```

```json
{
  "updated": 2, 
  "success": true
}
```
---
## Buy a sale item

Buys a single sale item

**URL** : `/saleitems/<int:saleitem_id>/buy`

**Method** : `POST`

**Request parameters**
- `/saleitem_id`: URI parameter. An integer representing a sale item id. *Required*

**Request body**
- `user_id`: int *Required*

**Success responses**
- `200 OK`

**Response body** :
- `updated_saleitem_id`: Id of updated sale item

**Response sample**

```bash
curl -X POST http://127.0.0.1:5000/saleitems/2/buy -H 'Content-Typpe: application/json' -d '{"user_id": 2}'
```

```json
{
  "updated_saleitem_id": 2, 
  "success": true
}
```

## Get all users

Fetches a dictionary of users

**URL** : `/users`

**Method** : `GET`

**Success responses**
- `200 OK`

**Response body**
- `users`: list of users
- `total_users`: total number of users

**Response sample**

```bash
curl http://127.0.0.1:5000/users
```

```json
{
  "success": true, 
  "total_users": 7, 
  "users": [
    {
      "email": "yukarim777@gmail.com", 
      "id": 1, 
      "name": "yukarim777@gmail.com", 
      "nickname": "yukapon"
    }, 
    {
      "email": "tester1@mail.com", 
      "id": 3, 
      "name": "Test user 1", 
      "nickname": "tester1"
    }, 
    {
      "email": "yukarim777@hotmail.com", 
      "id": 4, 
      "name": "yukarim777@hotmail.com", 
      "nickname": "yukarim777"
    }, 
    {
      "email": "tester2@email.com", 
      "id": 5, 
      "name": "tester2", 
      "nickname": "Tester 2"
    }, 
    {
      "email": "tester3@email.com", 
      "id": 6, 
      "name": "tester3", 
      "nickname": "Tester 3"
    }, 
    {
      "email": "tester4@email.com", 
      "id": 7, 
      "name": "tester4", 
      "nickname": "Tester 4"
    }, 
    {
      "email": "tester5@email.com", 
      "id": 8, 
      "name": "tester5", 
      "nickname": "Tester 5"
    }
  ]
}

```

---
## Get a single user by id

Returns a user.

**URL** : `/users/<int:user_id>`

**Method** : `GET`

**Request parameters**
- `/user_id`: URI parameter. An integer representing a user id. *Required*

**Success Responses**
- `200 OK`

**Response body**
- `user`: A user
- `items`: List of sale items this user buy

**Response sample**

```bash
curl http://127.0.0.1:5000/users/3
```

```json
{
  "items": [], 
  "success": true, 
  "user": {
    "email": "tester1@mail.com", 
    "id": 3, 
    "name": "Test user 1", 
    "nickname": "tester1"
  }
}
```

---
## Update a single user by id

Updates a user.

**URL** : `/users/<int:user_id>`

**Method** : `PATCH`

**Request parameters**
- `/user_id`: URI parameter. An integer representing a user id. *Required*

**Request body**
- `name`: string
- `nickname`: string
- `email`: string

**Success Responses**
- `200 OK`

**Response body**
- `updated`: Updated user id

**Response sample**

```bash
curl -X PATCH http://127.0.0.1:5000/users/6 -H 'Content-Type: application/json' -d '{"nickname": "starlight"}'
```

```json
{
  "success": true, 
  "updated": 6
}
```
---
## Delete a single user by id

Returns a user.

**URL** : `/users/<int:user_id>`

**Method** : `DELETE`

**Request parameters**
- `/user_id`: URI parameter. An integer representing a user id. *Required*

**Success Responses**
- `200 OK`

**Response body**
- `deleted`: Deleted user id

**Response sample**

```bash
curl -X DELETE http://127.0.0.1:5000/users/6
```

```json
{
    "success": true,
    "deleted": 6
}
```

---
## Add a new user

Adds a new user and returns the added user.  If email already exists, just returns the user.

**URL** : `/users`

**Method** : `POST`

**Request body**
- `name`: Name of user *Required*
- `nickname`: Nickname of user *Required*
- `email`: email address *Required*

**Success responses**
- `200 OK`

**Response body** :
- `user`: Newly added user or existing user if the user email is found

**Response sample**

```bash
curl -X POST http://127.0.0.1:5000/users -H 'Content-Type: application/json' -d '{"name":"Kate Summer", "nickname":"kat", "email":"katesummer@email.com"}'
```

```json
{
  "success": true, 
  "user": {
    "email": "katesummer@email.com", 
    "id": 9, 
    "name": "Kate Summer", 
    "nickname": "kat"
  }
}

```

