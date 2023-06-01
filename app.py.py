from transformers import pipeline
from flask import Flask, request, jsonify

#  language model pipeline with top_k=5
fill_mask = pipeline('fill-mask', model='xlm-roberta-base', top_k=10)

#  a Flask app
app = Flask(__name__)

# Define a route for generating predicted words
@app.route('/predict', methods=['POST'])
def predict():
    # Get the user's input text from the request
    input_text = request.json['text']

    # Generate predicted words using the language model
    predictions = fill_mask(input_text + '<mask>')

    # Extract the predicted words from the output
    predicted_words = [prediction['token_str'] for prediction in predictions]

    # Return the predicted words as a JSON response
    return jsonify({'predicted_words': predicted_words})




@app.route('/')
def index():
    
    return '''
        <html>
<head>
	<title>Predictive Text Generator</title>
	<style>
		body {
			font-family: 'Roboto', sans-serif;
			background-color: #f2f2f2;
			margin: 0;
			padding: 0;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			height: 100vh;
			color: #333;
		}

		h1 {
			font-size: 36px;
			margin-bottom: 20px;
			text-align: center;
			color: #4CAF50;
		}

		.form-container {
			display: flex;
			flex-direction: column;
			align-items: center;
			background-color: white;
			padding: 30px;
			border-radius: 10px;
			box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
		}

		input[type="text"] {
			width: 100%;
			font-size: 18px;
			padding: 10px;
			margin-bottom: 20px;
			border: none;
			border-bottom: 2px solid #ccc;
			background-color: transparent;
			outline: none;
			transition: border-color 0.2s ease-in-out;
		}

		input[type="text"]:focus {
			border-color: #4CAF50;
		}

		button {
			background-color: #4CAF50;
			color: white;
			font-size: 18px;
			font-weight: bold;
			border: none;
			border-radius: 5px;
			padding: 10px 20px;
			cursor: pointer;
			transition: background-color 0.2s ease-in-out;
		}

		button:hover {
			background-color: #388E3C;
		}

		.spinner {
			display: inline-block;
			width: 20px;
			height: 20px;
			border-radius: 50%;
			border: 2px solid #ccc;
			border-top-color: #333;
			animation: spin 0.6s linear infinite;
			margin-left: 10px;
			vertical-align: middle;
			visibility: hidden;
		}

		@keyframes spin {
			to {
				transform: rotate(360deg);
			}
		}

		.form-output {
			display: flex;
			flex-direction: column;
			align-items: center;
			margin-top: 40px;
			color: #4CAF50;
			font-size: 24px;
			font-weight: bold;
			text-align: center;
			visibility: hidden;
			opacity: 0;
			transform: translateY(-20px);
			transition: visibility 0s, opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
		}

		.form-output.show {
			visibility: visible;
			opacity: 1;
			transform: translateY(0);
		}
	</style>
</head>
<body>
        <h1>Predictive Text Generator</h1>
        <form id="input-form">
            <label for="input-text">Type something here:</label>
            <input id="input-text" type="text" name="input-text" required>
            <button id="generate-button" type="submit">Generate</button>
        </form>
        <div id="predicted-words-container">
            <p id="predicted-words"></p>
            <div id="loading-spinner" class="spinner" style="display: none;"></div>
        </div>
        <script>
            const form = document.getElementById('input-form');
            const inputText = document.getElementById('input-text');
            const predictedWords = document.getElementById('predicted-words');
            const spinner = document.getElementById('loading-spinner');
            
            form.addEventListener('submit', event => {
                event.preventDefault();
                predictedWords.innerHTML = '';
                spinner.style.display = 'inline-block';
                
                fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({text: inputText.value})
                })
                .then(response => response.json())
                .then(data => {
                    const predictedWordsList = data.predicted_words.join(', ');
                    predictedWords.innerHTML = `Predicted words: ${predictedWordsList}.`;
                    spinner.style.display = 'none';
                })
                .catch(error => {
                    console.error('Error generating predicted words:', error);
                    predictedWords.innerHTML = 'Error generating predicted words.';
                    spinner.style.display = 'none';
                });
            });
        </script>
    </body>
</html>

 '''




if __name__ == '__main__':
    app.run()
app = Flask(__name__, debug=False)
