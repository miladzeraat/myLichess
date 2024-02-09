from flask import Flask, render_template
import requests

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

@app.route('/')
def player():
    player_info = get_player_info("miladonya")
    return render_template('player.html', player_info=player_info)

if __name__ == '__main__':
    app.run(debug=True)
