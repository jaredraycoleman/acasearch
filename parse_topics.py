import re
import pyperclip

SUBJECTS = """
Mobile User Experience
Security and Privacy
User Behaviour Analysis and Modelling
Crowdsourcing – Platforms and Applications
Internet of Things – Systems, Data Analytics, and Applications
Urban/mobile Crowd-sensing
Participatory Sensing
Wireless Access Technologies
Performance Analysis, Modelling and Measurement of Mobile Networks
Wearable Computing
Body Area Networks
Mobile Data Analysis and Mobile Platforms
Mobile Multimedia
Mobile User Interfaces and Interaction Technologies
Toolkit and Languages for Mobile Computing
Networked Sensing and Applications
Mobile Device Architectures
Mobile Systems and Applications
Mobile Data Management and Analytics
Energy Aware Mobile Computing
Pervasive Sensing
Localization and Tracking
Activity Recognition
Social Network Applications to Mobile Computing
Context and Location-based Applications and Services
AI and Machine Learning Algorithms and Application for Mobile Computing
Mobile Augmented Reality/Mixed Reality
Mobile Cloud Computing
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