"""Command-line interface for sentence autocomplete."""
import argparse
import logging
from .autocomplete import SentenceAutocomplete


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Sentence Autocomplete - Generate completions for partial sentences"
    )
    parser.add_argument(
        "sentence",
        type=str,
        help="Partial sentence to complete"
    )
    parser.add_argument(
        "-n", "--num-completions",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Number of completions to generate (default: 3)"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=1.0,
        help="Temperature for sampling (default: 1.0, higher = more random)"
    )
    parser.add_argument(
        "-k", "--top-k",
        type=int,
        default=50,
        help="Top-k sampling parameter (default: 50, 0 to disable)"
    )
    parser.add_argument(
        "-p", "--top-p",
        type=float,
        default=0.95,
        help="Top-p (nucleus) sampling parameter (default: 0.95)"
    )
    parser.add_argument(
        "-m", "--max-length",
        type=int,
        default=50,
        help="Maximum length of generated text (default: 50)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt2",
        help="Model name to use (default: gpt2)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging level
    log_level = logging.DEBUG if args.verbose else logging.INFO

    # Initialize autocomplete system
    autocomplete = SentenceAutocomplete(
        model_name=args.model,
        log_level=log_level
    )

    # Generate completions
    completions = autocomplete.complete(
        partial_sentence=args.sentence,
        num_completions=args.num_completions,
        max_length=args.max_length,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p
    )

    # Display results
    print("\n" + "="*80)
    print(f"Input: {args.sentence}")
    print("="*80)
    for i, completion in enumerate(completions, 1):
        print(f"\nCompletion {i}:")
        print(f"  {completion}")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
