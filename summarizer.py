"""
Abstractive Text Summarizer using BART-Large (facebook/bart-large-cnn)
More powerful and more abstractive than DistilBART.
Optimized to run safely on CPU-only or low-VRAM GPUs.
"""

import re
import sys
import warnings
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm
import logging

warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("summarizer.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class BartLargeAbstractiveSummarizer:
    """
    Strong abstractive summarizer using BART-Large (facebook/bart-large-cnn).

    Methods:
      - summarize(text): single abstractive summary
      - summarize_long_document(text): handles long inputs via chunking
      - summarize_paragraphs(text): paragraph-wise summarization
      - summarize_structured(text, num_paragraphs, lines_per_paragraph): 
            structured multi-paragraph summary
    """

    def __init__(
        self,
        model_name: str = "facebook/bart-large-cnn",
        use_gpu: bool = True,
    ):
        logger.info(f"Initializing BartLargeAbstractiveSummarizer with model: {model_name}")

        try:
            self._download_nltk_data()
            self.device = self._setup_device(use_gpu)
            logger.info(f"Using device: {self.device}")

            logger.info("Loading tokenizer and model...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

            self.model_name = model_name
            self.config = {
                "max_input_length": 1024,
                "default_max_length": 150,
                "default_min_length": 40,
                "temperature": 1.2,
                "repetition_penalty": 1.1,
                "length_penalty": 2.0,
            }

            logger.info(f"Model loaded successfully: {model_name}")
            logger.info(f"Vocab size: {self.tokenizer.vocab_size:,}")

        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            raise

    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------

    def _download_nltk_data(self):
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            logger.info("Downloading NLTK punkt data...")
            nltk.download("punkt", quiet=True)

    def _setup_device(self, use_gpu: bool):
        """
        BART-Large needs ~4GB+ VRAM for GPU.
        If VRAM < 4GB → force CPU for safety.
        """
        if use_gpu and torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = props.total_memory / (1024 ** 3)

            logger.info(f"GPU detected: {gpu_name}")
            logger.info(f"GPU VRAM: {vram_gb:.2f} GB")

            if vram_gb < 4.0:
                logger.info("VRAM too low for BART-Large → using CPU instead.")
                return torch.device("cpu")
            return torch.device("cuda")

        logger.info("Using CPU")
        return torch.device("cpu")

    # ------------------------------------------------------------------
    # Core summarization (single summary)
    # ------------------------------------------------------------------

    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 40,
        temperature: float = 1.2,
    ) -> str:
        """Generate a strongly abstractive summary for a single text."""
        try:
            text = self._clean_text(text)
            if len(text.strip()) < 30:
                return text.strip()

            logger.info(f"Summarizing text ({len(word_tokenize(text))} words)...")

            inputs = self.tokenizer(
                [text],
                max_length=self.config["max_input_length"],
                truncation=True,
                padding="longest",
                return_tensors="pt",
            ).to(self.device)

            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    # Abstractive settings: sampling instead of beams
                    do_sample=True,
                    num_beams=1,
                    top_k=80,
                    top_p=0.9,
                    temperature=temperature,
                    repetition_penalty=self.config["repetition_penalty"],
                    no_repeat_ngram_size=3,
                    length_penalty=self.config["length_penalty"],
                )

            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary.strip()

        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise

    # ------------------------------------------------------------------
    # Long document summarization
    # ------------------------------------------------------------------

    def summarize_long_document(self, text: str, chunk_size: int = 900) -> str:
        """
        Summarize long documents by splitting into chunks and summarizing chunks,
        then summarizing the combined summaries.
        """
        logger.info("Handling long document...")

        text = self._clean_text(text)
        chunks = self._split_into_chunks(text, chunk_size)

        if len(chunks) == 1:
            return self.summarize(chunks[0])

        summaries: List[str] = []
        for chunk in tqdm(chunks, desc="Summarizing chunks"):
            try:
                summaries.append(self.summarize(chunk, max_length=130, min_length=40))
            except Exception as e:
                logger.warning(f"Chunk failed: {e}")
                continue

        combined = " ".join(summaries)
        # Final pass to compress combined
        final = self.summarize(combined, max_length=180, min_length=60)
        return final

    # ------------------------------------------------------------------
    # Paragraph-wise summarization
    # ------------------------------------------------------------------

    def summarize_paragraphs(self, text: str, max_length_per_para: int = 80) -> str:
        """
        Summarize each paragraph separately, then join.
        """
        text = self._clean_text(text)
        paragraphs = self._extract_paragraphs(text)

        if not paragraphs:
            return self.summarize(text, max_length=max_length_per_para)

        results: List[str] = []
        for para in paragraphs:
            try:
                if len(para.split()) < 15:
                    results.append(para.strip())
                else:
                    results.append(
                        self.summarize(
                            para,
                            max_length=max_length_per_para,
                            min_length=20,
                        )
                    )
            except Exception as e:
                logger.warning(f"Paragraph failed: {e}")
                results.append(para.strip())

        return " ".join(results)

    # ------------------------------------------------------------------
    # NEW: Structured multi-paragraph summary
    # ------------------------------------------------------------------

    def summarize_structured(
        self,
        text: str,
        num_paragraphs: int = 2,
        lines_per_paragraph: int = 3,
        temperature: float = 1.2,
    ) -> str:
        """
        Generate a structured summary with approx:
          - num_paragraphs paragraphs
          - lines_per_paragraph sentences in each paragraph (approx).

        Strategy:
          1) Generate one long abstractive summary.
          2) Split into sentences.
          3) Group sentences into N paragraphs.
        """
        text = self._clean_text(text)

        # Heuristic: estimate how long the summary should be in tokens
        target_sentences = max(1, num_paragraphs * lines_per_paragraph)
        approx_tokens = target_sentences * 22  # ~22 tokens per sentence
        max_len = int(max(60, min(approx_tokens, 350)))
        min_len = int(max(30, min(approx_tokens * 0.5, 200)))

        logger.info(
            f"Structured summary → target_paras={num_paragraphs}, "
            f"target_lines_per_para={lines_per_paragraph}, "
            f"max_len={max_len}, min_len={min_len}"
        )

        # 1) Get one long summary
        long_summary = self.summarize(
            text,
            max_length=max_len,
            min_length=min_len,
            temperature=temperature,
        )

        # 2) Split into sentences
        sentences = [s.strip() for s in sent_tokenize(long_summary) if s.strip()]
        if not sentences:
            return long_summary

        total_sents = len(sentences)
        num_paragraphs = max(1, min(num_paragraphs, total_sents))

        paragraphs: List[str] = []
        idx = 0

        for p in range(num_paragraphs):
            remaining_sents = total_sents - idx
            remaining_paras = num_paragraphs - p

            if remaining_paras <= 0 or remaining_sents <= 0:
                break

            # Aim for lines_per_paragraph, but ensure we don't run out before the last para
            min_for_this = max(1, remaining_sents - (remaining_paras - 1) * lines_per_paragraph)
            s_for_this = min(lines_per_paragraph, remaining_sents, min_for_this)

            para_sents = sentences[idx : idx + s_for_this]
            idx += s_for_this

            paragraphs.append(" ".join(para_sents))

        # If any leftover sentences, attach to last paragraph
        if idx < total_sents and paragraphs:
            leftover = " ".join(sentences[idx:])
            paragraphs[-1] = paragraphs[-1] + " " + leftover

        # Join with blank lines between paragraphs
        structured_summary = "\n\n".join(paragraphs)
        return structured_summary.strip()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text.strip())
        text = re.sub(r"[\x00-\x1F\x7F]", "", text)
        return text

    def _split_into_chunks(self, text: str, chunk_size: int) -> List[str]:
        sentences = sent_tokenize(text)
        chunks: List[str] = []
        current = ""

        for s in sentences:
            if len(current) + len(s) <= chunk_size:
                current += s + " "
            else:
                if current:
                    chunks.append(current.strip())
                current = s + " "

        if current:
            chunks.append(current.strip())

        return chunks

    def _extract_paragraphs(self, text: str) -> List[str]:
        paras = re.split(r"\n\s*\n", text)
        paras = [p.strip() for p in paras if len(p.strip()) > 0]
        if not paras:
            return [text.strip()]
        return paras

    def clear_cache(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("GPU cache cleared")

    def __del__(self):
        try:
            self.clear_cache()
        except Exception:
            pass
