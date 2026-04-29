import ast
import os
import re


def load_source_code(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def convert_flask_path_to_openapi(path):
    path = re.sub(r"<(?:int|string|float|path):([^>]+)>", r"{\1}", path)
    path = re.sub(r"<([^>]+)>", r"{\1}", path)
    return path


def extract_path_parameters(path):
    parameters = []

    matches = re.findall(r"<(?:(int|string|float|path):)?([^>]+)>", path)

    for param_type, name in matches:
        openapi_type = "string"

        if param_type == "int":
            openapi_type = "integer"
        elif param_type == "float":
            openapi_type = "number"

        parameters.append({
            "name": name,
            "in": "path",
            "required": True,
            "type": openapi_type
        })

    return parameters


def extract_status_codes(function_node):
    status_codes = set()

    for node in ast.walk(function_node):
        if isinstance(node, ast.Tuple):
            for element in node.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, int):
                    if 100 <= element.value <= 599:
                        status_codes.add(str(element.value))

    return sorted(status_codes)


def extract_request_body_fields(function_node):
    fields = set()

    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "get":
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "data":
                        if node.args and isinstance(node.args[0], ast.Constant):
                            fields.add(node.args[0].value)

    return sorted(fields)


def extract_routes_from_code(source_code):
    tree = ast.parse(source_code)
    endpoints = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if not isinstance(decorator, ast.Call):
                    continue

                if not isinstance(decorator.func, ast.Attribute):
                    continue

                if decorator.func.attr != "route":
                    continue

                route_path = None
                methods = ["GET"]

                if decorator.args and isinstance(decorator.args[0], ast.Constant):
                    route_path = decorator.args[0].value

                for keyword in decorator.keywords:
                    if keyword.arg == "methods":
                        try:
                            methods = ast.literal_eval(keyword.value)
                        except Exception:
                            methods = ["GET"]

                if route_path:
                    endpoint = {
                        "function_name": node.name,
                        "path": convert_flask_path_to_openapi(route_path),
                        "original_path": route_path,
                        "methods": methods,
                        "docstring": ast.get_docstring(node) or "",
                        "path_parameters": extract_path_parameters(route_path),
                        "status_codes": extract_status_codes(node),
                        "request_body_fields": extract_request_body_fields(node)
                    }

                    endpoints.append(endpoint)

    return endpoints


def extract_api_from_code(file_path):
    source_code = load_source_code(file_path)
    endpoints = extract_routes_from_code(source_code)

    return {
        "title": "Todo API",
        "version": "1.0.0",
        "source_file": os.path.basename(file_path),
        "endpoints": endpoints
    }