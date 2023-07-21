import pyperclip

SUBJECTS = """
Computer and communication networks, protocols and algorithms
Wireless, mobile, ad-hoc and sensor networks, quantum networks, IoT applications, and blockchain networks
Computer architectures, hardware accelerators, multi-core processors, memory systems and storage networks
High Performance Computing
Operating systems, file systems and databases
Virtualization, data centers, distributed and cloud computing, fog and edge computing
Mobile and personal computing systems
Energy-efficient computing systems
Real-time and fault-tolerant systems
Security and privacy of computing and networked systems
Software systems and services, and enterprise applications
Social networks, metaverse, multimedia systems, Web services
Cyber-physical systems, including the smart grid
Analytical modeling techniques and model validation
Workload characterization and benchmarking
Performance, scalability, power and reliability analysis
Sustainability analysis and power management
System measurement, performance monitoring and forecasting
Anomaly detection, problem diagnosis and troubleshooting
Capacity planning, resource allocation, run time management and scheduling
Experimental design, statistical analysis, simulation
Game theory, network economics, and platform design
Machine learning, AI, Big data, data mining, graph analysis, optimization
Quantum computing
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