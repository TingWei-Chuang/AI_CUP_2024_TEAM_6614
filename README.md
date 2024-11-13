# AI CUP 2024 - TEAM_6614

### Method

There are two stages in tackling the task.

In the first stage, we process the data (PDFs, only *finance* and *insurance*) using OCR methods because the text of some of the PDFs cannot be directly extracted. To do this, we first convert all of the PDFs into JPGs using `pdfplumber`. Next, we use `Tesseract` to OCR the text. `Tesseract` binaries are downloaded and `pytesseract` wrapper functions are used. Last, the OCR text is combined with original PDF text (which is flawed) to generate the dataset used for information retrieval.

In the second stage, which is information retrieval, we use `bge-reranker-v2-m3` and `bge-reranker-large`, both reranker models, to decide the similarity of the query and the document. The reason we use two models is that in the experiment `bge-reranker-v2-m3` outperforms `bge-reranker-large` in *insurance* and *faq* while the result is opposite in `finance`. Therefore, we decided to use two models to achieve better performance.

### Commands for reproduction of results

> ⚠️ Python environment should be configured according to `requirements.txt`. `Tesseract` should be installed if the preprocessing function is called.


Assume the original PDF data is located at `reference` (`reference/finance/*.pdf`, `reference/insurance/*.pdf`, `reference/faq/pid_map_content.json`) and the path of the question is `question.json`. All python packages are installed using `requirements.txt`. The 3rd party application `tesseract` is installed in your system. (You can `tesseract` in the terminal.)

We provide two ways to reproduce the results. One is performing the full procedure including preprocessing and retrival. The other is directly using preprocessed text to do retrival. The first one might take hours, while the second only takes minutes.

#### First method

After executing the following code (it takes several hours since OCRing all PDFs is computationally costly), we have the answer stored in `out.json`.

```bash
python Preprocess/pdf2jpg.py -d reference/finance -s data_img/finance -r 600 -m -i 4
python Preprocess/pdf2jpg.py -d reference/insurance -s data_img/insurance -r 600 -m -i 4
python Preprocess/jpg2text.py -d data_img/finance -s data_img_text/finance -m -i 4
python Preprocess/jpg2text.py -d data_img/insurance -s data_img_text/insurance -m -i 4
python Preprocess/img_text2text.py -d data_img_text/finance -p reference/finance -s data_text/finance -m -i 4
python Preprocess/img_text2text.py -d data_img_text/insurance -p reference/insurance -s data_text/insurance -m -i 4
python Model/reranker.py --question_path questions.json --source_path data_text --output_path out.json
```

#### Second method

You would unzip `preprocessed.zip` containing preprocessed text. Afterwards, you can call `reranker.py` to make prediction. We have the answer stored in `out.json`.

```bash
unzip preprocessed.zip
python Model/reranker.py --question_path questions.json --source_path data_text --output_path out.json
```
