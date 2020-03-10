from tkinter import *
from tkinter import simpledialog
from tkinter import ttk, messagebox
import tkinter.font as font
import datetime as dt
from Waiting_Game_class import WaitingGame

panel_styles = {
    "quick help": {
        'main_background': "#E0F2DA",
        'main_foreground': "#3C713B",
        'sub_background': "#E0F2DA",
        'sub_foreground': "black",
        'request_btn': "Request Quick Help",
        "request_btn_background": "#A9D4A6",
        "request_btn_foreground": "white",
        "request_btn_border": "#73A777",
    },
    "long help": {
        'main_background': "#DAECF8",
        'main_foreground': "#3A617E",
        'sub_background': "#DAECF8",
        'sub_foreground': "black",
        'request_btn': "Request Long Help",
        "request_btn_background": "#A7D8E7",
        "request_btn_foreground": "white",
        "request_btn_border": "#3A617E",
    },
    "both_panel": {
        "green_background": "#AEDCAE",
        "green_border": "#3A617E",
        "red_background": "#E6ABAD",
        "red_border": "#CE5866",
    },
    "Play_btn": {
        "text": "Play While You Wait",
        "background": "#F5999E",
        "foreground": "#F0EBF4"
    }
}

panel_texts = {
    "quick help": {
        'main_title': "Quick Questions",
        'sub_title': "< 2 mins with a tutor",
    },
    "long help": {
        'main_title': "Long Questions",
        'sub_title': "> 2 mins with a tutor",
    },
}

panel_comments = {
    "quick help": {
        'comments': '''
            Some examples of quick questions:
                • Syntax errors
                • Interpreting error output
                • Assignment/MyPyTutor interpretation
                • MyPyTutor submission issues
        '''
    },
    "long help": {
        'comments': '''
            Some examples of long questions:
                • Open ended questions
                • How to start a problem
                • How to improve code
                • Debugging
                • Assignment help
        ''',
    },
}
total_users_in_queue = []

class MainGUI(Tk):
    """Main graphical user interface for queue app"""
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.resizable(0, True)
        self.center(win_w=1200, win_h=1000)
        Header(self)
        PlayBtn(self)
        QuestionPanel(self, panel_name="quick help")
        QuestionPanel(self, panel_name="long help")

    def center(self, win_w=1200, win_h=1000):
        """Centers the app.
        Parameters:
           win_w (int):number of pixels for width.
           win_h (int):number of pixels for height.
        """
        rootsize = (win_w, win_h)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = w / 2 - rootsize[0] / 2
        y = h / 2 - rootsize[1] / 2
        self.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))


class Header():
    """ A class to manage the assignment yellow Queue header."""
    def __init__(self, root):
        header_color = "#FEFBED"
        headerframe = Frame(root, height=85, bg=header_color, relief=SUNKEN)
        headerframe.pack(side=TOP, fill=X)

        important_header_txt = "Important"
        important_header = Label(headerframe, text=important_header_txt, font=('Roboto', 14, "bold"), bg=header_color, fg='#C79B53')
        important_header.pack(side=TOP, anchor=W, padx=20, pady=0)

        important_content_txt = "Individual assessment items must be solely your own work. While students are encouraged to have high-level conversations about the problems they are\ntrying to solve, you must not look at another student’s code or copy from it. The university uses sophisticated anti-collusion measures to automatically\ndetect similarity between assignment submissions."
        important_content = Label(headerframe, text=important_content_txt, font=('Roboto', 11), bg=header_color, fg='black', justify=LEFT)
        important_content.pack(side=TOP, anchor=W, padx=20, pady=10)


class PlayBtn(Button):
    """A button for the game, users can play while waiting in queue."""
    def __init__(self, root):
        self.root = root
        play_btn_frame = Frame(root, bg=panel_styles['Play_btn']['background'], relief=FLAT, width=200)
        play_btn_frame.pack(padx=5, pady=10)

        self.play_btn_lbl = Label(play_btn_frame, text=panel_styles['Play_btn']['text'], bg=panel_styles['Play_btn']['background'],
                          fg=panel_styles['Play_btn']['foreground'], font=('Roboto', 15, "bold"))
        self.play_btn_lbl.pack(padx=20, pady=5)

        self.play_btn_lbl.bind("<Button-1>", self.click_btn)

    def click_btn(self, event):
        """Event handling function for keypress event."""
        app = WaitingGame(None)
        self.root.bind_all('<Key>', app.move_ship)
        app.game_init()
        app.start_game()


class QuestionPanel():
    """Class for panels with question details"""
    def __init__(self, root, panel_name):
        """Construct the panels."""
        panel_frame = Frame(root)
        panel_frame.pack(side=LEFT, anchor=N, fill=X, expand=1, padx=20, pady=20)

        main_bg = panel_styles[panel_name]["main_background"]
        main_fg = panel_styles[panel_name]["main_foreground"]
        sub_bg = panel_styles[panel_name]["sub_background"]
        sub_fg = panel_styles[panel_name]["sub_foreground"]
        ''' Title Part 
        Quick Questions 
        < 2 mins with a tutor
        '''
        self.main_title = panel_texts[panel_name]["main_title"]
        self.sub_title = panel_texts[panel_name]["sub_title"]

        title_frame = Frame(panel_frame, relief=FLAT, height=150, bg=main_bg,
                            highlightbackground=main_fg, highlightthickness=1)
        title_frame.pack(side=TOP, fill=X, expand=1)

        main_title_lbl = Label(title_frame, text=self.main_title, font=('Roboto', 22, "bold"), bg=main_bg,
                               fg=main_fg)
        main_title_lbl.pack(side=TOP, padx=20, pady=10)

        sub_title_lbl = Label(title_frame, text=self.sub_title, font=('', 12), bg=sub_bg,
                              fg=sub_fg)
        sub_title_lbl.pack(side=TOP, padx=20, pady=10)
        ''' Comment Part 
        Some examples of questions:
        • Syntax Errors
        • Open ended questions
        '''
        comment_frame = Frame(panel_frame)
        comment_frame.pack(side=TOP, fill=X, expand=1, padx=20, pady=6)

        comment_txt = panel_comments[panel_name]['comments']
        comment_txt_lines = comment_txt.strip().split("\n")
        for i, comment_txt_line in enumerate(comment_txt_lines):
            comment_txt_line = comment_txt_line.strip()

            Label(comment_frame, text=comment_txt_line, font=('Sans serif', 9)).pack(side=TOP, anchor=W, padx=10, pady=6)

        QueuePanel(panel_frame, panel_name=panel_name)


class QueuePanel():
    "Queueing panel where users are entered into queue."
    def __init__(self, root, panel_name):
        self.panel_name = panel_name
        self.root = root
        self.panel_comment = ""

        queue_frame = Frame(root)
        queue_frame.pack(side=TOP, fill=X, expand=1)
        ''' Request Help Button
        Request Quick Help / Request Long Help
        '''
        request_btn_txt = panel_styles[panel_name]["request_btn"]
        request_btn_bg = panel_styles[panel_name]["request_btn_background"]
        request_btn_fg = panel_styles[panel_name]["request_btn_foreground"]
        request_btn_bd = panel_styles[panel_name]["request_btn_border"]

        request_btn_frame = Frame(queue_frame, relief=FLAT, width=200, height=60, bg=request_btn_bg,
                                  highlightbackground=request_btn_bd, highlightthickness=2)
        request_btn_frame.pack(side=TOP, padx=20, pady=10)

        request_btn_lbl = Label(request_btn_frame, text=request_btn_txt, font=('bold', 12), bg=request_btn_bg,
                                fg=request_btn_fg)
        request_btn_lbl.pack(padx=15, pady=10)

        request_btn_frame.bind("<Button-1>", self.click_btn)
        request_btn_lbl.bind("<Button-1>", self.click_btn)
        ''' Comment
        An average wait time of a few seconds for 1 student.
        An average wait time of about 5 minutes for 2 students.
        '''
        self.comment_lbl = Label(queue_frame, text=self.panel_comment, font=('Sans serif', 11))
        self.comment_lbl.pack(side=TOP, anchor=W, padx=15, pady=15)
        ''' Quest List
        '''
        main_list_frame = Frame(queue_frame, relief=FLAT, height=500, highlightbackground=request_btn_bd,
                                highlightthickness=0)
        main_list_frame.pack(side=TOP, fill=X, expand=1, padx=0, pady=0)

        self.size = 12
        self.sub_size = 10
        self.padx = 0
        self.pady = 5

        heading_frame = Frame(main_list_frame, relief=FLAT, height=500, highlightbackground="#A9A9A9",
                              highlightthickness=1)
        heading_frame.pack(side=TOP, fill=X, expand=1, padx=2, pady=0)

        heading_frame.columnconfigure(0, weight=4)
        heading_frame.columnconfigure(1, weight=6)
        heading_frame.columnconfigure(2, weight=8)
        heading_frame.columnconfigure(3, weight=8)
        heading_frame.columnconfigure(4, weight=1)
        heading_frame.columnconfigure(5, weight=1)

        Label(heading_frame, text="#", font=font.Font(family='Roboto', size=self.size, weight='bold')) \
            .grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky=W)
        Label(heading_frame, text="Name          ", font=font.Font(family='Roboto', size=self.size, weight='bold')) \
            .grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky=W)
        Label(heading_frame, text="       Questions Asked",
              font=font.Font(family='Roboto', size=self.size, weight='bold')) \
            .grid(row=0, column=2, padx=self.padx, pady=self.pady, sticky=W)
        Label(heading_frame, text="Time                                    ",
              font=font.Font(family='Roboto', size=self.size, weight='bold')) \
            .grid(row=0, column=3, padx=self.padx, pady=self.pady, sticky=W)

        Frame(heading_frame, width=20, height=20).grid(row=0, column=4, padx=self.padx, pady=self.pady)
        Frame(heading_frame, width=20, height=20).grid(row=0, column=5, padx=self.padx, pady=self.pady)

        content_frame = Frame(main_list_frame, relief=FLAT, highlightbackground=request_btn_bd,
                              highlightthickness=0)
        content_frame.pack(side=TOP, fill=BOTH, expand=1)

        self.list_canvas = Canvas(content_frame)
        self.list_canvas.config(width=300, height=2000)
        self.list_canvas.config(scrollregion=(0, 0, 300, 2000))
        self.list_canvas.config(highlightthickness=0)
        self.list_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.list_canvas.columnconfigure(0, weight=2)
        self.list_canvas.columnconfigure(1, weight=6)
        self.list_canvas.columnconfigure(2, weight=8)
        self.list_canvas.columnconfigure(3, weight=8)
      
        self.queue_list = QueueList()
        self.update()

    def click_btn(self, event):
        """Popup for user to enter name and warning disallowing duplicates in queue."""
        user_name = simpledialog.askstring(self.panel_name, 'Enter your name: ')
        if user_name:
            if user_name in total_users_in_queue:
                messagebox.showwarning("Warning", "You cannot join multiple queues.")
            else:
                total_users_in_queue.append(user_name)
                self.queue_list.addUserToQueue(user_name=user_name)
        else:
            print("Name is empty")
    
    def update(self):
        """Updating and queueing functionality for queue updates, rules and waiting times."""
        self.queue_list.update()

        for widget in self.list_canvas.winfo_children():
            widget.destroy()

        if self.queue_list.list_in_queue:
            #queue sorting for questions asked in descending order and time waited in ascending order.
            queue_list_sorted = []
            for key, val in self.queue_list.list_in_queue.items():
                user_name = key
                questions = val['questions']
                elapsed = val['elapsed']
                queue_list_sorted.append([user_name, questions, elapsed])

            queue_list_sorted.sort(key=takeThird, reverse=True)
            queue_list_sorted.sort(key=takeSecond)

            i = 0
            total_waiting_time = 0
            for [user_name, questions, elapsed] in queue_list_sorted:
                i += 1
                index = i
                Label(self.list_canvas, text=index, font=font.Font(family='Dosis', size=self.sub_size, weight='normal')) \
                    .grid(row=i, column=0, padx=self.padx, pady=self.pady, sticky=W)
                Label(self.list_canvas, text=user_name,
                      font=font.Font(family='Dosis', size=self.sub_size, weight='normal'), anchor=W, justify=LEFT, width=15) \
                    .grid(row=i, column=1, padx=self.padx, pady=self.pady, sticky=W)
                Label(self.list_canvas, text=questions,
                      font=font.Font(family='Dosis', size=self.sub_size, weight='normal')) \
                    .grid(row=i, column=2, padx=self.padx, pady=self.pady, sticky=W)

                total_waiting_time += elapsed
                elapsed_str = convertElapsedToStr(elapsed)

                Label(self.list_canvas, text=elapsed_str,
                      font=font.Font(family='Dosis', size=self.sub_size, weight='normal')) \
                    .grid(row=i, column=3, padx=self.padx, pady=self.pady, sticky=W)

                ''' Exit Queue Buttons Design
                    Red Buttons / Green
                '''
                red_btn_bg = panel_styles["both_panel"]["red_background"]
                red_btn_bd = panel_styles["both_panel"]["red_border"]

                red_btn = Frame(self.list_canvas, width=20, height=20, bg=red_btn_bg,
                                highlightbackground=red_btn_bd, highlightthickness=1)
                red_btn.grid(row=i, column=4, padx=0, pady=self.pady, sticky=W)

                red_btn.bind("<Button-1>", lambda event, user_name=user_name:
                self.red_exit(user_name))

                green_btn_bg = panel_styles["both_panel"]["green_background"]
                green_btn_bd = panel_styles["both_panel"]["green_border"]

                green_btn = Frame(self.list_canvas, width=20, height=20, bg=green_btn_bg,
                                  highlightbackground=green_btn_bd, highlightthickness=1)
                green_btn.grid(row=i, column=5, padx=self.padx, pady=self.pady, sticky=W)

                green_btn.bind("<Button-1>", lambda event, user_name=user_name:
                self.green_exit(user_name))

            #Calculates average waiting time for sorted users in queue.
            student_num = len(queue_list_sorted)
            total_waiting_time_str = convertElapsedToStr(total_waiting_time / student_num)
            total_waiting_time_str_ago = convertElapsedToStr(total_waiting_time / student_num).replace( ' ago','')
            student_num_str = convertStudentNumToStr(student_num)

            self.panel_comment = "An average wait time of {} for {}.".format(total_waiting_time_str_ago, student_num_str)
        else:
            self.panel_comment = "No students in queue"

        self.comment_lbl.config(text=self.panel_comment)

        self.root.after(500, self.update)
    

    def red_exit(self, user_name):
        """Removes user from queue after clicking red button.
        Parameters:
           user_name (str): user inputted name.
        """
        if user_name in total_users_in_queue:
            total_users_in_queue.remove(user_name)

        self.queue_list.notAsked(user_name=user_name)

    def green_exit(self, user_name):
        """Removes user from queue after clicking green button.
        Parameters:
           user_name (str): user inputted name.
        """
        if user_name in total_users_in_queue:
            total_users_in_queue.remove(user_name)

        self.queue_list.asked(user_name=user_name)


def takeSecond(elem):
    return elem[1]

def takeThird(elem):
    return elem[2]

def convertElapsedToStr(elapsed):
    """Convert time waiting into specified strings for display."""
    mins, secs = divmod(elapsed, 60)
    hours, sub_mins = divmod(mins, 60)

    if elapsed < 60:
        elapsed_str = 'a few seconds ago'
        return elapsed_str
    elif mins < 2:
        elapsed_str = 'a minute ago'
        return elapsed_str
    elif hours < 1:
        elapsed_str = '{} minutes ago'.format(int(mins))
        return elapsed_str
    elif hours < 2:
        elapsed_str = '1 hour ago'
        return elapsed_str
    else:
        elapsed_str = '{} hours ago'.format(int(hours))
        return elapsed_str


def convertStudentNumToStr(student_num):
    """Formats string based on number of students in queue."""
    if student_num == 1:
        return '{} student'.format(student_num)
    elif student_num > 1:
        return '{} students'.format(student_num)


class QueueList():
    """Class for important queue features."""
    def __init__(self):
        self.list_in_queue = {}
        self.list_in_history = {}

    def isUserExistsInQueue(self, user_name):
        """Checks if the new user is already in queue."""
        return user_name in self.list_in_queue

    def addUserToQueue(self, user_name):
        """Adds user to queue after match check"""
        if self.isUserExistsInQueue(user_name):
            print("{} is already waiting in the queue")
        else:
            if user_name not in self.list_in_history:
                timestart = dt.datetime.now()
                self.list_in_queue[user_name] = {
                    'questions': 0,
                    'time_start': timestart,
                    'elapsed': dt.datetime.now() - timestart
                }

            else:
                timestart = dt.datetime.now()
                self.list_in_queue[user_name] = {
                    'questions': self.list_in_history[user_name]['questions'],
                    'time_start': timestart,
                    'elapsed': dt.datetime.now() - timestart
                }

    def asked(self, user_name):
        """Checks if user has asked a question previously"""
        self.list_in_queue.pop(user_name)

        if user_name not in self.list_in_history:
            self.list_in_history[user_name] = {
                'questions': 1
            }
        else:
            self.list_in_history[user_name]['questions'] += 1

    def notAsked(self, user_name):
        """If user has not asked a question previously."""
        self.list_in_queue.pop(user_name)

        if user_name not in self.list_in_history:
            self.list_in_history[user_name] = {
                'questions': 0
            }
        else:
            self.list_in_history[user_name]['questions'] += 0

    def update(self):
        """Updates the time user has waited in queue based on time elapsed."""
        for user_name in self.list_in_queue:
            elapsed = dt.datetime.now() - self.list_in_queue[user_name]['time_start']

            elapsed_secs = elapsed.total_seconds()
            self.list_in_queue[user_name]['elapsed'] = elapsed_secs



if __name__ == '__main__':
    app = MainGUI(None)
    app.title("CSSE1001 Queue")
    app.mainloop()

    
