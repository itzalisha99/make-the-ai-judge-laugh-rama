"""Make the AI Judge Laugh — one funny line about office life.

The program writes a single office joke to /output/entry.txt.
Standard library only; no network, no files read, no secrets.
"""

import os

LINE = "We moved to an open-plan office so we could collaborate. Now we all wear headphones and message each other."


def validate(text: str) -> None:
    """Check the line against the bounty gate before it is written.

    The gate wants UTF-8 text of 1 to 200 characters that is not only
    white space. Anything outside that is refused, so fail loudly here
    instead of writing a file the judge would never see.
    """
    text.encode("utf-8")  # raises if the line is not valid UTF-8
    if not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    # Control characters would survive the gate but look broken to a
    # reader, so refuse them here rather than shipping them.
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")


def main() -> None:
    validate(LINE)
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read the file back and confirm it is byte-for-byte what we meant
    # to write: a silent encoding or newline slip would otherwise
    # reach the judge unnoticed.
    with open(path, "rb") as f:
        written = f.read()
    if written != (LINE + "\n").encode("utf-8"):
        raise ValueError("entry.txt does not match the intended line")


if __name__ == "__main__":
    main()
