"""
📝 INTERACTIVE ABSTRACTIVE SUMMARIZER
Run this file and follow the prompts to summarize any text!
"""

import sys
import os
import time
from pathlib import Path

# Ensure current directory is on sys.path so we can import summarizer.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from summarizer import PegasusAbstractiveSummarizer


class InteractiveSummarizer:
    def __init__(self):
        self.summarizer = None
        self.clear_screen()

    def clear_screen(self):
        """Clear terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        """Print header."""
        print("\n" + "=" * 70)
        print("🤖" + " " * 21 + "ABSTRACTIVE TEXT SUMMARIZER" + " " * 21 + "🤖")
        print("=" * 70)
        print("✨ Creates rephrased sentences (not just extracted ones)")
        print("✨ Powered by Google's Pegasus model")
        print("✨ Interactive and easy to use")
        print("=" * 70 + "\n")

    def show_menu(self):
        """Display main menu."""
        print("\n" + "═" * 50)
        print("📋 MAIN MENU")
        print("═" * 50)
        print("1. 📝 Enter text manually")
        print("2. 📂 Load from text file")
        print("3. 📄 Load from multiple files (coming soon)")
        print("4. 🔧 Settings & Options")
        print("5. ℹ️  Help & Instructions")
        print("6. 🚪 Exit")
        print("═" * 50)

    def get_text_manually(self):
        """Get text input from user."""
        print("\n" + "📝" + "─" * 48 + "📝")
        print("ENTER YOUR TEXT")
        print("(Press Enter twice when done)")
        print("─" * 50)

        lines = []
        empty_lines = 0

        print("\nStart typing (or paste) your text below:")
        print("-" * 50)

        try:
            while True:
                line = input()
                if line == "":
                    empty_lines += 1
                    # One empty line allowed as paragraph break, two = stop
                    if empty_lines >= 2:
                        break
                    else:
                        lines.append("")
                else:
                    empty_lines = 0
                    lines.append(line)
        except KeyboardInterrupt:
            print("\n⚠️ Input cancelled.")
            return None
        except EOFError:
            pass

        # Remove trailing empty lines
        while lines and lines[-1] == "":
            lines.pop()

        text = "\n".join(lines)
        return text if text.strip() else None

    def get_text_from_file(self):
        """Load text from a file."""
        print("\n📂 LOAD FROM FILE")
        print("-" * 50)

        while True:
            filepath = input(
                "\nEnter file path (or press Enter for 'input.txt'): "
            ).strip()
            if not filepath:
                filepath = "input.txt"

            if not os.path.exists(filepath):
                print(f"\n❌ File '{filepath}' not found!")
                print("\nAvailable files in current directory:")

                text_files = [
                    f
                    for f in os.listdir(".")
                    if f.endswith(".txt") or f.endswith(".md")
                ]

                if text_files:
                    for i, f in enumerate(text_files, 1):
                        print(f"  {i}. {f}")

                    choice = input(
                        "\nSelect a file number or enter new path (or 'b' to go back): "
                    ).strip()

                    if choice.lower() == "b":
                        return None
                    elif choice.isdigit() and 1 <= int(choice) <= len(text_files):
                        filepath = text_files[int(choice) - 1]
                    else:
                        continue
                else:
                    print("No text files found. Please create an 'input.txt' file first.")
                    create = input("Create sample 'input.txt' file? (y/n): ").lower()
                    if create == "y":
                        self.create_sample_file()
                        filepath = "input.txt"
                    else:
                        return None

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()

                print(f"✅ File loaded: {filepath}")
                print(f"📊 Size: {len(text):,} characters, ~{len(text.split()):,} words")

                print("\n📄 Preview (first 300 characters):")
                print("-" * 50)
                preview = text[:300] + "..." if len(text) > 300 else text
                print(preview)
                print("-" * 50)

                confirm = input("\n✅ Use this file? (y/n): ").lower()
                if confirm == "y":
                    return text
                else:
                    continue

            except UnicodeDecodeError:
                print("❌ Cannot read file (encoding issue). Try saving as UTF-8.")
            except Exception as e:
                print(f"❌ Error reading file: {str(e)}")
                return None

    def create_sample_file(self):
        """Create a sample input.txt file."""
        sample_text = """Artificial Intelligence in Modern Healthcare

Artificial intelligence is revolutionizing the healthcare industry by providing innovative solutions for diagnosis, treatment, and patient care. Machine learning algorithms can analyze medical images such as X-rays, MRIs, and CT scans with remarkable accuracy, often detecting abnormalities that human eyes might miss. This technology enables early diagnosis of diseases like cancer, Alzheimer's, and diabetic retinopathy.

In drug discovery, AI accelerates the process of identifying potential compounds and predicting their effectiveness. What traditionally took years can now be accomplished in months, significantly reducing research and development costs. Pharmaceutical companies are increasingly adopting AI-powered platforms to streamline their discovery pipelines.

Personalized medicine is another area where AI shines. By analyzing a patient's genetic information, medical history, and lifestyle factors, AI systems can recommend tailored treatment plans. This approach increases treatment effectiveness while minimizing side effects.

However, challenges remain in implementing AI in healthcare. Data privacy concerns, algorithmic bias, and the need for human oversight are critical issues that must be addressed. Regulatory bodies are working to establish guidelines that ensure the safe and ethical use of AI in medical settings.

Despite these challenges, the future of AI in healthcare looks promising. As technology advances and more data becomes available, AI will likely become an integral part of medical practice, improving outcomes and making healthcare more accessible worldwide."""
        try:
            with open("input.txt", "w", encoding="utf-8") as f:
                f.write(sample_text)
            print("✅ Created sample 'input.txt' file with healthcare AI text.")
        except Exception as e:
            print(f"❌ Failed to create file: {str(e)}")

    def get_summarization_method(self):
        """Let user choose summarization method."""
        print("\n🔧 SUMMARIZATION METHOD")
        print("-" * 50)
        print("1. 📄 Single summary (recommended for most texts)")
        print("2. 📑 Paragraph by paragraph (for structured documents)")
        print("3. 📚 Long document (auto-splits very long texts)")
        print("4. ⚡ Quick summary (shorter, faster)")
        print("5. 📊 Detailed summary (longer, more comprehensive)")
        print("-" * 50)

        while True:
            choice = input("\nChoose method (1-5): ").strip()

            if choice == "1":
                return {"method": "single", "max_len": 150, "min_len": 40}
            elif choice == "2":
                return {"method": "paragraphs", "max_len": 80, "min_len": 20}
            elif choice == "3":
                return {"method": "long", "max_len": 100, "min_len": 30}
            elif choice == "4":
                return {"method": "quick", "max_len": 80, "min_len": 20}
            elif choice == "5":
                return {"method": "detailed", "max_len": 200, "min_len": 60}
            else:
                print("❌ Invalid choice. Please enter 1-5.")

    def summarize_text(self, text, method_info):
        """Generate summary based on chosen method."""
        print("\n" + "⏳" + "─" * 48 + "⏳")
        print("GENERATING ABSTRACTIVE SUMMARY")
        print("─" * 50)

        try:
            if self.summarizer is None:
                print("🚀 Loading Pegasus model... (first time may take a minute)")
                self.summarizer = PegasusAbstractiveSummarizer()
                print("✅ Model loaded successfully!")

            start_time = time.time()

            if method_info["method"] == "paragraphs":
                print("📑 Summarizing paragraph by paragraph...")
                result = self.summarizer.summarize_paragraphs(
                    text,
                    max_length_per_para=method_info["max_len"],
                    return_details=True,
                )
                summary = result["full_summary"]

            elif method_info["method"] == "long":
                print("📚 Processing as long document...")
                summary = self.summarizer.summarize_long_document(text)

            else:
                print("📄 Generating single summary...")
                summary = self.summarizer.summarize(
                    text,
                    max_length=method_info["max_len"],
                    min_length=method_info["min_len"],
                )

            elapsed_time = time.time() - start_time

            from nltk.tokenize import word_tokenize, sent_tokenize

            orig_words = len(word_tokenize(text))
            summ_words = len(word_tokenize(summary))
            orig_sents = len(sent_tokenize(text))
            summ_sents = len(sent_tokenize(summary))
            reduction = ((orig_words - summ_words) / orig_words) * 100 if orig_words else 0

            return {
                "summary": summary,
                "original_words": orig_words,
                "summary_words": summ_words,
                "original_sentences": orig_sents,
                "summary_sentences": summ_sents,
                "reduction": reduction,
                "time": elapsed_time,
            }

        except Exception as e:
            print(f"\n❌ Error during summarization: {str(e)}")
            return None

    def display_results(self, text, results):
        """Display summarization results."""
        self.clear_screen()
        self.print_header()

        print("\n" + "✅" + "─" * 48 + "✅")
        print("SUMMARY GENERATED SUCCESSFULLY!")
        print("─" * 50)

        print(f"\n⏱️  Time taken: {results['time']:.2f} seconds")

        print("\n" + "📊" + "─" * 48 + "📊")
        print("STATISTICS")
        print("─" * 50)
        print(
            f"   Original: {results['original_words']} words, {results['original_sentences']} sentences"
        )
        print(
            f"   Summary:  {results['summary_words']} words, {results['summary_sentences']} sentences"
        )
        if results["summary_words"] > 0:
            print(f"   Reduction: {results['reduction']:.1f}%")
            print(
                f"   Compression: 1:{results['original_words'] // results['summary_words']}"
            )
        print("─" * 50)

        print("\n" + "📋" + "─" * 48 + "📋")
        print("ABSTRACTIVE SUMMARY")
        print("(Rephrased sentences, not extracted)")
        print("─" * 50)
        print(f"\n{results['summary']}\n")
        print("─" * 50)

        print("\n" + "📝" + "─" * 48 + "📝")
        print("ORIGINAL TEXT PREVIEW")
        print("─" * 50)
        preview = text[:200] + "..." if len(text) > 200 else text
        print(f"\n{preview}\n")
        print("─" * 50)

    def save_options(self, text, summary, results):
        """Handle saving options."""
        print("\n" + "💾" + "─" * 48 + "💾")
        print("SAVE OPTIONS")
        print("─" * 50)
        print("1. Save summary as text file (.txt)")
        print("2. Save as JSON with metadata (.json)")
        print("3. Save both original and summary")
        print("4. Copy summary to clipboard")
        print("5. Don't save")
        print("─" * 50)

        choice = input("\nChoose option (1-5): ").strip()

        if choice == "1":
            self.save_to_file(summary, "txt")
        elif choice == "2":
            self.save_to_file(summary, "json", text, results)
        elif choice == "3":
            self.save_both(text, summary, results)
        elif choice == "4":
            self.copy_to_clipboard(summary)
        else:
            print("💡 Summary not saved.")

    def save_to_file(self, summary, format_type, text=None, results=None):
        """Save summary to file."""
        from datetime import datetime
        import json

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format_type == "txt":
            filename = f"summary_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("ABSTRACTIVE SUMMARY\n")
                f.write("=" * 50 + "\n\n")
                f.write(summary)
                f.write("\n\n" + "=" * 50 + "\n")
                f.write(
                    f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )

            print(f"✅ Summary saved to: {filename}")

        elif format_type == "json":
            filename = f"summary_{timestamp}.json"

            data = {
                "timestamp": datetime.now().isoformat(),
                "original_text": text,
                "abstractive_summary": summary,
                "statistics": {
                    "original_words": results["original_words"],
                    "summary_words": results["summary_words"],
                    "original_sentences": results["original_sentences"],
                    "summary_sentences": results["summary_sentences"],
                    "reduction_percentage": results["reduction"],
                    "processing_time_seconds": results["time"],
                },
                "model": "google/pegasus-xsum",
            }

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Summary saved to: {filename}")

    def save_both(self, text, summary, results):
        """Save both original and summary."""
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_complete_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("ORIGINAL TEXT\n")
            f.write("=" * 60 + "\n\n")
            f.write(text)
            f.write("\n\n" + "=" * 60 + "\n\n\n")

            f.write("ABSTRACTIVE SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            f.write(summary)
            f.write("\n\n" + "=" * 60 + "\n\n")

            f.write("STATISTICS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Original words: {results['original_words']}\n")
            f.write(f"Summary words: {results['summary_words']}\n")
            f.write(f"Reduction: {results['reduction']:.1f}%\n")
            if results["summary_words"] > 0:
                f.write(
                    f"Compression ratio: 1:{results['original_words'] // results['summary_words']}\n"
                )
            f.write(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write("=" * 60)

        print(f"✅ Complete document saved to: {filename}")

    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        try:
            import pyperclip

            pyperclip.copy(text)
            print("✅ Summary copied to clipboard!")
        except ImportError:
            print("ℹ️  Install pyperclip for clipboard support:")
            print("   pip install pyperclip")
            print("\n📋 Summary text is above - you can manually copy it.")

    def show_help(self):
        """Display help instructions."""
        self.clear_screen()
        self.print_header()

        print("\n" + "❓" + "─" * 48 + "❓")
        print("HELP & INSTRUCTIONS")
        print("─" * 50)

        print("\n📖 ABOUT ABSTRACTIVE SUMMARIZATION:")
        print("-" * 50)
        print("Unlike extractive summarization (which picks existing sentences),")
        print("abstractive summarization creates NEW sentences that capture")
        print("the essence of the original text. It rephrases and rewrites!")

        print("\n🎯 BEST PRACTICES:")
        print("-" * 50)
        print("1. Input text should be coherent paragraphs")
        print("2. For best results, use 100–1000 words")
        print("3. Clear structure (paragraphs) improves quality")
        print("4. Remove unnecessary headers/footers")

        print("\n🔧 SUMMARIZATION METHODS:")
        print("-" * 50)
        print("📄 Single summary: Best for most documents")
        print("📑 Paragraph by paragraph: For structured papers/reports")
        print("📚 Long document: For books/very long texts")
        print("⚡ Quick summary: Brief overview")
        print("📊 Detailed summary: Comprehensive summary")

        print("\n💾 SAVING OPTIONS:")
        print("-" * 50)
        print(".txt: Simple text file with summary")
        print(".json: Structured data with metadata")
        print("Complete: Original + summary + statistics")

        input("\nPress Enter to continue...")

    def show_settings(self):
        """Display settings info."""
        self.clear_screen()
        self.print_header()

        print("\n" + "⚙️" + "─" * 48 + "⚙️")
        print("SETTINGS")
        print("─" * 50)

        print("\nCurrent settings:")
        print("Model: google/pegasus-xsum")
        print("Device: managed inside summarizer.py (CPU forced on low VRAM GPUs)")

        print("\nOptions:")
        print("1. Back to main menu")

        choice = input("\nChoose option (1): ").strip()
        # Just go back for now
        return

    def run(self):
        """Main interactive loop."""
        self.clear_screen()
        self.print_header()

        print("Welcome! This tool will help you create abstractive summaries.")
        print("First time? Choose option 5 for help.")
        input("\nPress Enter to start...")

        while True:
            self.clear_screen()
            self.print_header()
            self.show_menu()

            choice = input("\nEnter your choice (1-6): ").strip()
            text = None

            if choice == "1":
                text = self.get_text_manually()
                if text is None:
                    input("\nPress Enter to continue...")
                    continue

            elif choice == "2":
                text = self.get_text_from_file()
                if text is None:
                    input("\nPress Enter to continue...")
                    continue

            elif choice == "3":
                print("\n⚠️ Multiple files feature coming soon!")
                input("Press Enter to continue...")
                continue

            elif choice == "4":
                self.show_settings()
                continue

            elif choice == "5":
                self.show_help()
                continue

            elif choice == "6":
                print("\n👋 Thank you for using Abstractive Summarizer!")
                print("Goodbye!\n")
                break

            else:
                print("❌ Invalid choice. Please enter 1-6.")
                time.sleep(1)
                continue

            if text:
                method_info = self.get_summarization_method()
                results = self.summarize_text(text, method_info)

                if results:
                    self.display_results(text, results)
                    self.save_options(text, results["summary"], results)

                print("\n" + "🔄" + "─" * 48 + "🔄")
                again = input("Summarize another text? (y/n): ").lower()
                if again != "y":
                    print("\n👋 Thank you for using Abstractive Summarizer!")
                    break

            input("\nPress Enter to continue...")


def check_dependencies():
    """Check if all required packages are installed."""
    required = ["torch", "transformers", "nltk"]
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print("❌ Missing required packages:")
        for package in missing:
            print(f"   - {package}")
        print("\n💡 Install them with:")
        print("   pip install torch transformers nltk sentencepiece")
        return False

    return True


def main():
    """Main entry point."""
    print("\n🔍 Checking dependencies...")

    if not check_dependencies():
        print("\n⚠️ Please install missing packages and run again.")
        input("Press Enter to exit...")
        return

    try:
        app = InteractiveSummarizer()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("\n💡 If it's a model download issue, check your internet connection.")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
