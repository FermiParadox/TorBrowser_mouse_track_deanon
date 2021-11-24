from matplotlib.pyplot import scatter, plot


def plot_all_x_y(x, y):
    plot(x, y, c='gray', linewidth=0.4)
    scatter(x, y, s=5, c='blue')


def plot_crit_entry_x_y(x, y):
    scatter(x, y, s=50, c='green', marker='x')


def plot_crit_exit_x_y(x, y):
    scatter(x, y, s=50, c='red', marker='x')

