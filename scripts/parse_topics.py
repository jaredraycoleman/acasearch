import pyperclip

SUBJECTS = """
Novel and innovative distributed applications and systems, particularly in the areas of middleware
cloud, edge and fog computing
big data processing
streaming and complex event processing
distributed social networking
IoT and cyber-physical systems
mobile computing
advanced networking (SDN/NFV)
micro-services and service-oriented computing
peer-to-peer systems, and
data center and internet-scale systems.
Novel architectures and mechanisms, particularly in the areas of
publish/subscribe systems
epidemic protocols
language-based approaches
virtualization and resource allocation
distributed storage
trusted execution environments
blockchains, cryptocurrencies and smart contracts, and
distributed consensus mechanisms.
System issues and design goals, including
interoperability and adaptation
self-* properties (e.g., self-organization, self-management,…)
security and practical applications of cryptography
trust and privacy
cooperation incentives and fairness
fault-tolerance and dependability
scalability and elasticity, and
tail-performance and energy-efficiency
"""

PARSE_LINES = False

def main():
    if PARSE_LINES:
        topics = [topic.strip() for line in SUBJECTS.splitlines() for topic in line.strip().split(",") if topic.strip()]
    else:
        topics = [topic.strip() for topic in SUBJECTS.splitlines() if topic.strip()]

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