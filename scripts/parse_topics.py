import pyperclip
import re

SUBJECTS = """
operating systems; runtime systems; parallel and distributed systems; storage; networking; security and privacy; virtualization; software-hardware interactions; performance evaluation and workload characterization; reliability, availability, and scalability; energy and power management; bug-finding, tracing, analyzing, and troubleshooting
"""

PARSE_LINES = False

def main():
    separators = ["//", ";", "\n"]
    topics = re.split("|".join(separators), SUBJECTS)
    topics = [topic.strip() for topic in topics if topic.strip()]

    print(len(topics))
    topics_str = " // ".join(topics)
    print(topics_str)
    print()

    try:
        pyperclip.copy(topics_str)
        print("**COPIED TO CLIPBOARD**")
    except:
        print("**UNABLE TO COPY**")


if __name__ == "__main__":
    main()