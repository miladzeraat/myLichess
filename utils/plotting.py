import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np
import datetime

def generate_pie_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                        win_percentage_black, draw_percentage_black, loss_percentage_black,flavor=''):
    labels = ['Win', 'Draw', 'Loss']
    white_data = [win_percentage_white, draw_percentage_white, loss_percentage_white]
    black_data = [win_percentage_black, draw_percentage_black, loss_percentage_black]

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].pie(white_data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax[0].set_title('White')
    ax[1].pie(black_data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax[1].set_title('Black')

    # Save the plot to a file
    plot_filename = f'static/images/{username}_pie_charts{flavor}.png'
    plt.savefig(plot_filename)
    
    return plot_filename

def generate_bar_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                       win_percentage_black, draw_percentage_black, loss_percentage_black):
    GameResultWhite = {'Win': win_percentage_white, 'Draw': draw_percentage_white, 'Loss': loss_percentage_white}
    GameResultBlack = {'Win': win_percentage_black, 'Draw': draw_percentage_black, 'Loss': loss_percentage_black}

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].barh(list(GameResultWhite.keys()), list(GameResultWhite.values()), color=['green', 'yellow', 'red'], orientation='horizontal')
    ax[0].set_xlabel('Percentage')
    ax[0].set_ylabel('Result')
    ax[0].set_title('White Game Results')
    for i, (key, value) in enumerate(GameResultWhite.items()):
        ax[0].text(value, i, f'{value:.2f}%', ha='left', va='center')

    ax[1].barh(list(GameResultBlack.keys()), list(GameResultBlack.values()), color=['green', 'yellow', 'red'])
    ax[1].set_xlabel('Percentage')
    ax[1].set_ylabel('Result')
    ax[1].set_title('Black Game Results')
    for i, (key, value) in enumerate(GameResultBlack.items()):
        ax[1].text(value, i, f'{value:.2f}%', ha='left', va='center')

    # Save the plot to a file
    plot_filename = f'static/images/{username}_bar_chart.png'
    plt.savefig(plot_filename)
    
    return plot_filename



def generate_first_move_bar_chart(outcome,color):
    moves = list(outcome.keys())
    sorted_outcomes = sorted(outcome.items(), key=lambda x: x[1]['win'], reverse=True)[:10]


    moves = [move for move, _ in sorted_outcomes]
    win_counts = [outcome['win'] for _, outcome in sorted_outcomes]
    loss_counts = [outcome['loss'] for _, outcome in sorted_outcomes]
    draw_counts = [outcome['draw'] for _, outcome in sorted_outcomes]   

    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust figsize for wider plot
    bar_width = 0.25
    index = np.arange(len(moves))
    ax.bar(index, win_counts, bar_width, label='Win', color='green')
    ax.bar(index + bar_width, loss_counts, bar_width, label='Loss', color='red')
    ax.bar(index + 2 * bar_width, draw_counts, bar_width, label='Draw', color='yellow')
    
    ax.set_xlabel('First Move')
    ax.set_ylabel('Count')
    ax.set_title('Outcome of First Move')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(moves, rotation=45, ha='right')  # Rotate x-axis labels for better readability
    ax.legend()

    # Save the plot to a file
    plot_filename = f'static/images/first_move_{color}_bar_chart.png'
    plt.savefig(plot_filename)
    
    return plot_filename


import matplotlib.dates as mdates

def plot_ratings_over_time(ratings_data_bullet, ratings_data_blitz, ratings_data_rapid):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

    categories = ['Bullet', 'Blitz', 'Rapid']
    all_data = [ratings_data_bullet, ratings_data_blitz, ratings_data_rapid]

    for i, (ratings_data, category) in enumerate(zip(all_data, categories)):
        if ratings_data and len(ratings_data) >= 10:
            # Extract timestamps and ratings from the ratings data
            timestamps, ratings = zip(*ratings_data)
            
            # Convert timestamps to datetime objects if not already
            if isinstance(timestamps[0], int):
                timestamps = [datetime.datetime.utcfromtimestamp(ts) for ts in timestamps]

            # Plot ratings over time
            axes[i].plot(timestamps, ratings, linestyle='-')
            axes[i].set_title(f"Player's Ratings Over Time ({category})")
            axes[i].set_xlabel("Year")
            axes[i].set_ylabel("Rating")
            axes[i].grid(True)

            # Format x-axis as years
            axes[i].xaxis.set_major_locator(mdates.YearLocator())
            axes[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Adjust layout
    plt.tight_layout()
    
    # Save the plot to a file
    plot_filename = 'static/images/ratings_over_time_combined.png'
    plt.savefig(plot_filename)

    return plot_filename
def plot_rating_diffs(white_diffs, black_diffs, total_diffs):
    plt.figure(figsize=(10, 6))
    
    # Plot cumulative rating differences for white
    plt.plot(range(len(white_diffs)), white_diffs, color='blue', label='White')
    
    # Plot cumulative rating differences for black
    plt.plot(range(len(black_diffs)), black_diffs, color='red', label='Black')
    
    # Plot cumulative rating differences for total (white + black)
    plt.plot(range(len(total_diffs)), total_diffs, color='green', label='Total')
    
    plt.title("Cumulative Rating Differences Over Games")
    plt.xlabel("Games")
    plt.ylabel("Cumulative Rating Difference")
    plt.legend()
    plt.grid(True)
    

    # Save the plot to a file
    plot_filename = 'static/images/rating_diffs_over_games.png'
    plt.savefig(plot_filename)

    return plot_filename