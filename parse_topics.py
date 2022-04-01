import re
import pyperclip

SUBJECTS = """
Performance evaluation and modeling
Analytical Models
Simulation languages and tools for wireless systems
Wireless measurements tools and experiences
Formal methods for analysis of wireless systems
Correctness, survivability and reliability evaluation
Mobility modeling and management
Models and protocols for cognitive radio networks
Models and protocols for autonomic, or self-* networks
Capacity, coverage and connectivity modeling and analysis
Wireless network algorithms and protocols
Software Defined Network
Services for Smart City
Wireless PANs, LANs
Ad hoc and MESH networks
Vehicular Ad-hoc Networks (VANET)
Sensor and actuator networks
Delay Tolerant Networks
Integration of wired and wireless systems
Pervasive computing and emerging models
Wireless multimedia systems
QoS provisioning in wireless and mobile networks
Security and privacy of mobile/wireless systems
Algorithms and protocols for energy efficient operation and power control
Mobile applications, system software and algorithms
RF channel modeling and analysis
Design methodologies
Tools, prototypes and testbeds
Parallel and distributed simulation of wireless systems
Wireless Communication and Mobile Networking
Operating systems for mobile computations
Programming language support for mobility
Resource management techniques
Management of mobile object systems
Mobile cloud/edge/fog computing
Mobile crowd-sourcing
Mobile computing and application
AI and Federated Learning models for wireless and mobile networks
"""

def main():
    # re.sub(".*Topic \d: ", "", line)
    topics = SUBJECTS.splitlines()
    topics_str = " // ".join(line.strip() for line in topics if line)
    pyperclip.copy(topics_str)


if __name__ == "__main__":
    main()