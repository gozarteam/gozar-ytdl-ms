import re


def clean_filename(filename: str) -> str:
    invalid_chars = r'[<>:"/\\|?*]'
    cleaned_filename = re.sub(invalid_chars, "_", filename)
    cleaned_filename = cleaned_filename.strip()
    return cleaned_filename
