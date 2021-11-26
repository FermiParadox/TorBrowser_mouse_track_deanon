import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, user_id):
        self.user_id = user_id

    def plot_all_x_y(self, x, y):
        plt.plot(x, y, c='gray', linewidth=0.3)
        plt.scatter(x, y, s=4, c='blue')

    def plot_crit_entry_x_y(self, x, y):
        plt.scatter(x, y, s=50, c='green', marker='x', label='Browser exit point')

    def plot_crit_exit_x_y(self, x, y):
        plt.scatter(x, y, s=50, c='red', marker='x', label='Browser entry point')

    def decorate_graphs_and_show(self):
        title = f"Mouse track (UserID: {self.user_id})"
        plt.title(title)
        plt.legend()
        plt.axis([0, None, None, 0])
        plt.show()
