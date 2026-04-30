import yaml

def validate_openapi_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            return False, "YAML content is not an object."

        required_fields = ["openapi", "info", "paths"]

        for field in required_fields:
            if field not in data:
                return False, f"Missing required OpenAPI field: {field}"

        if not isinstance(data["paths"], dict):
            return False, "OpenAPI paths field must be an object."

        return True, "Valid basic OpenAPI structure."

    except Exception as error:
        return False, str(error)