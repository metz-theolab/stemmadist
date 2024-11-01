"""Utilities functions used to obtain the results of the paper."""
import json


def get_texts(json_collation_path, texts_output_folder):
    """Retrieve the full texts from a JSON collation."""
    with open(json_collation_path, "r") as f:
        json_collation = json.load(f)
    full_texts = {}
    for alignment in json_collation["alignment"]:
        text = ""
        for token in alignment["tokens"]:
            if token:
                text += token["text"] + " "
        full_texts[alignment["witness"]] = text
    for witness, text in full_texts.items():
        with open(f"{texts_output_folder}/{witness}.txt", "w") as f:
            f.write(text)
    return full_texts