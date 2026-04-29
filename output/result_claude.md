# Generated API Documentation from Source Code

**Source file:** `todo.py`

---

## Overview

This API provides a simple interface for managing todo items. It supports creating, retrieving, and deleting todo entries through standard RESTful HTTP endpoints.

**Base URL:** `/todos`
**Response Format:** JSON

---

## Endpoints

---

### 1. Get All Todos

| Property | Details |
|----------|---------|
| **Method** | `GET` |
| **Path** | `/todos` |
| **Function** | `get_todos` |

#### Description
Returns a list of all todo items currently stored.

#### Parameters
> No path or query parameters required.

#### Request Body
> Not applicable.

#### Response

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully returns a JSON array of all todo items |

#### Example Response
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "completed": false
  },
  {
    "id": 2,
    "title": "Write documentation",
    "completed": true
  }
]
```

#### Usage Note
> Use this endpoint to fetch the full list of todos. An empty array `[]` is returned if no items exist.

---

### 2. Create a Todo

| Property | Details |
|----------|---------|
| **Method** | `POST` |
| **Path** | `/todos` |
| **Function** | `create_todo` |

#### Description
Creates a new todo item with a title and a completed status.

#### Parameters
> No path parameters required.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | ✅ Yes | The title or description of the todo item |
| `completed` | `boolean` | ✅ Yes | The completion status of the todo item |

#### Example Request Body
```json
{
  "title": "Buy groceries",
  "completed": false
}
```

#### Response

| Status Code | Description |
|-------------|-------------|
| `201 Created` | Todo item was successfully created; returns the new item |
| `400 Bad Request` | Invalid or missing fields in the request body |

#### Example Response
```json
{
  "id": 3,
  "title": "Buy groceries",
  "completed": false
}
```

#### Usage Note
> Ensure the `Content-Type` header is set to `application/json` when sending the request body.

---

### 3. Get a Todo by ID

| Property | Details |
|----------|---------|
| **Method** | `GET` |
| **Path** | `/todos/<int:todo_id>` |
| **Function** | `get_todo_by_id` |

#### Description
Returns a single todo item identified by its unique integer ID.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `todo_id` | `integer` | ✅ Yes | The unique identifier of the todo item |

#### Request Body
> Not applicable.

#### Response

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully returns the requested todo item as a JSON object |
| `404 Not Found` | No todo item found with the given `todo_id` |

#### Example Response
```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false
}
```

#### Usage Note
> The `todo_id` must be a valid integer. Passing a non-integer value will result in a routing error.

---

### 4. Delete a Todo

| Property | Details |
|----------|---------|
| **Method** | `DELETE` |
| **Path** | `/todos/<int:todo_id>` |
| **Function** | `delete_todo` |

#### Description
Permanently deletes a todo item identified by its unique integer ID.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `todo_id` | `integer` | ✅ Yes | The unique identifier of the todo item to delete |

#### Request Body
> Not applicable.

#### Response

| Status Code | Description |
|-------------|-------------|
| `200 OK` / `204 No Content` | Todo item was successfully deleted |
| `404 Not Found` | No todo item found with the given `todo_id` |

#### Usage Note
> This action is **irreversible**. Once deleted, a todo item cannot be recovered. Confirm the correct `todo_id` before sending this request.

---

## Summary Table

| Method | Path | Function | Description |
|--------|------|----------|-------------|
| `GET` | `/todos` | `get_todos` | Retrieve all todo items |
| `POST` | `/todos` | `create_todo` | Create a new todo item |
| `GET` | `/todos/<int:todo_id>` | `get_todo_by_id` | Retrieve a single todo by ID |
| `DELETE` | `/todos/<int:todo_id>` | `delete_todo` | Delete a todo item by ID |

---

*Documentation generated from source file: `todo.py`*