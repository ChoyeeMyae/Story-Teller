from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# Simple form template
TEMPLATE = '''
<html>
    <body>
        <form action="/" method="post">
            Genre: <input type="text" name="genre"><br>
            Reader Age: <input type="number" name="reader_age"><br>
            Character Name: <input type="text" name="character_name"><br>
            Character Sex: <select name="character_sex">
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
            </select><br>
            <input type="submit" value="Generate Story">
        </form>
        {% if story %}
            <h2>Generated Story:</h2>
            <p>{{ story }}</p>
        {% endif %}
    </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    story = None
    if request.method == 'POST':
        genre = request.form['genre']
        reader_age = request.form['reader_age']
        character_name = request.form['character_name']
        character_sex = request.form['character_sex']

        prompt = f"Create a short story in the {genre} genre for a reader aged {reader_age}. "
        prompt += f"The story should feature a main character named {character_name} ({character_sex}).\n\nStory:"

        story = generate_story(prompt)
    
    return render_template_string(TEMPLATE, story=story)

def generate_story(prompt):
    api_key = os.getenv('')  # Make sure to set this environment variable
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 300
    }
    response = requests.post('https://api.openai.com/v1/completions', json=data, headers=headers)
    result = response.json()
    return result['choices'][0]['text'] if response.status_code == 200 else "Failed to generate story."

if __name__ == '__main__':
    app.run(debug=True)

