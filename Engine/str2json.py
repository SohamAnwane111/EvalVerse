import json
import re


def clean_text_block(text: str) -> str:
    """Clean up text by removing surrounding markdown, code blocks, or backticks."""
    return text.strip().strip("`").strip("```").strip()


def extract_all_json_objects(text: str) -> list:
    """
    Extracts all valid JSON objects from the string.
    Returns a list of parsed JSON objects.
    """
    text = clean_text_block(text)
    candidates = re.findall(r'\{.*?\}', text, re.DOTALL)
    json_objects = []
    for candidate in candidates:
        try:
            json_objects.append(json.loads(candidate))
        except json.JSONDecodeError:
            continue
    return json_objects


def extract_first_json_safe(text: str):
    """
    Extracts and returns the first valid JSON object (flat only) from the string.
    If nothing is found, returns None.
    """
    all_objs = extract_all_json_objects(text)
    if all_objs:
        return all_objs[0]
    print("❌ No valid JSON object found.")
    return None


def extract_first_any_json(text: str):
    """
    Extracts the first valid JSON structure (object or array), even with nesting.
    Much more reliable than regex-based extraction.
    """
    text = clean_text_block(text)
    decoder = json.JSONDecoder()
    for i in range(len(text)):
        try:
            obj, _ = decoder.raw_decode(text[i:])
            return obj
        except json.JSONDecodeError:
            continue
    print("❌ No valid JSON found in any format.")
    return None


def is_valid_json(text: str) -> bool:
    """Check if the provided string is a valid JSON string."""
    text = clean_text_block(text)
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def pretty_print_json(json_obj) -> str:
    """Return a pretty-printed JSON string from a Python object."""
    return json.dumps(json_obj, indent=2, ensure_ascii=False)

