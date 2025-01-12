import json
import os
from helper.api import get_kata_name_and_description
from helper.kata import KataParser
import unicodedata
import re


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

if __name__ == "__main__":
    with open("./setup.json", encoding="utf-8") as fin:
        setup = json.load(fin)

    with open("./source.html", encoding="utf-8") as fin:
        file = fin.read()

    base_dir = setup["download_folder"]
    extensions = setup["file_extensions"]

    parser = KataParser(file)
    katas = parser.parse_katas()

    print("Exporting katas...")
    for i, kata in enumerate(katas):
        print(f"\r{i + 1}/{len(katas)} katas exported.", end="")

        kata_name, kata_description = get_kata_name_and_description(kata.kata_id)

        for language, source_code in zip(kata.languages, kata.source_codes):
            file_dir = os.path.join(
                base_dir, kata.difficulty, slugify(kata.title), language
            )
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            filename = f"{slugify(kata_name)}{extensions[language]}"
            with open(os.path.join(file_dir, filename), "w", encoding="utf-8") as fout:
                fout.write(source_code)

            with open(os.path.join(file_dir, "README.md"), "w", encoding="utf-8") as fout:
                fout.write(kata_description)
    print("")
