import uuid
import jsonpatch
from flask import abort, Blueprint, jsonify, request
from datetime import datetime, timezone
from ..swagger import validate

app_name = __name__.split(".")[-1]
app = Blueprint(app_name, app_name)

todos = [] # this example just updates this array, probably should update a database


def find(f, seq):
  """Return first item in sequence where f(item) == True"""
  for item in seq:
    if f(item): 
      return item


@app.route('/api/v1/todos')
def list_entries():
  return jsonify(todos)


@app.route('/api/v1/todo/<id>')
def get_entry(id):
  entry = find(lambda x: x['id'] == id, todos)
  if entry is None:
    abort(404, 'Entry Not Found')
  return jsonify(entry)


@app.route('/api/v1/todo', methods=['POST'])
def create():
  json = request.get_json()
  validate(json, 'CreateTodo')
  json['id'] = str(uuid.uuid4())
  json['created'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
  todos.append(json)
  return jsonify(json)


@app.route('/api/v1/todo/<id>', methods=['PUT'])
def update(id):
  json = request.get_json()
  validate(json, 'Todo')

  json['id'] = id # reject any id changes
  json['last_updated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

  entry = find(lambda x: x['id'] == id, todos)
  if entry is not None:
    todos.remove(entry)
  todos.append(json)

  return jsonify(json)


@app.route('/api/v1/todo/<id>', methods=['PATCH'])
def patch(id):
  json = request.get_json()

  entry = find(lambda x: x['id'] == id, todos)
  if entry is None:
    abort(404, 'Entry Not Found')

  try:
    patch = jsonpatch.JsonPatch(json)
    result = patch.apply(entry)
  except jsonpatch.InvalidJsonPatch as e:
    abort(400, str(e))
  except jsonpatch.JsonPatchConflict as e:
    abort(409, str(e))
  except jsonpatch.JsonPatchTestFailed as e:
    return jsonify(entry), 201

  result['id'] = id # reject any id changes
  result['last_updated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
  validate(result, 'Todo', 422)
  todos.remove(entry)
  todos.append(result)
  return jsonify(result)


@app.route('/api/v1/todo/<id>', methods=['DELETE'])
def delete(id):
  entry = find(lambda x: x['id'] == id, todos)
  if entry is None:
    return '', 204
  todos.remove(entry)

  return jsonify(entry)