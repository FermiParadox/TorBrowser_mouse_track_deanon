from matplotlib.pyplot import scatter, plot, show


def plot_x_y(x, y):
    plot(x, y, c='blue', linewidth=0.4)
    scatter(x, y, s=5, c='r')
    show()
