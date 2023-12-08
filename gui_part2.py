from tkinter import *
import csv
import os


class Gui:
    """
    Class representing the GUI application.
    """
    def __init__(self, window) -> None:
        """
        Method to initialize the GUI for a golf handicap calculator.
        :param window: The main window of the GUI.
        """
        self.window = window

        self.entry_name = Entry(width=40)
        self.entry_date = Entry(width=40)
        self.entry_scores = Entry(width=40)
        self.entry_course = Entry(width=40)
        self.entry_course_ratings = Entry(width=40)
        self.entry_slope_ratings = Entry(width=40)

        self.label_name = Label(text='Enter your name:').pack()
        self.entry_name.pack()

        self.label_date = Label(text='Enter the date:').pack()
        self.entry_date.pack()

        self.label_course = Label(text='Enter the course:').pack()
        self.entry_course.pack()

        self.label_score = Label(text='Enter your score:').pack()
        self.entry_scores.pack()

        self.label_course_ratings = Label(text='Enter course rating:').pack()
        self.entry_course_ratings.pack()

        self.label_slope_ratings = Label(text='Enter slope rating:').pack()
        self.entry_slope_ratings.pack()

        self.frame_buttons = Frame(self.window)
        self.button_add_entry = Button(self.frame_buttons, width=8, text='Add Entry', command=self.add)
        self.button_calculate = Button(self.frame_buttons, width=12, text='Calculate Handicap',
                                       command=self.calculate_handicap)
        self.button_clear = Button(self.frame_buttons, width=8, text='Clear', command=self.clear)
        self.button_add_entry.pack(side='left')
        self.button_calculate.pack(side='left')
        self.button_clear.pack(side='left')
        self.frame_buttons.pack(pady=5)

        self.frame_radio = Frame(self.window)
        self.radio_1 = IntVar()
        self.radio_1.set(0)
        self.radio_recent = Radiobutton(self.frame_radio, text='Recent Rounds', variable=self.radio_1, value=1,
                                        command=self.output)
        self.radio_best = Radiobutton(self.frame_radio, text='Best Rounds', variable=self.radio_1, value=2,
                                      command=self.output)
        self.radio_recent.pack(side="left")
        self.radio_best.pack(side="left")
        self.frame_radio.pack()

        self.frame_output_handicap = Frame(self.window)
        self.label_output_handicap = Label(self.frame_output_handicap)
        self.label_output_handicap.pack(pady=10)
        self.frame_output_handicap.pack()

        self.frame_output_rounds = Frame(self.window)
        self.text_output_rounds = Text(self.frame_output_rounds, height=20, width=50, bd=0)
        self.text_output_rounds.config(state=DISABLED)
        self.text_output_rounds.pack(pady=10)
        self.frame_output_rounds.pack()

    def add(self) -> None:
        """
        Method that adds the user's entries to a CSV file in their name.
        """
        try:
            name = str(self.entry_name.get().strip())
            date = str(self.entry_date.get())
            score = int(self.entry_scores.get())
            course = str(self.entry_course.get())
            rating = float(self.entry_course_ratings.get())
            slope = float(self.entry_slope_ratings.get())

            with open(name, 'a', newline='') as output_csv:
                csv_writer = csv.writer(output_csv)
                header = ["Date", "Course", "Score", "Course Rating", "Slope Rating"]
                if os.stat(name).st_size == 0:
                    csv_writer.writerow(header)

                if name and date and course and score and rating and slope:
                    csv_writer.writerow([date, course, score, rating, slope])
                    self.clear()
                    self.text_output_rounds.config(state=NORMAL)
                    self.text_output_rounds.insert(1.0, 'Added Entry')
                    self.text_output_rounds.config(state=DISABLED)

                else:
                    raise Exception

        except Exception:
            self.text_output_rounds.config(state=NORMAL)
            self.text_output_rounds.delete(1.0, END)
            self.text_output_rounds.insert(1.0, 'Make sure all boxes are filled out.\nScore, Course Rating, and Slope Rating entries \nmust be numbers.')
            self.text_output_rounds.config(state=DISABLED)

    def calculate_handicap(self) -> None:
        """
        Method that calculates the handicap from the user's CSV file.
        """
        name = str(self.entry_name.get().strip())
        self.text_output_rounds.config(state=NORMAL)
        try:
            with open(name, 'r', newline='') as output_csv:
                csv_reader = csv.reader(output_csv)
                next(csv_reader)
                differentials = []

                for row in csv_reader:
                    score, course_rating, slope_rating = map(float, row[2:5])
                    differential = ((score - course_rating) * 113) / slope_rating #handicap formula
                    differentials.append(differential)

                average_differential = sum(differentials) / len(differentials)
                handicap = round(average_differential * 0.96, 1)

                self.label_output_handicap.config(text=f'Handicap: {handicap}')

        except FileNotFoundError:
            self.text_output_rounds.delete(1.0, END)
            self.text_output_rounds.insert(END, 'File not found. Enter Name.')
            self.text_output_rounds.config(state=DISABLED)

    def clear(self) -> None:
        """
        Method that clears all the entries, radio buttons, handicap label, and text box.
        """
        self.entry_name.delete(0, END)
        self.entry_date.delete(0, END)
        self.entry_scores.delete(0, END)
        self.entry_course.delete(0, END)
        self.entry_course_ratings.delete(0, END)
        self.entry_slope_ratings.delete(0, END)
        self.radio_1.set(0)
        self.label_output_handicap.config(text='')
        self.text_output_rounds.config(state=NORMAL)
        self.text_output_rounds.delete(1.0, END)
        self.text_output_rounds.config(state=DISABLED)

    def output(self) -> None:
        """
        Method that outputs the best or most recent rounds based on the input from the user.
        """
        radio_input = self.radio_1.get()

        if radio_input == 1:
            self.text_output_rounds.config(state=NORMAL)
            self.text_output_rounds.delete(1.0, END)

            try:
                with open(self.entry_name.get().strip(), 'r', newline='') as output_csv:
                    csv_reader = csv.reader(output_csv)
                    header = next(csv_reader)
                    self.text_output_rounds.insert(END,
                                                   'Date, Course, Score, Course Rating, Slope Rating\n')
                    for row in csv_reader:
                        line = ', '.join(row) + '\n'
                        self.text_output_rounds.insert(END, line)

                self.text_output_rounds.config(state=DISABLED)
            except FileNotFoundError:
                self.text_output_rounds.delete(1.0, END)
                self.text_output_rounds.insert(END, 'File not found. Enter Name.')
                self.text_output_rounds.config(state=DISABLED)

        elif radio_input == 2:
            self.text_output_rounds.config(state=NORMAL)
            self.text_output_rounds.delete(1.0, END)

            try:
                with open(self.entry_name.get().strip(), 'r', newline='') as output_csv:
                    csv_reader = csv.reader(output_csv)
                    header = next(csv_reader)
                    self.text_output_rounds.insert(END, 'Date, Course, Score, Course Rating, Slope Rating\n')

                    data = [row for row in csv_reader]

                    sorted_data = sorted(data, key=lambda x: int(x[header.index('Score')]))

                    for row in sorted_data:
                        line = ', '.join(row) + '\n'
                        self.text_output_rounds.insert(END, line)

                self.text_output_rounds.config(state=DISABLED)
            except FileNotFoundError:
                self.text_output_rounds.delete(1.0, END)
                self.text_output_rounds.insert(END, 'File not found. Enter Name.')
                self.text_output_rounds.config(state=DISABLED)
