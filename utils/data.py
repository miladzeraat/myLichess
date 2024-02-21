import requests
import berserk

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

def calculate_outcomes(username, games, Boolean):
    #True===White
    outcomes = {}

    for game in games:
        

        moves = game['moves'].split()
        if len(moves)>2:
            temp=moves[0]+moves[1]
            
            # Get the winner and check if the game involves the specified username
            winner = game.get('winner')
            is_white = game['players']['white']['user']['name'].lower() == username.lower()
            is_black = game['players']['black']['user']['name'].lower() == username.lower()
            if is_white and Boolean:
                if temp not in outcomes:
                    outcomes[temp] = {'win': 0, 'loss': 0, 'draw': 0}
                if winner is None:
                    outcomes[temp]['draw'] += 1
                elif winner == 'white'  :
                    outcomes[temp]['win'] += 1
                else:
                    outcomes[temp]['loss'] += 1
            elif is_black and not Boolean:
                if temp not in outcomes:
                    outcomes[temp] = {'win': 0, 'loss': 0, 'draw': 0}
                if winner is None:
                    outcomes[temp]['draw'] += 1
                elif winner == 'black'  :
                    outcomes[temp]['win'] += 1
                else:
                    outcomes[temp]['loss'] += 1

    # Calculate percentages
    total_games = sum(sum(outcome.values()) for outcome in outcomes.values())
    for outcome in outcomes.values():
        total_outcomes = sum(outcome.values())
        outcome['win_percentage'] = (outcome['win'] / total_outcomes) * 100 if total_outcomes > 0 else 0
        outcome['loss_percentage'] = (outcome['loss'] / total_outcomes) * 100 if total_outcomes > 0 else 0
        outcome['draw_percentage'] = (outcome['draw'] / total_outcomes) * 100 if total_outcomes > 0 else 0

    return outcomes

def get_win_percentages(username,games):

    total_games = len(games)
    
    wins_white = 0
    draw_with_white = 0
    games_with_white = 0
    wins_black = 0
    draw_with_black = 0
    games_with_black = 0
    
    for game in games:
        winner = game.get('winner')
        draw_status = game.get('status')
        if winner is None:
            if game['players']['white']['user']['name'].lower() == username.lower():
                draw_with_white += 1
                games_with_white += 1
            else:
                draw_with_black += 1
                games_with_black += 1
        else:
            if game['players']['white']['user']['name'].lower() == username.lower():
                if winner == 'white':
                    wins_white += 1
                games_with_white += 1
            elif game['players']['black']['user']['name'].lower() == username.lower():
                if winner == 'black':
                    wins_black += 1
                games_with_black += 1

    win_percentage_white = (wins_white / games_with_white) * 100 if games_with_white > 0 else 0
    draw_percentage_white = (draw_with_white / games_with_white) * 100 if games_with_white > 0 else 0
    loss_percentage_white = 100 - win_percentage_white - draw_percentage_white
    
    win_percentage_black = (wins_black / games_with_black) * 100 if games_with_black > 0 else 0
    draw_percentage_black = (draw_with_black / games_with_black) * 100 if games_with_black > 0 else 0
    loss_percentage_black = 100 - win_percentage_black - draw_percentage_black
    
    return (
        win_percentage_white, 
        draw_percentage_white, 
        loss_percentage_white, 
        win_percentage_black, 
        draw_percentage_black, 
        loss_percentage_black
    )
