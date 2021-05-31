import tkinter


class MorrisBoard(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("440x552")
        self.title("Octavian-Florin Staicu - Tintar")
        self.board_frame = tkinter.Frame(self, width=440, height=512)
        bg = tkinter.PhotoImage(file="board13.png")
        label = tkinter.Label(self.board_frame, image=bg)
        label.place(x=0, y=0)
        self.add_buttons(5)

        # self.board_frame.grid_propagate(True)

        self.board_frame.grid(row=1, column=1)  # put frame where the button should be
        self.board_frame.update_idletasks()
        # self.mainloop()

    def add_buttons(self, dim):
        button1 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button1.grid(row=1, column=1)
        button2 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button2.grid(row=1, column=4)
        button3 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button3.grid(row=1, column=7)

        button4 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button4.grid(row=2, column=2)
        button5 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button5.grid(row=2, column=4)
        button6 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button6.grid(row=2, column=6)

        button7 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button7.grid(row=3, column=3)
        button8 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button8.grid(row=3, column=4)
        button9 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button9.grid(row=3, column=5)

        button10 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button10.grid(row=4, column=1)
        button11 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button11.grid(row=4, column=2)
        button12 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button12.grid(row=4, column=3)

        button13 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button13.grid(row=4, column=5)
        button14 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button14.grid(row=4, column=6)
        button15 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button15.grid(row=4, column=7)

        button16 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button16.grid(row=5, column=3)
        button17 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button17.grid(row=5, column=4)
        button18 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button18.grid(row=5, column=5)

        button19 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button19.grid(row=6, column=2)
        button20 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button20.grid(row=6, column=4)
        button21 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button21.grid(row=6, column=6)

        button22 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button22.grid(row=7, column=1)
        button23 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button23.grid(row=7, column=4)
        button24 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button24.grid(row=7, column=7)


if __name__ == "__main__":
    a = MorrisBoard()
    a.mainloop()