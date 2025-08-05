import os
from pathlib import Path
from string import Template

import pypdf
from llm_openrouter import OpenRouterChat

from data_model import MacroCollection

DIR_CURRENT = Path(__file__).parent
DIR_DOCS = DIR_CURRENT / "demo_docs"
DIR_OUTPUT = DIR_CURRENT / "demo_output"

if not DIR_OUTPUT.exists():
    DIR_OUTPUT.mkdir(parents=True)

MODEL_ID = "google/gemini-flash-1.5-8b"
MODEL_PROVIDER = {"only": ["google-ai-studio"]}

llm = OpenRouterChat(
    model_id=MODEL_ID,
    key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
    headers={"HTTP-Referer": "https://llm.datasette.io/", "X-Title": "LLM"},
    supports_schema=True,
)

SCHEMA = MacroCollection.model_json_schema()

PROMPT_TEMPLATE = Template(
    """
    Your task is to extract FPGA macro definitions from vendor documentation, websites, and libraries into structured objects.
    Please extract all the macros you can find that are well defined.
    Be sure to extract all ports and attributes (i.e. parameters) for each macro.

    The structured schema of a collection of macro objects to use for the extraction is shown below. Please follow this schema exactly.

    SCHEMA:
    ```
    $schema
    ```

    The input data is shown below.

    INPUT DATA:
    ```
    $input_data
    ```
    """
)

if __name__ == "__main__":
    DEMO_DOCS = [
        DIR_DOCS / "7series_logic.pdf",
        DIR_DOCS / "7series_memory.pdf",
    ]

    for doc_path in sorted(DEMO_DOCS):
        print(f"Processing {doc_path.name}...")

        print(f"Loading {doc_path.name}...")
        doc = pypdf.PdfReader(doc_path)
        print(f"Loaded {len(doc.pages)} pages from {doc_path.name}.")

        print("Extracting text from PDF...")
        doc_txt = "\n\n".join([page.extract_text() for page in doc.pages])
        print(
            f"Extracted text from {doc_path.name}, length: {len(doc_txt)} characters."
        )

        print("Generating prompt for LLM...")
        prompt = PROMPT_TEMPLATE.substitute(schema=SCHEMA, input_data=doc_txt)
        print(f"Prompt generated: length {len(prompt)} characters.")

        print("Sending request to LLM...")
        response = llm.prompt(
            prompt, schema=SCHEMA, provider=MODEL_PROVIDER, max_tokens=80_000
        )
        response_txt = response.text()
        print("Response received from LLM.")

        response_file = DIR_OUTPUT / f"{doc_path.stem}__response.json"
        response_file.write_text(response_txt)

        print("Parsing response into data structure...")
        macro_collection = MacroCollection.model_validate_json(response_txt)
        print(f"Parsed {len(macro_collection.macros)} macros from the response.")

        print("Dumping macros to JSON file...")
        output_file = DIR_OUTPUT / f"{doc_path.stem}__macros.json"
        output_file.write_text(macro_collection.model_dump_json(indent=4))
        print(f"Dumped macros to {output_file}.")

        print("Processing complete for this document.\n")
        print("--------------------------------------------------\n")
