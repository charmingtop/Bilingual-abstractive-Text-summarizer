"""
Unit tests for the abstractive summarizer.
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from summarizer import PegasusAbstractiveSummarizer

class TestSummarizer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize summarizer once for all tests."""
        cls.summarizer = PegasusAbstractiveSummarizer(use_gpu=False)
    
    def test_short_text(self):
        """Test summarization of short text."""
        text = "Artificial intelligence is transforming industries worldwide."
        summary = self.summarizer.summarize(text)
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)
    
    def test_paragraph_extraction(self):
        """Test paragraph extraction."""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        paragraphs = self.summarizer._extract_paragraphs(text)
        self.assertEqual(len(paragraphs), 3)
    
    def test_text_cleaning(self):
        """Test text cleaning function."""
        text = "  Extra   spaces  \n\nand newlines  "
        cleaned = self.summarizer._clean_text(text)
        self.assertNotIn("\n\n", cleaned)
        self.assertEqual(cleaned.count(" "), 4)  # Normalized spaces
    
    def test_statistics_calculation(self):
        """Test statistics calculation."""
        original = "This is a test. It has multiple sentences."
        summary = "Test summary."
        stats = self.summarizer._calculate_statistics(original, summary)
        self.assertIn("original_words", stats)
        self.assertIn("summary_words", stats)
        self.assertIn("reduction_percentage", stats)

if __name__ == '__main__':
    unittest.main()