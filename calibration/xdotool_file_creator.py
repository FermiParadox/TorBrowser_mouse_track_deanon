"""
WARNING: xdotool doesn't provide points as expected.
    It seems to delay its exit from the browser,
    displayed as 2 denser points before exit.

    Check if there's an optional flag that fixes it.
"""

from calibration.angle_conversion import _xdotool_angle

START_SLEEP = 3
START_SLEEP_STR = f"sleep {START_SLEEP}\n"

REPETITIONS = 2000  # large enough to cover screen


def store_straight_steady_speed(pixels_per_sec, angle: int = 90):
    xdotool_angle = _xdotool_angle(angle)

    move_delay = 1 / pixels_per_sec
    move_delay_ms = move_delay * 1000
    file_name = f"xdotool_move_files/angle{angle}_1px_per_{str(move_delay_ms).replace('.','')}ms"

    with open(file_name, "+w") as file:
        file.writelines(START_SLEEP_STR)
        for _ in range(REPETITIONS):
            file.writelines(f"mousemove_relative --polar {xdotool_angle} 1\n")
            file.writelines(f"sleep {move_delay}\n")


if __name__ == "__main__":
    store_straight_steady_speed(pixels_per_sec=2000)
