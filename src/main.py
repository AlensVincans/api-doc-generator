import os
import time

from parser import extract_api_from_code
from prompt_builder import build_prompt
from generator import generate_openapi
from exporter import save_file
from validator import validate_openapi_file


MODELS = {
    "llama_3.1_8b": "meta-llama/llama-3.1-8b-instruct",
    "gpt_5_1": "openai/gpt-5.1",
    "claude_sonnet_4.6": "anthropic/claude-sonnet-4.6",
    "deepseek_v4_flash": "deepseek/deepseek-v4-flash",
    "gemma_3_4b": "google/gemma-3-4b-it",
    "gpt-oss-20b": "openai/gpt-oss-20b",
}


def main():
    input_file = "input/question_backend.py"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    api_data = extract_api_from_code(input_file)
    prompt = build_prompt(api_data)

    for name, model in MODELS.items():
        print(f"Generating OpenAPI with model: {name}")

        try:
            start_time = time.perf_counter()

            openapi_yaml = generate_openapi(prompt, model)

            end_time = time.perf_counter()
            generation_time = end_time - start_time

            output_path = os.path.join(output_dir, f"openapi_{name}.yaml")
            save_file(openapi_yaml, output_path)

            is_valid, message = validate_openapi_file(output_path)
            print(f"{name}: {message}")
            print(f"{name}: generation time = {generation_time:.2f} seconds")

        except Exception as error:
            print(f"{name}: generation failed - {error}")

    print("OpenAPI generation completed.")


if __name__ == "__main__":
    main()