import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

def generate_pie_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                        win_percentage_black, draw_percentage_black, loss_percentage_black):
    labels = ['Win', 'Draw', 'Loss']
    white_data = [win_percentage_white, draw_percentage_white, loss_percentage_white]
    black_data = [win_percentage_black, draw_percentage_black, loss_percentage_black]

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].pie(white_data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax[0].set_title('White')
    ax[1].pie(black_data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax[1].set_title('Black')

    # Save the plot to a file
    plot_filename = f'static/images/{username}_pie_charts.png'
    plt.savefig(plot_filename)
    
    return plot_filename

def generate_bar_chart(username, win_percentage_white, draw_percentage_white, loss_percentage_white,
                       win_percentage_black, draw_percentage_black, loss_percentage_black):
    GameResultWhite = {'Win': win_percentage_white, 'Draw': draw_percentage_white, 'Loss': loss_percentage_white}
    GameResultBlack = {'Win': win_percentage_black, 'Draw': draw_percentage_black, 'Loss': loss_percentage_black}

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].barh(list(GameResultWhite.keys()), list(GameResultWhite.values()), color=['green', 'yellow', 'red'])
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
