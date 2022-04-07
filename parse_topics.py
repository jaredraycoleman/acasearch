import re
import pyperclip

SUBJECTS = """
Anti-malware techniques: detection, analysis, and prevention
Cyber-crime defense and forensics (e.g., anti-phishing, anti-blackmailing, anti-fraud techniques)
Security for future Internet architectures and designs (e.g., Software-Defined Networking)
Implementation, deployment and management of network security policies
Integrating security in network protocols (e.g., routing, naming, and management)
Cyber attack (e.g., APTs, botnets, DDoS) prevention, detection, investigation, and response
Software/firmware analysis, customization, and transformation for systems security
Privacy and anonymity in networks and distributed systems
Security and privacy for blockchains and cryptocurrencies
Public key infrastructures, key management, certification, and revocation
Security for cloud/edge computing
Security and privacy of mobile/smartphone platforms
Security for cyber-physical systems (e.g., autonomous vehicles, industrial control systems)
Security for emerging networks (e.g., home networks, IoT, body-area networks, VANETs)
Security for large-scale, critical infrastructures (e.g., electronic voting, smart grid)
Security and privacy of systems based on machine learning and AI
Security of Web-based applications and services (e.g., social networking, crowd-sourcing)
Special problems and case studies: e.g., tradeoffs between security and efficiency, usability, cost, and ethics
Usable security and privacy
Trustworthy Computing software and hardware to secure networks and systems
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