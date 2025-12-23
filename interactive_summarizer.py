"""
Interactive abstractive summarizer using BART-Large (facebook/bart-large-cnn).

Features:
- Single summary
- Paragraph-wise summary
- Long document summary
- Quick / detailed presets
- Structured summary: choose number of paragraphs and lines per paragraph
"""

import os
import sys
import time

# Allow importing summarizer.py from same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from summarizer import BartLargeAbstractiveSummarizer
from nltk.tokenize import sent_tokenize, word_tokenize


class InteractiveSummarizer:
    def __init__(self):
        self.summarizer = None
        self.clear_screen()

    # ----------------- Utility UI methods -----------------

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        print("=" * 70)
        print("ABSTRACTIVE TEXT SUMMARIZER (BART-Large)".center(70))
        print("=" * 70)
        print("Model: facebook/bart-large-cnn")
        print("This tool creates rephrased, abstractive summaries.")
        print("=" * 70)
        print()

    def show_main_menu(self):
        print("MAIN MENU")
        print("-" * 70)
        print("1. Enter text manually")
        print("2. Load text from file")
        print("3. Help / instructions")
        print("4. Exit")
        print("-" * 70)

    # ----------------- Input methods -----------------

    def get_text_manually(self):
        print("\nEnter/paste your text below.")
        print("Press Enter twice on an empty line to finish.\n")

        lines = []
        empty_count = 0

        while True:
            try:
                line = input()
            except EOFError:
                break

            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append("")
            else:
                empty_count = 0
                lines.append(line)

        text = "\n".join(lines).strip()
        return text if text else None

    def get_text_from_file(self):
        print("\nLOAD TEXT FROM FILE")
        print("-" * 70)
        path = input("Enter file path (default: input.txt): ").strip()
        if not path:
            path = "input.txt"

        if not os.path.exists(path):
            print(f"\nError: file '{path}' not found.")
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"\nError reading file: {e}")
            return None

        print(f"\nLoaded file: {path}")
        print(f"Characters: {len(text):,}  |  Words: {len(text.split()):,}")
        return text

    # ----------------- Mode selection -----------------

    def get_summarization_mode(self):
        print("\nSUMMARIZATION MODES")
        print("-" * 70)
        print("1. Single summary (recommended)")
        print("2. Paragraph-by-paragraph summary")
        print("3. Long document mode")
        print("4. Quick summary (shorter)")
        print("5. Detailed summary (longer)")
        print("6. Structured summary (paragraphs + lines)")
        print("-" * 70)

        while True:
            choice = input("Choose mode (1-6): ").strip()

            if choice == "1":
                return {"mode": "single", "max_len": 150, "min_len": 40}
            elif choice == "2":
                return {"mode": "paragraphs", "max_len": 80, "min_len": 20}
            elif choice == "3":
                return {"mode": "long", "max_len": 180, "min_len": 60}
            elif choice == "4":
                return {"mode": "quick", "max_len": 80, "min_len": 30}
            elif choice == "5":
                return {"mode": "detailed", "max_len": 220, "min_len": 70}
            elif choice == "6":
                return {"mode": "structured"}
            else:
                print("Invalid choice. Please enter a number from 1 to 6.")

    def get_structured_params(self):
        """Ask user for number of paragraphs and lines per paragraph."""
        print("\nSTRUCTURED SUMMARY SETTINGS")
        print("-" * 70)

        while True:
            try:
                num_paras = int(input("Number of paragraphs (1-10): ").strip())
                if 1 <= num_paras <= 10:
                    break
                print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            try:
                lines_per_para = int(
                    input("Approx. lines per paragraph (1-6): ").strip()
                )
                if 1 <= lines_per_para <= 6:
                    break
                print("Please enter a number between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        return num_paras, lines_per_para

    # ----------------- Summarization logic -----------------

    def ensure_model_loaded(self):
        if self.summarizer is None:
            print("\nLoading BART-Large model. This may take some time...")
            self.summarizer = BartLargeAbstractiveSummarizer()
            print("Model loaded successfully.\n")

    def summarize_text(self, text, mode_info):
        """Run summarization according to selected mode."""
        self.ensure_model_loaded()
        start_time = time.time()

        mode = mode_info["mode"]

        if mode == "structured":
            num_paras, lines_per_para = self.get_structured_params()
            summary = self.summarizer.summarize_structured(
                text,
                num_paragraphs=num_paras,
                lines_per_paragraph=lines_per_para,
            )

        elif mode == "paragraphs":
            summary = self.summarizer.summarize_paragraphs(text)

        elif mode == "long":
            summary = self.summarizer.summarize_long_document(text)

        else:
            summary = self.summarizer.summarize(
                text,
                max_length=mode_info["max_len"],
                min_length=mode_info["min_len"],
            )

        elapsed = time.time() - start_time
        return summary, elapsed

    # ----------------- Display results -----------------

    def display_results(self, original_text, summary, elapsed_seconds):
        self.clear_screen()
        self.print_header()

        # Stats
        orig_words = len(word_tokenize(original_text))
        sum_words = len(word_tokenize(summary))
        orig_sents = len(sent_tokenize(original_text))
        sum_sents = len(sent_tokenize(summary))
        reduction = ((orig_words - sum_words) / orig_words * 100) if orig_words else 0

        print("SUMMARY (FULL)")
        print("-" * 70)
        print(summary)
        print("-" * 70)
        print(f"Time taken: {elapsed_seconds:.2f} seconds\n")

        print("STATISTICS")
        print("-" * 70)
        print(f"Original: {orig_words} words, {orig_sents} sentences")
        print(f"Summary:  {sum_words} words, {sum_sents} sentences")
        print(f"Reduction: {reduction:.1f}%")
        print("-" * 70)

        print("\nFULL ORIGINAL TEXT")
        print("-" * 70)
        print(original_text)
        print("-" * 70)

    # ----------------- Help text -----------------

    def show_help(self):
        self.clear_screen()
        self.print_header()

        print("HELP / INSTRUCTIONS")
        print("-" * 70)
        print("This tool uses BART-Large CNN to generate abstractive summaries.")
        print("Choose structured mode to set paragraphs/lines manually.")
        print("Works best with 100–1200 words.")
        print("-" * 70)

        input("\nPress Enter to return to menu...")

    # ----------------- Main loop -----------------

    def run(self):
        self.clear_screen()
        self.print_header()
        input("Press Enter to start...")

        while True:
            self.clear_screen()
            self.print_header()
            self.show_main_menu()

            choice = input("\nEnter choice (1-4): ").strip()

            if choice == "1":
                text = self.get_text_manually()
            elif choice == "2":
                text = self.get_text_from_file()
            elif choice == "3":
                self.show_help()
                continue
            elif choice == "4":
                print("\nGoodbye!\n")
                break
            else:
                print("Invalid choice.")
                time.sleep(1)
                continue

            if not text:
                print("No text entered.")
                time.sleep(1)
                continue

            mode_info = self.get_summarization_mode()
            summary, elapsed = self.summarize_text(text, mode_info)
            self.display_results(text, summary, elapsed)

            again = input("\nSummarize another? (y/n): ").strip().lower()
            if again != "y":
                print("\nGoodbye!\n")
                break


# ----------------- Dependency check -----------------

def check_dependencies():
    required = ["torch", "transformers", "nltk"]
    missing = []

    for pkg in required:
        try:
            __import__(pkg)
        except:
            missing.append(pkg)

    if missing:
        print("Missing packages:", ", ".join(missing))
        print("Install using: pip install torch transformers nltk")
        return False

    return True


def main():
    print("Checking dependencies...")
    if not check_dependencies():
        input("Press Enter to exit...")
        return

    app = InteractiveSummarizer()
    app.run()


if __name__ == "__main__":
    main()
