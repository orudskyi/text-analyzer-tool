import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from typing import Set


def read_file(file_path: Path) -> str:
    """Reads the content of a text file safely."""
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""


def clean_and_tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    """Normalizes text and splits into words."""
    text = text.lower()
    words = re.findall(r"\b\w+\b", text)

    if remove_stopwords:
        stop_words: Set[str] = {
            "the",
            "is",
            "a",
            "an",
            "and",
            "or",
            "but",
            "to",
            "of",
            "in",
            "on",
            "at",
            "it",
            "that",
            "this",
        }
        words = [word for word in words if word not in stop_words]

    return words


def generate_visualization(df: pd.DataFrame, output_path: Path):
    """
    Creates a bar chart of the top 10 words using Matplotlib.
    """
    # Take top 10 for the plot
    top_10 = df.head(10)

    # Create a figure (canvas)
    plt.figure(figsize=(10, 6))

    # Plot bar chart: x=word, y=count
    plt.bar(top_10["word"], top_10["count"], color="skyblue")

    plt.title("Top 10 Most Frequent Words", fontsize=14)
    plt.xlabel("Words", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=45)  # Rotate labels for better readability

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    # Save to file
    plt.savefig(output_path)
    print(f"[SUCCESS] Chart saved to: {output_path.absolute()}")

    # Close the plot to free memory
    plt.close()


def process_with_pandas(words: list[str]):
    """
    Main analysis logic using Pandas.
    Replaces the old 'analyze_frequencies' and 'create_report_string' logic.
    """
    # 1. Create a DataFrame (Imagine an Excel table with one column "word")
    df = pd.DataFrame(words, columns=["word"])

    if df.empty:
        print("No data to analyze.")
        return

    # 2. Calculate Frequencies
    # value_counts() is the Pandas equivalent of GroupBy + Count
    # reset_index() converts the result back to a nice table with columns 'word' and 'count'
    word_counts = df["word"].value_counts().reset_index()
    word_counts.columns = ["word", "count"]  # Rename columns explicitly

    # 3. Display Stats in Console
    print("\n" + "=" * 30)
    print("   PANDAS ANALYSIS REPORT")
    print("=" * 30)
    print(f"Total Words:  {len(df)}")
    print(f"Unique Words: {len(word_counts)}")
    print("-" * 30)
    print("Top 10 Words:")
    print(word_counts.head(10).to_string(index=False))  # to_string() formats it nicely
    print("=" * 30 + "\n")

    # 4. Save Report (CSV) - Standard Data format
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    csv_path = reports_dir / "word_stats.csv"
    word_counts.to_csv(csv_path, index=False)
    print(f"[SUCCESS] Data saved to CSV: {csv_path.absolute()}")

    # 5. Generate Visualization
    chart_path = reports_dir / "top_words_chart.png"
    generate_visualization(word_counts, chart_path)


def main():
    input_path = Path("data/sample.txt")
    print(f"--- Processing file: {input_path} ---")

    raw_text = read_file(input_path)
    if not raw_text:
        return

    tokens = clean_and_tokenize(raw_text, remove_stopwords=True)

    # Hand over control to Pandas logic
    process_with_pandas(tokens)


if __name__ == "__main__":
    main()
