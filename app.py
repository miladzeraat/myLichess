from flask import Flask, render_template, request
from utils.data import get_player_info, get_win_percentages, calculate_outcomes
from utils.plotting import generate_pie_chart, generate_bar_chart, generate_first_move_bar_chart
import os
import requests
import berserk
API_TOKEN = 'lip_yBjKhwsBvqUCJEu2Khcr'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player', methods=['POST'])
def player():
    username = request.form['username']
    player_info = get_player_info(username)
    # Fetch games data
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)
    games = list(client.games.export_by_player(username))
    if player_info:
        # Get win percentages using the data module
        (win_percentage_white, draw_percentage_white, loss_percentage_white,
         win_percentage_black, draw_percentage_black, loss_percentage_black) = get_win_percentages(username,games)

        # Generate pie charts
        plot_filename = generate_pie_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                                            win_percentage_black, draw_percentage_black, loss_percentage_black)

        # Generate bar charts
        bar_plot_filename = generate_bar_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                                                win_percentage_black, draw_percentage_black, loss_percentage_black)
        #First move bar chart
        outcome_white=calculate_outcomes(username, games, True)
        outcome_black=calculate_outcomes(username, games, False)
        
        bar_chart_first_move_white = generate_first_move_bar_chart(outcome_white,color='white')
        bar_chart_first_move_black = generate_first_move_bar_chart(outcome_black,color='black')
        return render_template(
            'player.html',
            player_info=player_info,
            win_percentage_white=win_percentage_white,
            draw_percentage_white=draw_percentage_white,
            loss_percentage_white=loss_percentage_white,
            win_percentage_black=win_percentage_black,
            draw_percentage_black=draw_percentage_black,
            loss_percentage_black=loss_percentage_black,
            plot_filename=plot_filename,
            bar_plot_filename=bar_plot_filename,
            bar_chart_first_move_white=bar_chart_first_move_white,
            bar_chart_first_move_black=bar_chart_first_move_black)
    else:
        return render_template('index.html', error="Failed to retrieve player information.")

if __name__ == '__main__':
    app.run(port=8090, debug=True)