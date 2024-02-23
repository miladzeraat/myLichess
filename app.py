from flask import Flask, render_template, request, redirect, url_for
from utils.data import get_player_info, extract_rating_diffs, get_win_percentages, calculate_outcomes, calculate_rating
from utils.plotting import generate_pie_chart,plot_rating_diffs, generate_bar_chart, generate_first_move_bar_chart,plot_ratings_over_time
import os
import requests
import berserk
import pickle
from openai import OpenAI
client = OpenAI(api_key='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')

API_TOKEN = 'lip_yBjKhwsBvqUCJEu2Khcr'
CACHE_FOLDER = "game_cache"
app = Flask(__name__)
def chat_with_gpt(outcome_white, outcome_black):
    # Construct the message for ChatGPT
    messages = [
        {"role": "system", "content": "I'm providing you with chess dataset for games played with white and black pieces. Please analyze the data and provide insights and recommendations based on the outcomes."},
        {"role": "user", "content": f"For games played with white pieces: {outcome_white}. For games played with black pieces: {outcome_black}."}
    ]

    # Send the messages to ChatGPT
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message.content
def check_cached_data(username):
    cache_filename = os.path.join(CACHE_FOLDER, f"{username}_games.pkl")
    return os.path.exists(cache_filename)

def save_games_to_cache(username, games):
    cache_filename = os.path.join(CACHE_FOLDER, f"{username}_games.pkl")
    with open(cache_filename, "wb") as f:
        pickle.dump(games, f)

def load_games_from_cache(username):
    cache_filename = os.path.join(CACHE_FOLDER, f"{username}_games.pkl")
    with open(cache_filename, "rb") as f:
        return pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player/<username>', methods=['POST', 'GET'])
def player_info(username):
    player_info = get_player_info(username)
    # Fetch games data
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)
    if check_cached_data(username):
        games = load_games_from_cache(username)
    else:
        games = list(client.games.export_by_player(username))
        if username.lower() in ['miladonya','miladagha','drnykterstein','alireza2003','lance5500']:
            save_games_to_cache(username, games)

    if player_info:
        # Get win percentages using the data module
        (win_percentage_white, draw_percentage_white, loss_percentage_white,
         win_percentage_black, draw_percentage_black, loss_percentage_black) = get_win_percentages(username,games)

        # Generate pie charts
        plot_filename = generate_pie_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                                            win_percentage_black, draw_percentage_black, loss_percentage_black,flavor='')

        # Generate bar charts
        bar_plot_filename = generate_bar_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                                                win_percentage_black, draw_percentage_black, loss_percentage_black)
        #First move bar chart
        outcome_white=calculate_outcomes(username, games, True)
        outcome_black=calculate_outcomes(username, games, False)
        bar_chart_first_move_white = generate_first_move_bar_chart(outcome_white,color='white')
        bar_chart_first_move_black = generate_first_move_bar_chart(outcome_black,color='black')
        #Rating per time
        rating_bullet,rating_blitz,rating_rapid=calculate_rating(username,games)
        rating_plot=plot_ratings_over_time(rating_bullet, rating_blitz, rating_rapid)
        #higher/lowe rated players
        lower_rated_opponent_games = []
        higher_rated_opponent_games = []
        rated_games= [game for game in games if game['rated']]
        for game in rated_games:
            
            if (game['players']['white']['user']['name'].lower() == username.lower() and game['players']['white']['rating'] < game['players']['black']['rating']) or (game['players']['black']['user']['name'].lower() == username.lower() and game['players']['black']['rating'] < game['players']['white']['rating']):
                higher_rated_opponent_games.append(game)
            else:
                lower_rated_opponent_games.append(game)
            
        (higher_win_percentage_white, higher_draw_percentage_white, higher_loss_percentage_white,
        higher_win_percentage_black, higher_draw_percentage_black, higher_loss_percentage_black) = get_win_percentages(username, higher_rated_opponent_games)

        (lower_win_percentage_white, lower_draw_percentage_white, lower_loss_percentage_white,
        lower_win_percentage_black, lower_draw_percentage_black, lower_loss_percentage_black) = get_win_percentages(username, lower_rated_opponent_games)
        # Generate pie chart for games against higher-rated opponents
        higher_rating_plot_filename = generate_pie_chart(username, higher_win_percentage_white, higher_draw_percentage_white, higher_loss_percentage_white,
                                                  higher_win_percentage_black, higher_draw_percentage_black, higher_loss_percentage_black, flavor='_higher rated opponent')

        # Generate pie chart for games against lower-rated opponents
        lower_rating_plot_filename = generate_pie_chart(username, lower_win_percentage_white, lower_draw_percentage_white, lower_loss_percentage_white,
                                                 lower_win_percentage_black, lower_draw_percentage_black, lower_loss_percentage_black,flavor='_lower rated opponents')
        #Rating difference
        # Extract rating differences for games against higher-rated opponents
        higher_white_rating_diffs, higher_black_rating_diffs, higher_overall_rating_diffs = extract_rating_diffs(username, higher_rated_opponent_games)
        lower_white_rating_diffs, lower_black_rating_diffs, lower_overall_rating_diffs = extract_rating_diffs(username, lower_rated_opponent_games)
        higher_rating_score = plot_rating_diffs(higher_white_rating_diffs, higher_black_rating_diffs, higher_overall_rating_diffs)
        lower_rating_score=plot_rating_diffs(lower_white_rating_diffs, lower_black_rating_diffs, lower_overall_rating_diffs)
        #chat with chatgpt
        chat_data = f"Player {username}'s statistics: Wins - {win_percentage_white}, Draws - {draw_percentage_white}, Losses - {loss_percentage_white}, etc."
        advice = chat_with_gpt(outcome_white, outcome_black)
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
            bar_chart_first_move_black=bar_chart_first_move_black,rating_plot=rating_plot,higher_rating_plot_filename=higher_rating_plot_filename,lower_rating_plot_filename=lower_rating_plot_filename,higher_rating_score=higher_rating_score,lower_rating_score=lower_rating_score,advice=advice)
    else:
        return render_template('index.html', error="Failed to retrieve player information.")

if __name__ == '__main__':
    app.run(port=8090, debug=True)