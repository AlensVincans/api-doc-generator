# Generated API Documentation from Source Code  
**Source file:** `todo.py`

---

## Endpoint: List All Todos

**Function name:** `get_todos`  
**HTTP method:** `GET`  
**Path:** `/todos`

**Description:**  
Returns a list of all todo items.

**Parameters:**  
None in the path or query as indicated by the source snippet.

**Request body:**  
Not applicable for this endpoint.

**Response:**  
- **200 OK** – JSON array of todo objects.  
  - Each todo is expected to contain at least:
    - `id` (integer) – Unique identifier of the todo item.
    - `title` (string) – Title or description of the todo.
    - `completed` (boolean) – Completion status of the todo.

**Usage note:**  
Use this endpoint to retrieve the full list of todos, for example to display them in a UI or to perform bulk operations client-side.

---

## Endpoint: Create a New Todo

**Function name:** `create_todo`  
**HTTP method:** `POST`  
**Path:** `/todos`

**Description:**  
Creates a new todo item with a title and completed status.

**Parameters:**  
None in the path or query.

**Request body:**  
JSON object with the following fields:

- `title` (string, required) – Title of the todo item.  
- `completed` (boolean, optional) – Initial completion status.  
  - If not specified, typical implementations default this to `false` (not guaranteed from the snippet but common practice).

**Example request body:**
```json
{
  "title": "Buy groceries",
  "completed": false
}
```

**Response:**  
- **201 Created** – JSON object representing the created todo item, including its generated `id`.  
- **400 Bad Request** – If required fields (such as `title`) are missing or invalid.

**Usage note:**  
Call this endpoint when you need to add a new todo item. Ensure you send `Content-Type: application/json` with the request.

---

## Endpoint: Get Todo by ID

**Function name:** `get_todo_by_id`  
**HTTP method:** `GET`  
**Path:** `/todos/<int:todo_id>`

**Description:**  
Returns a single todo item by its ID.

**Path parameters:**

- `todo_id` (integer, required) – Unique identifier of the todo item to retrieve.

**Request body:**  
Not applicable for this endpoint.

**Response:**  
- **200 OK** – JSON object representing the requested todo item.
- **404 Not Found** – If a todo with the given `todo_id` does not exist.

**Usage note:**  
Use this endpoint to retrieve the details of a specific todo, for example when viewing or editing a single entry.

---

## Endpoint: Delete Todo by ID

**Function name:** `delete_todo`  
**HTTP method:** `DELETE`  
**Path:** `/todos/<int:todo_id>`

**Description:**  
Deletes a todo item by its ID.

**Path parameters:**

- `todo_id` (integer, required) – Unique identifier of the todo item to delete.

**Request body:**  
Not applicable for this endpoint.

**Response:**  
- **204 No Content** – Todo was successfully deleted (no response body).  
- **404 Not Found** – If a todo with the given `todo_id` does not exist.

**Usage note:**  
Call this endpoint to permanently remove a todo. This action is typically irreversible; confirm with the user in UI before sending the request.