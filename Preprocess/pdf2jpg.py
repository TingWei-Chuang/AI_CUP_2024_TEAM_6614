import pdfplumber
import os
import shutil
import argparse

def convert(path_src, path_des, resolution=600, log=False):
    os.mkdir(path_des)
    pdf = pdfplumber.open(path_src)
    for i, page in enumerate(pdf.pages):
        image_obj = page.to_image(resolution=resolution)
        image_obj.save(os.path.join(path_des, str(i) + ".jpg"))
    pdf.close()
    if log:
        print(f"{path_src} was processed...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--pdf_source_dir", type=str, required=True)
    parser.add_argument("-s", "--save_dir", type=str, required=True)
    parser.add_argument("-r", "--resolution", type=int, required=True)
    parser.add_argument("-m", "--enable_multiprocessing", action="store_true")
    parser.add_argument("-i", "--num_worker", default=4, type=int)

    args = parser.parse_args()

    pdf_source_dir = args.pdf_source_dir
    save_dir = args.save_dir
    resolution = args.resolution
    use_multiprocessing = args.enable_multiprocessing
    num_worker = args.num_worker

    shutil.rmtree(save_dir, ignore_errors=True)
    os.makedirs(save_dir)

    files = os.listdir(pdf_source_dir)
    prefixes = sorted([int(f.replace(".pdf", "")) for f in files])
    src_paths = [os.path.join(pdf_source_dir, str(pre) + ".pdf") for pre in prefixes]
    dest_paths = [os.path.join(save_dir, str(pre)) for pre in prefixes]

    if use_multiprocessing:
        import concurrent.futures
        resolutions = [resolution for i in range(len(src_paths))]
        logs = [True for i in range(len(src_paths))]
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_worker) as executor:
            results = executor.map(convert, src_paths, dest_paths, resolutions, logs)
            for _ in results:
                pass
    else:
        for src, dest in zip(src_paths, dest_paths):
            convert(src, dest, resolution)

    