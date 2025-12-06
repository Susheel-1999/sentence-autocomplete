from flask import Flask, render_template_string, jsonify, request
from sentence_complete import build_default_completer

app = Flask(__name__)
completer = build_default_completer()

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentence Autocomplete</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px;
            width: 100%;
            max-width: 800px;
        }

        h1 {
            text-align: center;
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 50px;
            font-weight: 600;
        }

        .input-container {
            position: relative;
            margin-bottom: 20px;
        }

        #suggestion-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            padding: 18px;
            font-size: 18px;
            line-height: 1.6;
            color: transparent;
            pointer-events: none;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow: hidden;
            border: 2px solid transparent;
            border-radius: 12px;
            font-family: inherit;
        }

        .suggestion-text {
            color: #bbb;
        }

        #user-text {
            width: 100%;
            min-height: 150px;
            padding: 18px;
            font-size: 18px;
            line-height: 1.6;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            resize: vertical;
            font-family: inherit;
            background: transparent;
            position: relative;
            transition: border-color 0.3s;
        }

        #user-text:focus {
            outline: none;
            border-color: #667eea;
        }

        .instructions {
            text-align: center;
            color: #666;
            font-size: 15px;
            margin-top: 15px;
        }

        .instructions strong {
            color: #667eea;
            font-weight: 600;
        }

        .loading {
            text-align: center;
            color: #667eea;
            font-size: 14px;
            margin-top: 10px;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .loading.show {
            opacity: 1;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sentence Autocomplete</h1>
        
        <div class="input-container">
            <div id="suggestion-layer"></div>
            <textarea id="user-text" placeholder="Start typing your sentence..." autocomplete="off" spellcheck="false"></textarea>
        </div>

        <div class="instructions">
            Press <strong>Space</strong> to get AI suggestions • Press <strong>Tab</strong> to accept
        </div>

        <div class="loading" id="loading">Generating suggestion...</div>

        <div class="footer">
            Powered by GPT-2
        </div>
    </div>

    <script>
        const userText = document.getElementById('user-text');
        const suggestionLayer = document.getElementById('suggestion-layer');
        const loadingIndicator = document.getElementById('loading');
        
        let currentSuggestion = '';
        let isGenerating = false;
        let lastText = '';

        userText.addEventListener('keydown', async function(e) {
            // Accept suggestion with Tab
            if (e.key === 'Tab' && currentSuggestion) {
                e.preventDefault();
                userText.value = currentSuggestion;
                clearSuggestion();
                lastText = currentSuggestion;
            }
            
            // Generate suggestion on Space
            else if (e.key === ' ' && userText.value.trim().length > 3 && !isGenerating) {
                const currentText = userText.value.trim();
                
                // Only generate if text has changed significantly
                if (currentText !== lastText && currentText.length > 0) {
                    setTimeout(() => generateSuggestion(currentText), 150);
                }
            }
        });

        userText.addEventListener('input', function() {
            // Clear suggestion if user types something different
            if (currentSuggestion) {
                const currentValue = userText.value;
                if (!currentSuggestion.startsWith(currentValue)) {
                    clearSuggestion();
                }
            }
        });

        async function generateSuggestion(text) {
            if (isGenerating) return;
            
            isGenerating = true;
            loadingIndicator.classList.add('show');
            
            try {
                const response = await fetch('/complete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: text,
                        max_new_tokens: 20,
                        top_k: 50,
                        top_p: 0.95,
                        temperature: 0.7,
                        num_return_sequences: 1
                    })
                });

                const data = await response.json();
                
                if (data.completions && data.completions.length > 0) {
                    currentSuggestion = data.completions[0];
                    displaySuggestion();
                    lastText = text;
                }
            } catch (error) {
                console.error('Error generating suggestion:', error);
            } finally {
                isGenerating = false;
                loadingIndicator.classList.remove('show');
            }
        }

        function displaySuggestion() {
            if (!currentSuggestion) return;
            
            const userValue = userText.value;
            const suggestionRemainder = currentSuggestion.substring(userValue.length);
            
            if (suggestionRemainder) {
                const userPart = document.createElement('span');
                userPart.style.color = 'transparent';
                userPart.textContent = userValue;
                
                const suggestionPart = document.createElement('span');
                suggestionPart.className = 'suggestion-text';
                suggestionPart.textContent = suggestionRemainder;
                
                suggestionLayer.innerHTML = '';
                suggestionLayer.appendChild(userPart);
                suggestionLayer.appendChild(suggestionPart);
            }
        }

        function clearSuggestion() {
            currentSuggestion = '';
            suggestionLayer.innerHTML = '';
        }

        // Auto-focus on load
        userText.focus();
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/complete', methods=['POST'])
def complete():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        completions = completer.complete(
            prompt,
            max_new_tokens=int(data.get('max_new_tokens', 20)),
            top_k=int(data.get('top_k', 50)),
            top_p=float(data.get('top_p', 0.95)),
            temperature=float(data.get('temperature', 0.7)),
            num_return_sequences=int(data.get('num_return_sequences', 1)),
        )
        return jsonify({'completions': completions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
