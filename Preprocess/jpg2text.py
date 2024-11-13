import os
import shutil
import argparse
import cv2
import numpy as np
import pytesseract

def noise_removal(image):
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.erode(image, kernel, iterations=2)
    image = cv2.dilate(image, kernel, iterations=2)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

def convert(img_path):
    image = cv2.imread(img_path)
    image = (image - image.min()) / (image.max() - image.min())
    _, b = cv2.threshold(image[..., 0], 0.5, 1., cv2.THRESH_BINARY)
    _, g = cv2.threshold(image[..., 1], 0.5, 1., cv2.THRESH_BINARY)
    _, r = cv2.threshold(image[..., 2], 0.5, 1., cv2.THRESH_BINARY)
    b = b.astype(np.uint8)
    g = g.astype(np.uint8)
    r = r.astype(np.uint8)
    out = (b | g | r) * 255
    out = noise_removal(out)
    text = pytesseract.image_to_string(out, lang="chi_tra")
    return text

def convertDocument(path_src, path_des, log=False):
    fns = os.listdir(path_src)
    text = ""
    for fn in fns:
        path = os.path.join(path_src, fn)
        ocr_text = convert(path)
        text += ocr_text
    text = text.replace(" ", "")
    with open(path_des, "w") as f:
        f.write(text)
    if log:
        print(f"{path_src} was processed...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--jpg_source_dir", type=str, required=True)
    parser.add_argument("-s", "--save_dir", type=str, required=True)
    parser.add_argument("-m", "--enable_multiprocessing", action="store_true")
    parser.add_argument("-i", "--num_worker", default=4, type=int)

    args = parser.parse_args()

    jpg_source_dir = args.jpg_source_dir
    save_dir = args.save_dir
    use_multiprocessing = args.enable_multiprocessing
    num_worker = args.num_worker

    shutil.rmtree(save_dir, ignore_errors=True)
    os.makedirs(save_dir)

    folder_names = os.listdir(jpg_source_dir)
    document_ids = sorted([int(f) for f in folder_names])
    src_paths = [os.path.join(jpg_source_dir, str(id)) for id in document_ids]
    dest_paths = [os.path.join(save_dir, str(id) + ".txt") for id in document_ids]

    if use_multiprocessing:
        import concurrent.futures
        logs = [True for _ in range(len(src_paths))]
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_worker) as executor:
            results = executor.map(convertDocument, src_paths, dest_paths, logs)
            for _ in results:
                pass
    else:
        for src, dest in zip(src_paths, dest_paths):
            convertDocument(src, dest)

    