def build_prompt(api_data):
    prompt = f"""
You are a professional API documentation specialist.

Your task is to generate an OpenAPI 3.0 YAML specification based strictly on the provided Python Flask source code analysis.

Important rules:
- Generate only valid OpenAPI 3.0 YAML.
- Do not generate Markdown.
- Do not wrap the result in code fences.
- Use only information found in the provided source code analysis.
- Do not invent endpoints, parameters, request fields, response fields, validation rules, or status codes.
- If response schema details are not visible in the source code analysis, use a general description.
- Convert Flask paths to OpenAPI paths, for example /todos/<int:todo_id> becomes /todos/{{todo_id}}.
- Include path parameters when they are visible in the route.
- Include requestBody only when request body fields are visible.
- Include only status codes that are visible in the source code.

API title: {api_data["title"]}
API version: {api_data["version"]}
Source file: {api_data["source_file"]}

Extracted endpoints:
"""

    for ep in api_data["endpoints"]:
        prompt += "\nEndpoint:\n"
        prompt += f"Function name: {ep['function_name']}\n"
        prompt += f"Path: {ep['path']}\n"
        prompt += f"HTTP methods: {', '.join(ep['methods'])}\n"
        prompt += f"Description/docstring: {ep['docstring']}\n"

        if ep["path_parameters"]:
            prompt += "Path parameters:\n"
            for param in ep["path_parameters"]:
                prompt += (
                    f"- name: {param['name']}, "
                    f"type: {param['type']}, "
                    f"required: {param['required']}\n"
                )
        else:
            prompt += "Path parameters: None\n"

        if ep["request_body_fields"]:
            prompt += "Request body fields:\n"
            for field in ep["request_body_fields"]:
                prompt += f"- {field}\n"
        else:
            prompt += "Request body fields: None\n"

        if ep["status_codes"]:
            prompt += "Visible status codes:\n"
            for code in ep["status_codes"]:
                prompt += f"- {code}\n"
        else:
            prompt += "Visible status codes: None\n"

    return prompt