from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    story = None
    error = None
    if request.method == 'POST':
        try:
            genre = request.form['genre']
            reader_age = request.form['reader_age']
            num_characters = int(request.form['num_characters'])
            character_names = [request.form[f'character_name_{i}'] for i in range(1, num_characters + 1)]

            prompt = construct_prompt(genre, reader_age, character_names)
            story = generate_story(prompt)
            if not story:
                error = 'Failed to generate story. Please try again later.'

        except Exception as e:
            error = str(e)

    return render_template('home.html', story=story, error=error)

def construct_prompt(genre, reader_age, character_names):
    character_descriptions = ''
    for i, name in enumerate(character_names, start=1):
        character_descriptions += f"The story should include a character named {name}. "
    
    return (
        f"Create a short story in the {genre} genre for a reader aged {reader_age}. "
        f"{character_descriptions}"
        f"Include elements typical of the genre and create a conflict that is resolved by the end of the story. "
        f"Keep the language and content appropriate for the intended reader age. The story should start with an attention-grabbing event and maintain a consistent tone throughout.\n\n"
        f"Story:"
    )

def generate_story(prompt):
    # Retrieve your API key from an environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise EnvironmentError("No API Key found. Please set the OPENAI_API_KEY environment variable.")

    # Set up the headers with your API key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Set up the data payload for the POST request
    data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 300,
        'temperature': 0.7, # Adjust as needed for creativity
        'frequency_penalty': 0.5,
        'presence_penalty': 0.5,
        'stop': ["\n"] # Stop generation at a new line character
    }

    # Make the POST request to the OpenAI API
    response = requests.post('https://api.openai.com/v1/completions', json=data, headers=headers)

    # Check the response and return the story text if successful
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['text'].strip()
    else:
        # Log the error or handle it as you see fit
        return None

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
