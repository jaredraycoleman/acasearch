import pathlib
import re
import pyperclip

SUBJECTS = """
unsupervised, semi-supervised, and supervised representation learning
representation learning for planning and reinforcement learning
representation learning for computer vision and natural language processing
metric learning and kernel learning
sparse coding and dimensionality expansion
hierarchical models
optimization for representation learning
learning representations of outputs or states
optimal transport
theoretical issues in deep learning
visualization or interpretation of learned representations
implementation issues, parallelization, software platforms, hardware
applications in audio, speech, robotics, neuroscience, computational biology, or any other field
societal considerations of representation learning including fairness, safety, privacy, and interpretability
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