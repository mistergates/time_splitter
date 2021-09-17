import os
import sys

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", ".."))
from time_splitter.gui import TimerGUI


def main():
    gui = TimerGUI()
    gui.open_gui()


if __name__ == '__main__':
    main()
