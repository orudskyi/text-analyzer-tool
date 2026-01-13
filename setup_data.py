from pathlib import Path


raw_text = """
Artificial Intelligence (AI) is transforming the world! 
But... what is AI? It is a broad field. Machine Learning (ML) is a subset of AI.

To start with ML, you need data. DATA is the new oil. 
However, raw data is often "dirty". You must clean it... 
Cleaning data takes 80% of the time.

Python is the king of Data Science. Why Python? 
Because python is simple, and PYTHON has great libraries like Pandas and NumPy.
C# is great, but Python is better for ML.

Contact our support team at: support@ai-learning.org or hr@tech-corp.com.
Project start date: 2024-05-20. 
Deadline: 15/01/2025.

Is it hard? No! Is it fun? YES!!!
"""


def create_sample_file():

    file_path = Path("data/sample.txt")

    file_path.parent.mkdir(exist_ok=True)

    file_path.write_text(raw_text, encoding="utf-8")

    print(f"✅ File succesfully created: {file_path.absolute()}")


if __name__ == "__main__":
    create_sample_file()
