import re


def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    emails = re.findall(pattern, text)

    return emails[0] if emails else None


def extract_phone(text):

    pattern = r"(?:\+91[-\s]?)?[6-9]\d{9}"

    phones = re.findall(pattern, text)

    return phones[0] if phones else None


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if len(line.split()) in [2, 3]:

            if re.fullmatch(r"[A-Za-z ]+", line):

                return line

    return None


def extract_linkedin(text):

    import re

    pattern = r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()

    return None

def extract_github(text):

    import re

    pattern = r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()

    return None