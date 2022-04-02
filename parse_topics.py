import re
import pyperclip

SUBJECTS = """
Smart Mobility
Internet of Medical Things
Wireless & Softwarization
"""

def main():
    # re.sub(".*Topic \d: ", "", line)
    topics = SUBJECTS.splitlines()
    topics_str = " // ".join(line.strip() for line in topics if line)
    try:
        pyperclip.copy(topics_str)
    except:
        print(topics_str)


if __name__ == "__main__":
    main()