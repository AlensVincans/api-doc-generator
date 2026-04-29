import os

from parser import extract_api_from_code
from prompt_builder import build_prompt
from generator import generate_openapi
from exporter import save_file
from validator import validate_openapi_file


def main():
    input_file = "input/todo.py"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    api_data = extract_api_from_code(input_file)
    prompt = build_prompt(api_data)

    models = {
        "gpt": "openai/gpt-5.1",
        "claude": "anthropic/claude-sonnet-4.6",
        "deepseek": "deepseek/deepseek-v4-flash"
    }

    for name, model in models.items():
        print(f"Generating OpenAPI with {name}...")

        openapi_yaml = generate_openapi(prompt, model)

        output_path = os.path.join(output_dir, f"openapi_{name}.yaml")
        save_file(openapi_yaml, output_path)

        is_valid, message = validate_openapi_file(output_path)
        print(f"{name}: {message}")

    print("OpenAPI generation completed.")


if __name__ == "__main__":
    main()