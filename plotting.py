from matplotlib.pyplot import scatter, plot, show


def plot_all_x_y(x, y):
    plot(x, y, c='green', linewidth=0.4)
    scatter(x, y, s=5, c='blue')


def plot_crit_entry_x_y(x, y):
    scatter(x, y, s=50, c='orange', marker='x')


def plot_crit_exit_x_y(x, y):
    scatter(x, y, s=50, c='red', marker='x')

