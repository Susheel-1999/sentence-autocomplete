# Sentence Autocomplete

A sentence autocompletion system that generates 1–3 plausible completions for a given partial sentence using pre-trained language models like GPT-2.

## Features

- **Multiple Completions**: Generate 1-3 meaningful sentence completions
- **Pre-trained Models**: Uses GPT-2 (easily extensible to GPT-Neo, T5, etc.)
- **Sampling Control**:
  - Top-k sampling for limiting vocabulary choices
  - Top-p (nucleus) sampling for dynamic vocabulary selection
  - Temperature control for creativity vs. determinism
- **Logging**: Comprehensive logging of inputs, parameters, and generated outputs
- **CLI Interface**: Easy-to-use command-line interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Susheel-1999/sentence-autocomplete.git
cd sentence-autocomplete
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **First Run**: The system will automatically download the GPT-2 model from HuggingFace on first use. This requires an internet connection and may take a few minutes. The model will be cached locally for future use.

## Usage

### Command Line Interface

Basic usage:
```bash
python -m src.cli "The meeting is scheduled to"
```

With custom parameters:
```bash
python -m src.cli "The meeting is scheduled to" \
  --num-completions 3 \
  --temperature 1.0 \
  --top-k 50 \
  --top-p 0.95 \
  --max-length 50
```

### Python API

```python
from src.autocomplete import SentenceAutocomplete

# Initialize the system
autocomplete = SentenceAutocomplete(model_name="gpt2")

# Generate completions
completions = autocomplete.complete(
    partial_sentence="The meeting is scheduled to",
    num_completions=3,
    temperature=1.0,
    top_k=50,
    top_p=0.95,
    max_length=50
)

# Print results
for i, completion in enumerate(completions, 1):
    print(f"Completion {i}: {completion}")
```

## Parameters

- `partial_sentence`: The incomplete sentence to complete (required)
- `num_completions`: Number of completions to generate (1-3, default: 3)
- `temperature`: Controls randomness (0.1-2.0, default: 1.0)
  - Lower values (0.5): More focused, deterministic outputs
  - Higher values (1.5+): More creative, diverse outputs
- `top_k`: Top-k sampling - consider only top k tokens (default: 50)
  - Set to 0 to disable
- `top_p`: Nucleus sampling - cumulative probability threshold (default: 0.95)
  - Range: 0.0-1.0
- `max_length`: Maximum length of generated text (default: 50)

## Quick Start

Run the example script to see the system in action:
```bash
python example.py
```

This will demonstrate various features including basic completion, temperature control, top-k sampling, and top-p (nucleus) sampling.

## Examples

### Example 1: Default Parameters
```bash
python -m src.cli "The weather today is"
```

Output:
```
================================================================================
Input: The weather today is
================================================================================

Completion 1:
  The weather today is expected to be sunny with temperatures in the 70s.

Completion 2:
  The weather today is quite nice, perfect for outdoor activities.

Completion 3:
  The weather today is cloudy with a chance of rain later this afternoon.
================================================================================
```

### Example 2: More Creative (Higher Temperature)
```bash
python -m src.cli "I believe that" --temperature 1.5 --num-completions 2
```

### Example 3: More Focused (Lower Temperature, Top-k)
```bash
python -m src.cli "The best way to learn is" --temperature 0.7 --top-k 20
```

## Configuration

Edit `config.json` to change default parameters:

```json
{
  "model_name": "gpt2",
  "default_parameters": {
    "num_completions": 3,
    "max_length": 50,
    "temperature": 1.0,
    "top_k": 50,
    "top_p": 0.95
  }
}
```

## Testing

Run the test suite:
```bash
python -m unittest discover tests
```

Run specific tests:
```bash
python -m unittest tests.test_autocomplete
```

## Requirements

- Python 3.7+
- PyTorch 2.0+
- Transformers 4.30+

## Architecture

The system consists of three main components:

1. **SentenceAutocomplete** (`src/autocomplete.py`): Core functionality
   - Model loading and initialization
   - Text generation with sampling strategies
   - Logging and monitoring

2. **CLI Interface** (`src/cli.py`): Command-line interface
   - Argument parsing
   - User-friendly output formatting

3. **Configuration** (`config.json`): Default parameters and settings

## Logging

The system provides comprehensive logging:
- Model initialization status
- Input text and parameters
- Generated completions
- Performance metrics

Enable verbose logging:
```bash
python -m src.cli "Your text here" --verbose
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
