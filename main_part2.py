from gui_part2 import *


def main() -> None:
    """
    Main function to initialize and run the GUI for the Final Project.
    """
    window = Tk()
    window.title("Golf Handicap Calculator")
    window.geometry("400x700")
    window.resizable(False, False)
    Gui(window)
    window.mainloop()


if __name__ == '__main__':
    main()