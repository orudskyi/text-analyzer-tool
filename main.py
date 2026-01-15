from collections import Counter
from pathlib import Path
import re


def read_file(file_path: Path) -> str:
    """
    Reads the content of a text file safely.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return ""
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return ""


def clean_and_tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    """
    Normalizes text and splits it into a list of words.
    
    Processing steps:
    1. Convert to lowercase (normalization).
    2. Use Regex to find words (removes punctuation).
    """
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    
    if remove_stopwords:
        stop_words: set[str] = {
            "the", "is", "a", "an", "and", "or", "but", 
            "to", "of", "in", "on", "at", "it", "that", "this"
        }
        
        words = [word for word in words if word not in stop_words]
    
    return words

def extract_emails(text: str) -> list[str]:
    """
    Finds all email addresses using a Regular Expression.
    """
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


def analyze_frequencies(words: list[str]) -> Counter:
    """Counts word occurrences"""
    return Counter(words)

def create_report_string(
    total_words: int,
    unique_words: int,
    top_words: list[tuple],
    emails: list[str]
) -> str:
    """
    Generates the report as a single string.
    """
    lines = []
    lines.append("="*30)
    lines.append("   TEXT ANALYSIS REPORT")
    lines.append("="*30)
    lines.append(f"Total Words (clean): {total_words}")
    lines.append(f"Unique Words:        {unique_words}")
    
    lines.append("-" * 30)
    lines.append("Top 10 Most Frequent Words:")
    for rank, (word, count) in enumerate(top_words, start=1):
        lines.append(f"{rank}. {word:<15} : {count}")
        
    lines.append("-" * 30)
    lines.append(f"Found Emails ({len(emails)}):")
    if emails:
        for email in emails:
            lines.append(f"- {email}")
    else:
        lines.append("No emails found.")
        
    lines.append("="*30)
    
    # Join all lines with a newline character
    return "\n".join(lines)

def save_report_to_file(report_content: str, filename: str = "report.txt"):
    """Saves the report string to a file."""
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    try:
        # mode='w' creates the file or overwrites it if it exists
        with open(output_path, mode='w', encoding='utf-8') as file:
            file.write(report_content)
        print(f"\n[SUCCESS] Report saved to: {output_path.absolute()}")
    except Exception as e:
        print(f"\n[ERROR] Could not save report: {e}")

def main():
    """Main execution flow."""
    input_path = Path("data/sample.txt")
    print(f"--- Processing file: {input_path} ---")
    
    # 1. Extract
    raw_text = read_file(input_path)
    if not raw_text:
        return

    # 2. Transform & Mining
    tokens = clean_and_tokenize(raw_text, remove_stopwords=True)
    emails = extract_emails(raw_text) 
    
    # 3. Analyze
    word_stats = analyze_frequencies(tokens)
    top_10 = word_stats.most_common(10)
    
    # 4. Generate Report
    report = create_report_string(
        total_words=sum(word_stats.values()), 
        unique_words=len(word_stats), 
        top_words=top_10,
        emails=emails
    )
    
    # 5. Output (Print & Save)
    print(report)
    save_report_to_file(report)


if __name__ == "__main__":
    main()
