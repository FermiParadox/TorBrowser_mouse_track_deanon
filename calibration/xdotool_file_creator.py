START_SLEEP = 3
START_SLEEP_STR = f"sleep {START_SLEEP}\n"

REPETITIONS = 2000  # large enough to cover screen


def store_straight_steady_speed(pixels_per_sec):
    move_delay = 1 / pixels_per_sec
    move_delay_ms = move_delay * 1000
    file_name = f"xdotool_move_files/right_1px_per_{move_delay_ms}ms"

    with open(file_name, "+w") as file:
        file.writelines(START_SLEEP_STR)
        for _ in range(REPETITIONS):
            file.writelines("mousemove_relative 1 0\n")
            file.writelines(f"sleep {move_delay}\n")


store_straight_steady_speed(pixels_per_sec=2000)
