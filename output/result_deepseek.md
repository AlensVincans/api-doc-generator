# Todo API Documentation

## Endpoint: GET /todos

- **Function name**: `get_todos`
- **HTTP method**: GET
- **Description**: Returns a list of all todo items.
- **Parameters**: None.
- **Response**: A JSON array containing all todo objects.

**Usage note**: This endpoint is useful for retrieving the current state of all tasks.

---

## Endpoint: POST /todos

- **Function name**: `create_todo`
- **HTTP method**: POST
- **Description**: Creates a new todo item with a title and completed status.
- **Request body**: A JSON object with the following fields:
    - `title` (string, required): The title of the todo.
    - `completed` (boolean, required): Whether the todo is completed.
- **Response**: The created todo object, including its assigned ID.

**Usage note**: Ensure the request body is valid JSON and includes both `title` and `completed` fields.

---

## Endpoint: GET /todos/<int:todo_id>

- **Function name**: `get_todo_by_id`
- **HTTP method**: GET
- **Description**: Returns a single todo item identified by its unique ID.
- **Parameters**:
    - `todo_id` (integer, required): The ID of the todo to retrieve, provided as part of the URL path.
- **Response**: A JSON object representing the requested todo item.

**Usage note**: The ID must be an integer. Returns a 404 error if the todo does not exist.

---

## Endpoint: DELETE /todos/<int:todo_id>

- **Function name**: `delete_todo`
- **HTTP method**: DELETE
- **Description**: Deletes a todo item by its ID.
- **Parameters**:
    - `todo_id` (integer, required): The ID of the todo to delete, provided as part of the URL path.
- **Response**: A JSON message indicating successful deletion (e.g., `{"message": "Todo deleted"}`).

**Usage note**: This operation is irreversible. The request returns a 404 error if the ID does not exist.

---

*Generated from source file `todo.py`.*