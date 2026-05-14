import ast
import os
import re
from typing import Any, Dict, List


def load_source_code(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def convert_flask_path_to_openapi(path: str) -> str:
    path = re.sub(r"<(?:int|string|float|path):([^>]+)>", r"{\1}", path)
    path = re.sub(r"<([^>]+)>", r"{\1}", path)
    return path


def convert_express_path_to_openapi(path: str) -> str:
    return re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"{\1}", path)


def extract_flask_path_parameters(path: str) -> List[Dict[str, Any]]:
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


def extract_express_path_parameters(path: str) -> List[Dict[str, Any]]:
    parameters = []
    matches = re.findall(r":([A-Za-z_][A-Za-z0-9_]*)", path)

    for name in matches:
        parameters.append({
            "name": name,
            "in": "path",
            "required": True,
            "type": "string"
        })

    return parameters

def extract_python_status_codes(function_node: ast.FunctionDef) -> List[str]:
    status_codes = set()

    for node in ast.walk(function_node):
        if isinstance(node, ast.Tuple):
            for element in node.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, int):
                    if 100 <= element.value <= 599:
                        status_codes.add(str(element.value))

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "abort":
                if node.args and isinstance(node.args[0], ast.Constant):
                    if isinstance(node.args[0].value, int) and 100 <= node.args[0].value <= 599:
                        status_codes.add(str(node.args[0].value))

            if isinstance(node.func, ast.Attribute) and node.func.attr == "get_or_404":
                status_codes.add("404")

    return sorted(status_codes)


def extract_python_request_body_fields(function_node: ast.FunctionDef) -> List[str]:
    fields = set()
    json_variable_names = set()

    for node in ast.walk(function_node):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            call = node.value

            if isinstance(call.func, ast.Attribute) and call.func.attr == "get_json":
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        json_variable_names.add(target.id)

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "get" and node.args and isinstance(node.args[0], ast.Constant):
                field_name = node.args[0].value

                if isinstance(node.func.value, ast.Name) and node.func.value.id in json_variable_names:
                    fields.add(field_name)

                if isinstance(node.func.value, ast.Attribute):
                    if (
                        isinstance(node.func.value.value, ast.Name)
                        and node.func.value.value.id == "request"
                        and node.func.value.attr in {"json", "form", "args"}
                    ):
                        fields.add(field_name)

    return sorted(fields)


def extract_flask_routes_from_code(source_code: str) -> List[Dict[str, Any]]:
    tree = ast.parse(source_code)
    endpoints = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

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
                    "methods": [method.upper() for method in methods],
                    "docstring": ast.get_docstring(node) or "",
                    "path_parameters": extract_flask_path_parameters(route_path),
                    "request_body_fields": extract_python_request_body_fields(node),
                    "status_codes": extract_python_status_codes(node),
                    "source_language": "Python",
                    "framework": "Flask"
                }

                endpoints.append(endpoint)

    return endpoints

def remove_ts_swagger_blocks(source_code: str) -> str:
    """
    Removes manual @swagger/@openapi blocks so that manual documentation
    is not used as input for generation.
    """
    return re.sub(
        r"/\*\*[\s\S]*?@(?:swagger|openapi)[\s\S]*?\*/",
        "",
        source_code,
        flags=re.IGNORECASE
    )


def find_matching_parenthesis(text: str, open_index: int) -> int:
    depth = 0
    in_string = None
    escape = False

    for index in range(open_index, len(text)):
        char = text[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == in_string:
                in_string = None
            continue

        if char in {"'", '"', "`"}:
            in_string = char
            continue

        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index

    return -1


def split_top_level_arguments(argument_text: str) -> List[str]:
    args = []
    current = []
    depth = 0
    in_string = None
    escape = False

    for char in argument_text:
        if in_string:
            current.append(char)

            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == in_string:
                in_string = None

            continue

        if char in {"'", '"', "`"}:
            in_string = char
            current.append(char)
            continue

        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue

        current.append(char)

    if current:
        args.append("".join(current).strip())

    return args


def extract_ts_status_codes(route_call_text: str) -> List[str]:
    status_codes = set()

    for match in re.finditer(r"\.(?:status|sendStatus)\s*\(\s*(\d{3})\s*\)", route_call_text):
        status_codes.add(match.group(1))

    for match in re.finditer(r"\bstatus\s*:\s*(\d{3})\b", route_call_text):
        status_codes.add(match.group(1))

    return sorted(status_codes)


def extract_ts_request_body_fields(route_call_text: str) -> List[str]:
    fields = set()

    for match in re.finditer(
        r"\b(?:req|request)\.body\.([A-Za-z_][A-Za-z0-9_]*)",
        route_call_text
    ):
        fields.add(match.group(1))

    destructuring_pattern = re.compile(
        r"(?:const|let|var)\s*\{([^}]+)\}\s*=\s*(?:req|request)\.body",
        re.MULTILINE
    )

    for match in destructuring_pattern.finditer(route_call_text):
        raw_fields = match.group(1).split(",")

        for raw_field in raw_fields:
            field = raw_field.strip().split(":")[0].strip()

            if field and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", field):
                fields.add(field)

    return sorted(fields)


def infer_ts_function_name(route_arguments: List[str], http_method: str, path: str) -> str:
    if not route_arguments:
        return f"{http_method}_{path.strip('/').replace('/', '_').replace(':', '') or 'root'}"

    last_argument = route_arguments[-1].strip()

    controller_match = re.search(
        r"([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)",
        last_argument
    )

    if controller_match:
        return controller_match.group(2)

    function_match = re.search(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", last_argument)

    if function_match:
        return function_match.group(1)

    return f"{http_method}_{path.strip('/').replace('/', '_').replace(':', '') or 'root'}"


def extract_express_routes_from_code(source_code: str) -> List[Dict[str, Any]]:
    clean_source = remove_ts_swagger_blocks(source_code)
    endpoints = []

    route_pattern = re.compile(
        r"\b(?:router|app)\.(get|post|put|patch|delete|options|head)\s*\(",
        re.IGNORECASE
    )

    for match in route_pattern.finditer(clean_source):
        http_method = match.group(1).upper()
        open_paren_index = match.end() - 1
        close_paren_index = find_matching_parenthesis(clean_source, open_paren_index)

        if close_paren_index == -1:
            continue

        argument_text = clean_source[open_paren_index + 1:close_paren_index]
        route_call_text = clean_source[match.start():close_paren_index + 1]
        route_arguments = split_top_level_arguments(argument_text)

        if not route_arguments:
            continue

        path_argument = route_arguments[0].strip()
        path_match = re.match(r"""['"`]([^'"`]+)['"`]""", path_argument)

        if not path_match:
            continue

        route_path = path_match.group(1)

        endpoint = {
            "function_name": infer_ts_function_name(route_arguments, http_method.lower(), route_path),
            "path": convert_express_path_to_openapi(route_path),
            "original_path": route_path,
            "methods": [http_method],
            "docstring": "",
            "path_parameters": extract_express_path_parameters(route_path),
            "request_body_fields": extract_ts_request_body_fields(route_call_text),
            "status_codes": extract_ts_status_codes(route_call_text),
            "source_language": "TypeScript",
            "framework": "Express"
        }

        endpoints.append(endpoint)

    return endpoints


def extract_api_from_code(file_path: str) -> Dict[str, Any]:
    source_code = load_source_code(file_path)
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".py":
        endpoints = extract_flask_routes_from_code(source_code)
        source_language = "Python"
        framework = "Flask"

    elif extension in {".ts", ".tsx", ".js", ".jsx"}:
        endpoints = extract_express_routes_from_code(source_code)
        source_language = "TypeScript" if extension in {".ts", ".tsx"} else "JavaScript"
        framework = "Express"

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return {
        "title": "Generated API",
        "version": "1.0.0",
        "source_file": os.path.basename(file_path),
        "source_language": source_language,
        "framework": framework,
        "endpoints": endpoints
    }