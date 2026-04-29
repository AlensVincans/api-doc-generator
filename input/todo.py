from flask import Flask, request, jsonify

app = Flask(__name__)

todos = []


@app.route("/todos", methods=["GET"])
def get_todos():
    """Returns a list of all todo items."""
    return jsonify(todos), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    """Creates a new todo item with title and completed status."""
    data = request.get_json()

    todo = {
        "id": len(todos) + 1,
        "title": data.get("title"),
        "completed": data.get("completed", False)
    }

    todos.append(todo)
    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo_by_id(todo_id):
    """Returns a single todo item by its ID."""
    for todo in todos:
        if todo["id"] == todo_id:
            return jsonify(todo), 200

    return jsonify({"error": "Todo not found"}), 404


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Deletes a todo item by its ID."""
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return jsonify({"message": "Todo deleted"}), 200

    return jsonify({"error": "Todo not found"}), 404