import pathlib
import re
import pyperclip

SUBJECTS = """
Communication Protocol and Architecture
High-speed Communication and Network
Wireless Communication and Network
Multimedia Communication System
Personal Communication System
Mobile Ad-hoc and Sensor Network
Low-power Network and System
Wearable Network and System
Embedded System and Networking
Internet Technology and IP-based Applications
Network Control and Management
Network Performance, Analysis and Evaluation
Quality of Services (QoS)
Multicast Routing and Technology
Security, Privacy and Trust
Fault-tolerant and Dependable System
Multi-agent System and Applications
Parallel/Distributed Algorithm and Architecture
Distributed Database and Data Mining
Distributed Graphics and VR/AR/MR System
Distributed AI and Soft/Natural Computing     
Biological Informatics
E-Learning, E-Commerce, E-Society, etc.
Grid, Cluster and Internet Computing
Peer-to-Peer (P2P) System
Service-oriented Framework and Middleware
Autonomic Computing and Communication
WWW, Semantic Web and Cyber World
Mobile and Context-aware Computing
Ubiquitous/Pervasive Networks and Computing
Ubiquitous Intelligence and Smart World
Smart Object, Space/Environment and System
Innovative Networking and Applications
Social, Ethical & Other Issues of Networked World
Network and Application Hardware
Cognitive Network Access
Digital Eco Systems
"""

def main():
    topics = SUBJECTS.splitlines()
    topics = [re.sub(r".*: ", "", line).strip() for line in topics if line.strip()]
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