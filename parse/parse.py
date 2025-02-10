# Get the latest version of emoji-test.txt before running this script:
# https://unicode.org/Public/emoji/15.1/emoji-test.txt

import json
import re

from typing import Any, Dict

from jsonschema import validate
from jsonschema.exceptions import ValidationError

import humps


def find_base_name(description: str):
    base = description.split(":")

    if len(base) == 1:
        return description

    modifiers = base[1].split(", ")
    modifiers = [i.strip() for i in modifiers]

    tones = [
        "medium-light skin tone",
        "medium-dark skin tone",
        "light skin tone",
        "medium skin tone",
        "dark skin tone",
    ]

    modifiers = [i for i in modifiers if i not in tones and i != "person"]

    if len(modifiers) == 0:
        return base[0]
    else:
        return base[0] + ": " + ", ".join(modifiers)


def find_version(s: str):
    match_version = re.compile(r"E\d+(\.\d+)?", re.IGNORECASE)
    version_test = match_version.search(s)
    if version_test:
        version = version_test.group(0)
        version = version.strip()
        return version, version_test.start()
    else:
        return None, None


def validate_schema(emojiMap) -> None:
    with open("./parse/schema.json", "r", encoding="utf-8") as file:
        schema = json.load(file)
    try:
        validate(instance=emojiMap, schema=schema)
    except ValidationError as e:
        print(e.message)
        exit(1)


def write_files(emojiMap: Dict[str, Any]) -> None:
    validate_schema(emojiMap)

    with open("./parse/emojiMap.json", "w", encoding="utf-8") as file:
        json.dump(emojiMap, file, ensure_ascii=False, separators=(",", ": "))

    with open("./parse/emojiMapPretty.json", "w", encoding="utf-8") as file:
        json.dump(emojiMap, file, ensure_ascii=False, indent=2)


def parse_lines(data: str):
    emoji_map = {}

    base_name_to_base_hex = {}
    base_hex_to_modifiers = {}

    lines = data.split("\n")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        left, right = line.split("#", maxsplit=1)

        hex_code_points, status = left.split(";")

        hex_code_points = hex_code_points.strip()
        status = status.strip()

        if status == "component":
            continue

        version, index = find_version(right)

        if not version or not index:
            continue

        emoji = right[:index].strip()
        emoji = emoji.strip()

        full_name = right[index + len(version) :].strip()
        full_name = full_name.strip()

        base_name = find_base_name(full_name)
        base_name = base_name.strip()

        is_base = False
        if base_name == full_name and status == "fully-qualified":
            is_base = True
            base_name_to_base_hex[base_name] = hex_code_points
            base_hex_to_modifiers[hex_code_points] = {}

        elif base_name in base_name_to_base_hex:
            tones = ["1F3FB", "1F3FC", "1F3FD", "1F3FE", "1F3FF"]
            points = hex_code_points.split(" ")
            has_tones = [t for t in points if t in tones]
            tone_count = len(has_tones)

            if tone_count == 1:
                tone = has_tones[0]
                base_code_points = base_name_to_base_hex[base_name]
                base_hex_to_modifiers[base_code_points][tone] = hex_code_points

        emoji_map[hex_code_points] = {
            "hex_code_points": hex_code_points,
            "status": status,
            "emoji": emoji,
            "version": version,
            "base_name": base_name,
            "full_name": full_name,
            "is_base": is_base,
            "base_hex": base_name_to_base_hex[base_name],
            "modifiers": {} if is_base else None,
        }

    for key, v in base_hex_to_modifiers.items():
        if v != {}:
            emoji_map[key]["modifiers"] = v
        else:
            emoji_map[key]["modifiers"] = None

    return emoji_map


def main():
    with open("./emoji-test.txt", "r", encoding="utf-8") as file:
        data = file.read()

    emoji_map = parse_lines(data)
    # TODO: Don't need humps, just use camelCase from the beginning
    emojiMap = humps.camelize(emoji_map)

    write_files(emojiMap)


if __name__ == "__main__":
    main()
