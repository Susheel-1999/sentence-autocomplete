"""Core autocomplete functionality using pre-trained language models."""
import logging
from typing import List, Optional
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class SentenceAutocomplete:
    """Sentence autocompletion system using GPT-2."""

    def __init__(
        self,
        model_name: str = "gpt2",
        device: Optional[str] = None,
        log_level: int = logging.INFO
    ):
        """
        Initialize the sentence autocomplete system.

        Args:
            model_name: Name of the pre-trained model to use (default: "gpt2")
            device: Device to run the model on ("cpu" or "cuda"). Auto-detected if None.
            log_level: Logging level
        """
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info(f"Initializing SentenceAutocomplete with model: {model_name}")

        # Setup device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        self.logger.info(f"Using device: {self.device}")

        # Load model and tokenizer
        self.logger.info("Loading tokenizer and model...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        self.logger.info("Model loaded successfully")

    def complete(
        self,
        partial_sentence: str,
        num_completions: int = 3,
        max_length: int = 50,
        temperature: float = 1.0,
        top_k: int = 50,
        top_p: float = 0.95,
        num_return_sequences: int = 3
    ) -> List[str]:
        """
        Generate sentence completions for a partial sentence.

        Args:
            partial_sentence: The incomplete sentence to complete
            num_completions: Number of completions to return (1-3)
            max_length: Maximum length of generated text
            temperature: Temperature for sampling (higher = more random)
            top_k: Top-k sampling parameter (0 to disable)
            top_p: Top-p (nucleus) sampling parameter
            num_return_sequences: Number of sequences to generate

        Returns:
            List of completed sentences
        """
        self.logger.info(f"Generating completions for: '{partial_sentence}'")
        self.logger.info(
            f"Parameters - temp: {temperature}, top_k: {top_k}, "
            f"top_p: {top_p}, max_length: {max_length}"
        )

        # Encode input
        input_ids = self.tokenizer.encode(partial_sentence, return_tensors="pt")
        input_ids = input_ids.to(self.device)

        # Generate completions
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_length=max_length,
                num_return_sequences=min(num_return_sequences, num_completions),
                temperature=temperature,
                top_k=top_k if top_k > 0 else None,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                early_stopping=True
            )

        # Decode outputs
        completions = []
        for i, output in enumerate(outputs):
            completed_text = self.tokenizer.decode(output, skip_special_tokens=True)
            completions.append(completed_text)
            self.logger.info(f"Completion {i+1}: {completed_text}")

        return completions[:num_completions]
