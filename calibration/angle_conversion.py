import numpy as np
import matplotlib.pyplot as plt


def _xdotool_angle(angle):
    """"""
    if 0 <= angle <= 90:
        return -angle + 90
    if 90 < angle <= 360:
        return -angle + 90 + 360

    if angle < 0:
        return _xdotool_angle(angle + 360)

    if angle > 360:
        raise ValueError(f"Max angle: 360deg. Angle provided {angle}")


def plot_and_save_relation():
    vectorized_xdotool_angle = np.vectorize(_xdotool_angle)

    x_values = np.linspace(0, 360, 10 ** 5)
    y_values = vectorized_xdotool_angle(x_values)

    plt.plot(x_values, y_values)
    plt.axis([0, 360, 0, 360])
    plt.xlabel("angle (polar)")
    plt.ylabel("angle (xdotool)")
    plt.title("Polar angle conversion to 'xdotool angle'\n(xdotool's 0 is at 90 deg and goes clockwise)")

    plt.savefig("polar_angle_to_xdotool_angle_relation")
    plt.show()


if __name__ == "__main__":
    plot_and_save_relation()
