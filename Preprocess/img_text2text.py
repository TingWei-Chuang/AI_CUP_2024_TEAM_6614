import os
import shutil
import argparse
import pdfplumber

def read_pdf(path):
    pdf = pdfplumber.open(path)
    pdf_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            pdf_text += text
    pdf.close()
    return pdf_text

def add_pdf_text(img_text_path_src, pdf_text_path_src, path_des, log=False):
    text = ""
    text += read_pdf(pdf_text_path_src)
    with open(img_text_path_src, "r") as f:
        text += f.read()
    text = text.replace(" ", "")
    with open(path_des, "w") as f:
        f.write(text)
    if log:
        print(f"{img_text_path_src} was processed...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--img_text_source_dir", type=str, required=True)
    parser.add_argument("-p", "--pdf_text_source_dir", type=str, required=True)
    parser.add_argument("-s", "--save_dir", type=str, required=True)
    parser.add_argument("-m", "--enable_multiprocessing", action="store_true")
    parser.add_argument("-i", "--num_worker", default=4, type=int)

    args = parser.parse_args()

    img_text_source_dir = args.img_text_source_dir
    pdf_text_source_dir = args.pdf_text_source_dir
    save_dir = args.save_dir
    use_multiprocessing = args.enable_multiprocessing
    num_worker = args.num_worker

    shutil.rmtree(save_dir, ignore_errors=True)
    os.makedirs(save_dir)

    files = os.listdir(img_text_source_dir)
    prefixes = sorted([int(f.replace(".txt", "")) for f in files])
    src_img_text_paths = [os.path.join(img_text_source_dir, str(id) + ".txt") for id in prefixes]
    src_pdf_text_paths = [os.path.join(pdf_text_source_dir, str(id) + ".pdf") for id in prefixes]
    dest_paths = [os.path.join(save_dir, str(id) + ".txt") for id in prefixes]

    if use_multiprocessing:
        import concurrent.futures
        logs = [True for _ in range(len(src_img_text_paths))]
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_worker) as executor:
            results = executor.map(add_pdf_text, src_img_text_paths, src_pdf_text_paths, dest_paths, logs)
            for _ in results:
                pass
    else:
        for src_img, src_pdf, dest in zip(src_img_text_paths, src_pdf_text_paths, dest_paths):
            add_pdf_text(src_img, src_pdf, dest)