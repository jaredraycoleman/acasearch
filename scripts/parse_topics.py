import pyperclip
import re

SUBJECTS = """
Accessibility technologies
Aging and technology
Ergonomics
Disabilities and technology
Assistive technologies
Elderly user interfaces
Novel input devices
Interaction techniques
Human computation
Datasets for interaction
Interaction design tools
Hardware for interaction
Physical devices for HCI
Sensing and tracking devices
Display technology
Haptic feedback
Robotic approaches
Novel materials
Fabrication techniques
Machine learning in HCI
Optimization in HCI
Statistical modeling in HCI
Natural language processing in HCI
Control theory in HCI
Signal processing in HCI
Computer vision in HCI
Human-AI interaction
Explainable AI
Algorithmic fairness
Social justice in HCI
Environmental sustainability in HCI
Critical computing
Ethical HCI research
Feminist HCI
Queer HCI
Decolonial HCI
Low-carbon technologies
Artful HCI experiences
Interaction aesthetics
Design processes in HCI
Interactive product design
Service design
Design methods
Design principles
Alternative epistemologies in design
Design for health and wellness
Game interaction
Playful systems
Player experience
Game development
Serious games
Gamification
Player psychology
Games user research
Game analytics
Health technologies
Wellness technologies
Clinical interfaces
Self-management technologies
Everyday wellness interfaces
Healthcare provider interfaces
Physical interaction techniques
Gesture interaction
Speech interfaces
Sound interaction
Haptics
Gaze-based interaction
Smell interaction
Physiological signal interaction
Mobile interfaces
VR interfaces
AR interfaces
On-body interfaces
Tangible interfaces
Collaborative technologies
Crowdsourcing systems
Group behavior with technology
Organizational technology use
Community technology interaction
Educational technologies
Learning analytics
Intelligent tutoring systems
Collaborative learning tools
Tangible learning interfaces
Child-computer interaction
Family technology interaction
Privacy techniques
Security technologies
Usability of privacy tools
Security behavior studies
ICT for development (ICTD)
HCI for low-income countries
Marginalized population technologies
Creativity tools
Maker technologies
Smart and connected communities
Transportation technologies
Urban informatics
Civic engagement technologies
Human-nature interaction
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