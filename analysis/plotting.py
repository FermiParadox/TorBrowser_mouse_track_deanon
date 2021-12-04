import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def plot_all_x_y(x, y):
        plt.plot(x, y, c='gray', linewidth=0.3)
        plt.scatter(x, y, s=4, c='blue')

    @staticmethod
    def plot_exit_xy(x, y):
        plt.scatter(x, y, s=30, c='red', marker='o', label='Browser exit point')

    @staticmethod
    def plot_entry_xy(x, y):
        plt.scatter(x, y, s=30, c='green', marker='x', label='Browser entry point')

    def decorate_graphs_and_show(self):
        title = f"Mouse track (UserID: {self.user_id})"
        plt.title(title)
        plt.legend()
        plt.axis([0, 1500, -1000, 0])
        plt.show()
