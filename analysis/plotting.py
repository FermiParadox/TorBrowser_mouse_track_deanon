import matplotlib.pyplot as plt
from analysis.user_base import User


class TrackPlotter:
    def __init__(self, user: User, ax: plt.axis):
        self.ax = ax
        self.user = user
        self.user_id = user.id

    def plot_all_x_y(self, x, y):
        self.ax.plot(x, y, c='gray', linewidth=0.3)
        self.ax.scatter(x, y, s=4, c='black', label='Normal point')

    def plot_exit_xy(self, x, y):
        self.ax.scatter(x, y, s=40, c='red', marker='d', label='Exit point')

    def plot_entry_xy(self, x, y):
        self.ax.scatter(x, y, s=40, c='red', marker='x', label='Entry point')

    def decorate_graphs(self):
        title = f"Mouse track (UserID: {self.user_id})"
        self.ax.title(title)
        self.ax.legend()
        self.ax.axis([0, 1500, -1000, 0])

    def plot(self):
        x_all = self.user.all_itxyek.x
        y_all = self.user.all_itxyek.y

        self.plot_all_x_y(x=x_all, y=y_all)

        exit_x_list = self.user.exit_x
        exit_y_list = self.user.exit_y
        self.plot_exit_xy(x=exit_x_list, y=exit_y_list)

        entry_x_list = self.user.entry_x
        entry_y_list = self.user.entry_y
        self.plot_entry_xy(x=entry_x_list, y=entry_y_list)

        # self.decorate_graphs()
