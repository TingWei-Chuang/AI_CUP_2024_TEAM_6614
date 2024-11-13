# Preprocess

### Usage

- `python pdf2jpg.py -d [PDF_SOURCE_DIR] -s [SAVE_DIR] -r [RESOLUTION]`

    - The command would inspect every PDF files in **PDF_SOURCE_DIR**, convert them to JPG files and store the images in **SAVE_DIR**. This is for OCR later on.

    - `-d` the path of directory where PDF files to be converted

    - `-s` the path where converted files are stored

    - `-r` the parameter which controls the image's resolution after transformation

    - `-m` (optional) set to enable multiprocessing

    - `-i` (optional) number of workers of multiprocessing when `-m` is set

    - Usage examples \
    `python pdf2jpg.py -d .../reference/finance -s .../data_img/finance -r 600 -m -i 4` (adjust paths at your need)

- `python jpg2text.py -d [JPG_SOURCE_DIR] -s [SAVE_DIR]`

    - The command would inspect every JPG files in **JPG_SOURCE_DIR**, OCR these files, and store the text files in **SAVE_DIR**.

    - `-d` the path of directory where JPG files to be converted

    - `-s` the path where converted files are stored

    - `-m` (optional) set to enable multiprocessing

    - `-i` (optional) number of workers of multiprocessing when `-m` is set

    - Usage examples \
    `python jpg2text.py -d .../data_img/finance -s .../data_img_text/finance -m -i 4` (adjust paths at your need)

- `python img_text2text.py -d [IMG_TEXT_SOURCE_DIR] -p [PDF_TEXT_SOURCE_DIR] -s [SAVE_DIR]`

    - The command would inspect every OCR files (text) in **IMG_TEXT_SOURCE_DIR**, find corresponding PDF files in **PDF_TEXT_SOURCE_DIR**, combine these two, and store the resulting text files in **SAVE_DIR**. The files in two directory must correspond to each other. If there is a file named *0.txt* in **IMG_TEXT_SOURCE_DIR**, there must be a file named *0.pdf* in **PDF_TEXT_SOURCE_DIR**.

    - `-d` the path of directory where OCR text is located

    - `-p` the path of directory where PDF text is located

    - `-s` the path where converted files are stored

    - `-m` (optional) set to enable multiprocessing

    - `-i` (optional) number of workers of multiprocessing when `-m` is set

    - Usage examples \
    `python img_text2text.py -d .../data_img_text/finance -p .../reference/finance -s .../data_text/finance -m -i 4` (adjust paths at your need)
