# FPGA Macro Extraction From Docs Using LLMs

This project demonstrates how to use a LLM to extract FPGA macro definitions from FPGA vendor documentation, websites, and primitive / macro libraries into structured objects in Python and dump them to JSON.

The data model is a collection of macros, each with a name, description, ports, and attributes (i.e.e parameters).
Using Pydantic, the data model is dumped to a JSON schema that can be used for structured outputs from LLMs.
One can now simply pass the raw text extracted from a FPGAs vendor PDF documentation, web documentation, or large Verilog / CHDL /vendor-specific library files to the LLM and it will extract all the macro definitions into structured objects.

The `demo.py` script demonstrates how to use the LLM to extract macros from two test PDF files in the `demo_docs` directory:

- `7series_logic.pdf`: Contains documentation for logic macros for the Xilinx 7 Series FPGAs pulled from the Xilinx website.
- `7series_memory.pdf`: Contains documentation for memory macros for the Xilinx 7 Series FPGAs pulled from the Xilinx website.

The script uses the `llm_openrouter` library to interact with the LLM and the `pypdf` library to read PDF files.
The extracted macros are saved to JSON files in the `output` directory, with each file named after the input document.
Currently, the demo uses the `google/gemini-flash-1.5-8b` model (with the default provider `google-ai-studio`) from OpenRouter. You also need to set the `OPENROUTER_API_KEY` environment variable if you would like to run the demo.

So far the results look surprisingly good! The LLM is nearly perfect.
The biggest exception is the "RAMB18E1" macro, for which the LLM does not extract all the parameters listed in the docs (which there are many for "RAMB18E1").