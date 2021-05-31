import tkinter
import functools


class Stare:
    def __init__(self, piese_albe_nefolosite=9, piese_albe_pe_tabla=0, piese_negre_nefolosite=9, piese_negre_pe_tabla=0, jucator_curent="alb", tata=None, matrix=None):
        """
        Starea este retinuta sub forma unei matrici 8x3, cate o linie pt fiecare rand (linia din mijloc cu 6 intrari se considera doua linii separate, una pt stanga si una pt dreapta)
        :param piese_albe_nefolosite: nr de piese ce mai trb puse pe tabla (etapa1). Initial fiecare jucator are 9 piese
        :param piese_albe_pe_tabla: cate piese se gasesc pe tabla (fara cele din mana si fara cele scoase din joc)
        :param piese_negre_nefolosite: idem
        :param piese_negre_pe_tabla: idem
        :param jucator_curent: ce jucator urmeaza sa mute. Intotdeauna incepe jucatorul alb
        :param tata: starea din care s-a generat aceasta mutare
        :param matrix: matricea actuala a tablei de bord
        """
        self.tata = tata
        self.matrix = matrix if matrix is not None else [[0] * 3 for _ in range(8)]
        self.piese_albe_nefolosite = piese_albe_nefolosite
        self.piese_albe_pe_tabla = piese_albe_pe_tabla
        self.piese_negre_nefolosite = piese_negre_nefolosite
        self.piese_negre_pe_tabla = piese_negre_pe_tabla
        self.jucator_curent = jucator_curent


class MorrisBoard(tkinter.Tk):
    buttons = []

    def __init__(self):
        super().__init__()
        self.geometry("440x552")
        self.title("Octavian-Florin Staicu - Tintar")
        self.board_frame = tkinter.Frame(self, width=440, height=512)
        bg = tkinter.PhotoImage(file="board13.png")
        label = tkinter.Label(self.board_frame, image=bg)
        label.place(x=0, y=0)
        self.add_buttons(5)
        self.stare_initiala = Stare()

        # self.board_frame.grid_propagate(True)

        self.board_frame.grid(row=1, column=1)  # put frame where the button should be

        self.mainloop()

    def add_buttons(self, dim):
        # Linia 1 (cea mai sus)
        button1 = tkinter.Button(self.board_frame, height=dim, width=dim, )  # command=functools.partial(f, 3))
        button1.grid(row=1, column=1)
        MorrisBoard.buttons.append((button1, (1, 1)))

        button2 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button2.grid(row=1, column=4)
        MorrisBoard.buttons.append((button2, (1, 4)))

        button3 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button3.grid(row=1, column=7)
        MorrisBoard.buttons.append((button3, (1, 7)))

        # linia 2 (mijloc sus)
        button4 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button4.grid(row=2, column=2)
        MorrisBoard.buttons.append((button4, (2, 2)))

        button5 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button5.grid(row=2, column=4)
        MorrisBoard.buttons.append((button5, (2, 4)))

        button6 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button6.grid(row=2, column=6)
        MorrisBoard.buttons.append((button6, (2, 6)))

        # linia 3(inf sus)
        button7 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button7.grid(row=3, column=3)
        MorrisBoard.buttons.append((button7, (3, 3)))

        button8 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button8.grid(row=3, column=4)
        MorrisBoard.buttons.append((button8, (3, 4)))

        button9 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button9.grid(row=3, column=5)
        MorrisBoard.buttons.append((button9, (3, 5)))

        # linia 4 (Mijloc stanga)
        button10 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button10.grid(row=4, column=1)
        MorrisBoard.buttons.append((button10, (4, 1)))

        button11 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button11.grid(row=4, column=2)
        MorrisBoard.buttons.append((button11, (4, 2)))

        button12 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button12.grid(row=4, column=3)
        MorrisBoard.buttons.append((button12, (4, 3)))

        # linia 5 (Mijloc dreapta)
        button13 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button13.grid(row=4, column=5)
        MorrisBoard.buttons.append((button13, (4, 5)))

        button14 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button14.grid(row=4, column=6)
        MorrisBoard.buttons.append((button14, (4, 6)))

        button15 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button15.grid(row=4, column=7)
        MorrisBoard.buttons.append((button15, (4, 7)))

        # linia 6 (sup jos)
        button16 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button16.grid(row=5, column=3)
        MorrisBoard.buttons.append((button16, (5, 3)))

        button17 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button17.grid(row=5, column=4)
        MorrisBoard.buttons.append((button17, (5, 4)))

        button18 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button18.grid(row=5, column=5)
        MorrisBoard.buttons.append((button18, (5, 5)))

        # linia 7 (mij jos)
        button19 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button19.grid(row=6, column=2)
        MorrisBoard.buttons.append((button19, (6, 2)))

        button20 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button20.grid(row=6, column=4)
        MorrisBoard.buttons.append((button20, (6, 4)))

        button21 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button21.grid(row=6, column=6)
        MorrisBoard.buttons.append((button21, (6, 6)))

        # linia 8 (inf jos)
        button22 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button22.grid(row=7, column=1)
        MorrisBoard.buttons.append((button22, (7, 1)))

        button23 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button23.grid(row=7, column=4)
        MorrisBoard.buttons.append((button23, (7, 4)))

        button24 = tkinter.Button(self.board_frame, height=dim, width=dim)
        button24.grid(row=7, column=7)
        MorrisBoard.buttons.append((button24, (7, 7)))


if __name__ == "__main__":
    a = MorrisBoard()
