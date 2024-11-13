# Model

### Usage

- `python reranker.py --question_path [QUESTION_PATH] --source_path [SOURCE_PATH] --output_path [OUTPUT_PATH]`

    - The command would read the questions at **QUESTION_PATH**, read the (converted, OCRed) data from **SOURCE_PATH**, and save the prediction at **OUTPUT_PATH**.

    - Internally, reranker models are fetched from *Hugging Face*, loaded into GPU, and assigned tasks for scoring relativity.

    - Usage examples \
    `python reranker.py --question_path .../preliminary/questions_example.json --source_path .../data_text --output_path .../out.json` (adjust paths at your need)
