"""
Example usage of the sentence autocomplete system.

This script demonstrates how to use the SentenceAutocomplete API.
"""
from src.autocomplete import SentenceAutocomplete


def main():
    """Run example completions."""
    print("="*80)
    print("Sentence Autocomplete - Example Usage")
    print("="*80)
    
    # Initialize the system
    print("\n1. Initializing SentenceAutocomplete with GPT-2...")
    autocomplete = SentenceAutocomplete(model_name="gpt2")
    print("   ✓ Model loaded successfully")
    
    # Example 1: Basic completion
    print("\n2. Example 1: Basic completion")
    print("-" * 40)
    partial_sentence = "The meeting is scheduled to"
    print(f"   Input: '{partial_sentence}'")
    completions = autocomplete.complete(
        partial_sentence=partial_sentence,
        num_completions=3,
        max_length=40
    )
    for i, completion in enumerate(completions, 1):
        print(f"   Completion {i}: {completion}")
    
    # Example 2: With temperature control (more creative)
    print("\n3. Example 2: Creative completion (high temperature)")
    print("-" * 40)
    partial_sentence = "I believe that"
    print(f"   Input: '{partial_sentence}'")
    completions = autocomplete.complete(
        partial_sentence=partial_sentence,
        num_completions=2,
        temperature=1.5,  # Higher temperature = more creative
        max_length=35
    )
    for i, completion in enumerate(completions, 1):
        print(f"   Completion {i}: {completion}")
    
    # Example 3: With top-k sampling (focused)
    print("\n4. Example 3: Focused completion (top-k sampling)")
    print("-" * 40)
    partial_sentence = "The best way to learn is"
    print(f"   Input: '{partial_sentence}'")
    completions = autocomplete.complete(
        partial_sentence=partial_sentence,
        num_completions=2,
        temperature=0.7,  # Lower temperature = more focused
        top_k=20,  # Consider only top 20 tokens
        max_length=35
    )
    for i, completion in enumerate(completions, 1):
        print(f"   Completion {i}: {completion}")
    
    # Example 4: With top-p (nucleus) sampling
    print("\n5. Example 4: Nucleus sampling (top-p)")
    print("-" * 40)
    partial_sentence = "In the future,"
    print(f"   Input: '{partial_sentence}'")
    completions = autocomplete.complete(
        partial_sentence=partial_sentence,
        num_completions=2,
        top_p=0.9,  # Consider tokens in top 90% probability mass
        max_length=35
    )
    for i, completion in enumerate(completions, 1):
        print(f"   Completion {i}: {completion}")
    
    print("\n" + "="*80)
    print("Examples completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
