from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Define your route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    story = None
    error = None

    # Check if the form has been submitted
    if request.method == 'POST':
        try:
            # Extract form data
            genre = request.form['genre']
            reader_age = request.form['reader_age']
            character_name = request.form['character_name']
            character_sex = request.form['character_sex']

            # Construct the prompt for the AI
            prompt = construct_prompt(genre, reader_age, character_name, character_sex)

            # Generate the story
            story = generate_story(prompt)
            if not story:
                error = 'Failed to generate story. Please try again later.'

        except Exception as e:
            # Handle exceptions and provide feedback
            error = str(e)

    # Render the home page with the story and any error messages
    return render_template('home.html', story=story, error=error)

def construct_prompt(genre, reader_age, character_name, character_sex):
    # Create a detailed prompt for the AI
    return (
        f"Create a short story in the {genre} genre for a reader aged {reader_age}. "
        f"The story should be engaging and easy to follow, with a protagonist named {character_name} who is {character_sex}. "
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
