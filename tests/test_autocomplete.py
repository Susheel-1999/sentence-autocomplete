"""Tests for the autocomplete module."""
import unittest
import sys
import os

# Add parent directory to path to import src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.autocomplete import SentenceAutocomplete


class TestSentenceAutocomplete(unittest.TestCase):
    """Test cases for SentenceAutocomplete class."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are expensive to create."""
        # Use a small model for testing
        cls.autocomplete = SentenceAutocomplete(model_name="gpt2")

    def test_initialization(self):
        """Test that the autocomplete system initializes correctly."""
        self.assertIsNotNone(self.autocomplete.model)
        self.assertIsNotNone(self.autocomplete.tokenizer)
        self.assertIn(self.autocomplete.device, ["cpu", "cuda"])

    def test_basic_completion(self):
        """Test basic sentence completion."""
        partial_sentence = "The meeting is scheduled to"
        completions = self.autocomplete.complete(
            partial_sentence,
            num_completions=1,
            max_length=30
        )
        
        self.assertEqual(len(completions), 1)
        self.assertTrue(completions[0].startswith(partial_sentence))
        self.assertGreater(len(completions[0]), len(partial_sentence))

    def test_multiple_completions(self):
        """Test generating multiple completions."""
        partial_sentence = "I think that"
        completions = self.autocomplete.complete(
            partial_sentence,
            num_completions=3,
            max_length=25
        )
        
        self.assertEqual(len(completions), 3)
        for completion in completions:
            self.assertTrue(completion.startswith(partial_sentence))

    def test_temperature_control(self):
        """Test that temperature parameter is accepted."""
        partial_sentence = "Hello, my name is"
        
        # Low temperature (more deterministic)
        completions_low = self.autocomplete.complete(
            partial_sentence,
            num_completions=1,
            temperature=0.5,
            max_length=20
        )
        
        # High temperature (more random)
        completions_high = self.autocomplete.complete(
            partial_sentence,
            num_completions=1,
            temperature=1.5,
            max_length=20
        )
        
        self.assertEqual(len(completions_low), 1)
        self.assertEqual(len(completions_high), 1)

    def test_top_k_sampling(self):
        """Test top-k sampling parameter."""
        partial_sentence = "The weather today is"
        completions = self.autocomplete.complete(
            partial_sentence,
            num_completions=2,
            top_k=10,
            max_length=25
        )
        
        self.assertEqual(len(completions), 2)

    def test_top_p_sampling(self):
        """Test top-p (nucleus) sampling parameter."""
        partial_sentence = "In my opinion"
        completions = self.autocomplete.complete(
            partial_sentence,
            num_completions=2,
            top_p=0.9,
            max_length=25
        )
        
        self.assertEqual(len(completions), 2)


if __name__ == "__main__":
    unittest.main()
