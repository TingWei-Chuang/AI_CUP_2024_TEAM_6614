import os
import json
import argparse

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import numpy as np


def reranker_retrieve(qs, source, corpus_dict):
    filtered_corpus = [corpus_dict[int(file)] for file in source]

    pairs = [[qs, corpus] for corpus in filtered_corpus]

    scores = []
    for pair in pairs:
        with torch.no_grad():
            input = tokenizer([pair], padding=True, truncation=True, return_tensors="pt").to("cuda:0")
            score = model(**input, return_dict=True).logits.view(-1, ).float().cpu().numpy()
        scores.append(score[0])
    scores = np.array(scores)
    best = scores.argmax()
    return source[best]

def load_text(source_path):
    document_text_fn = os.listdir(source_path)
    corpus_dict = dict()
    for fn in document_text_fn:
        pathname = os.path.join(source_path, fn)
        with open(pathname, "r") as f:
            text = f.read()
        text.replace(" ", "")
        text.replace("\n", "")
        corpus_dict[int(fn.replace(".txt", ""))] = text
    return corpus_dict
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question_path", type=str, required=True)
    parser.add_argument("--source_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)

    args = parser.parse_args()

    tokenizer_v2_m3 = AutoTokenizer.from_pretrained("BAAI/bge-reranker-v2-m3")
    model_v2_m3 = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-v2-m3")
    model_v2_m3.eval()
    model_v2_m3.to("cuda:0")

    tokenizer_large = AutoTokenizer.from_pretrained("BAAI/bge-reranker-large")
    model_large = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-large")
    model_large.eval()
    model_large.to("cuda:0")

    answer_dict = {"answers": []}

    with open(args.question_path, "rb") as f:
        qs_ref = json.load(f)

    source_path_finance = os.path.join(args.source_path, "finance")
    corpus_dict_finance = load_text(source_path_finance)

    source_path_insurance = os.path.join(args.source_path, "insurance")
    corpus_dict_insurance = load_text(source_path_insurance)
    
    
    source_path_faq = "data/reference/faq/pid_map_content.json"
    with open(source_path_faq, "rb") as f:
        temp = json.load(f)
        corpus_dict_faq = {int(key): str(value) for key, value in temp.items()}

    for q_dict in qs_ref["questions"]:
        if q_dict["category"] == "finance":
            tokenizer = tokenizer_large
            model = model_large
            retrieved = reranker_retrieve(q_dict["query"], q_dict["source"], corpus_dict_finance)
            answer = {"qid": q_dict["qid"], "retrieve": retrieved}
            answer_dict["answers"].append(answer)
        elif q_dict["category"] == "insurance":
            tokenizer = tokenizer_v2_m3
            model = model_v2_m3
            retrieved = reranker_retrieve(q_dict["query"], q_dict["source"], corpus_dict_insurance)
            answer = {"qid": q_dict["qid"], "retrieve": retrieved}
            answer_dict["answers"].append(answer)
        elif q_dict["category"] == "faq":
            tokenizer = tokenizer_v2_m3
            model = model_v2_m3
            retrieved = reranker_retrieve(q_dict["query"], q_dict["source"], corpus_dict_faq)
            answer = {"qid": q_dict["qid"], "retrieve": retrieved}
            answer_dict["answers"].append(answer)

    with open(args.output_path, "w", encoding="utf8") as f:
        json.dump(answer_dict, f, ensure_ascii=False, indent=4)
