from flask import Flask, render_template, request
import requests
import time
app = Flask(__name__)

API_TOKEN = 'lip_yBjKhwsBvqUCJEu2Khcr'

def get_player_info(username):
    
    url = f'https://lichess.org/api/user/{username}'
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    
    try:
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes (e.g., 404, 500)
        player_info = response.json()
        return player_info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player info: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def player():
    
    if request.method == 'POST':
        username = request.form['username']
        
        player_info = get_player_info(username)
        if player_info:
            return render_template('player.html', player_info=player_info)
        else:
            return render_template('index.html', error="Failed to retrieve player information.")
    else:
        # Handle GET request
        
        return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8090,debug=True)
