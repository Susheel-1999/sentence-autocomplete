from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch


class SentenceCompleter:
    """AI-powered sentence completion using GPT-2."""

    def __init__(self, model_name: str = "gpt2"):
        print(f"Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto" if torch.cuda.is_available() else None,
        )
        print("✓ Model loaded successfully")

    def complete(
        self,
        prompt: str,
        max_new_tokens: int = 20,
        top_k: int = 50,
        top_p: float = 0.95,
        temperature: float = 0.7,
        num_return_sequences: int = 1,
    ) -> List[str]:
        """Generate sentence completions."""
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        outputs = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            num_return_sequences=num_return_sequences,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        completions = [out["generated_text"].strip() for out in outputs]
        
        for idx, text in enumerate(completions, 1):
            print(f"[{idx}] {text}")
        
        return completions

def build_default_completer() -> SentenceCompleter:
    return SentenceCompleter()
