import tkinter
import functools
import copy


class Stare:
    decodif_poz_matrice = [(1, 1), (1, 4), (1, 7), (2, 2), (2, 4), (2, 6), (3, 3), (3, 4), (3, 5), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5), (6, 2), (6, 4), (6, 6), (7, 1), (7, 4), (7, 7)]

    def __init__(self, piese_albe_nefolosite=9, piese_albe_pe_tabla=0, piese_negre_nefolosite=9, piese_negre_pe_tabla=0, jucator_curent_alb=True, tata=None, matrix=None, se_scoate_o_piesa=False):
        """
        Starea este retinuta sub forma unei matrici 8x3, cate o linie pt fiecare rand (linia din mijloc cu 6 intrari se considera doua linii separate, una pt stanga si una pt dreapta)
        :param piese_albe_nefolosite: nr de piese ce mai trb puse pe tabla (etapa1). Initial fiecare jucator are 9 piese
        :param piese_albe_pe_tabla: cate piese se gasesc pe tabla (fara cele din mana si fara cele scoase din joc)
        :param piese_negre_nefolosite: idem
        :param piese_negre_pe_tabla: idem
        :param jucator_curent_alb: ce jucator urmeaza sa mute. True daca e alb, False daca e Negru
        :param tata: starea din care s-a generat aceasta mutare
        :param matrix: matricea actuala a tablei de bord
        """
        self.tata = tata
        self.matrix = matrix if matrix is not None else [[None for _ in range(3)] for _ in range(8)]
        self.piese_albe_nefolosite = piese_albe_nefolosite
        self.piese_albe_pe_tabla = piese_albe_pe_tabla
        self.piese_negre_nefolosite = piese_negre_nefolosite
        self.piese_negre_pe_tabla = piese_negre_pe_tabla
        self.jucator_curent_alb = jucator_curent_alb
        self.se_scoate_o_piesa = se_scoate_o_piesa
        self.l_succesori = None

    def __eq__(self, o):
        if self.__class__ == o.__class__:
            return self.matrix == o.matrix and self.jucator_curent_alb == o.jujucator_curent_alb and self.piese_albe_nefolosite == o.piese_albe_nefolosite and \
                   self.piese_albe_pe_tabla == o.piese_albe_pe_tabla and self.piese_negre_nefolosite == o.piese_negre_nefolosite and self.piese_negre_pe_tabla == o.piese_negre_pe_tabla
        else:
            return False

    @classmethod
    def este_in_moara(cls, matrix, poz):
        lin_reala, col_reala = cls.decodif_poz_matrice[poz[0] * 3 + poz[1]]
        okMoaraCol = True
        okMoaraLin = True
        for i in range(len(cls.decodif_poz_matrice)):
            lin_in_matrice = i // 3
            col_in_matrice = i % 3
            if cls.decodif_poz_matrice[i][0] == lin_reala:
                if matrix[lin_in_matrice][col_in_matrice] != matrix[poz[0]][poz[1]]:
                    okMoaraCol = False
            if cls.decodif_poz_matrice[i][1] == col_reala:
                if matrix[lin_in_matrice][col_in_matrice] != matrix[poz[0]][poz[1]]:
                    okMoaraLin = False
        return okMoaraLin or okMoaraCol

    def generare_succesori(self):
        """
        Va parcurge toate elementele din matrix. Daca nu mai sunt piese de adaugat, pentru elementele care au aceeasi culoare cu a jucatorului curent,
        se vor incerca din cele maxim 4 directi posibile de deplasare, care sunt libere si se va genera noul succesor
        :return: intoarce lista mutarilor posibile pentru jucatorul curent
        """
        if self.l_succesori is None:
            self.l_succesori = []
            for i in range(8):
                for j in range(3):
                    if self.se_scoate_o_piesa:
                        if self.matrix[i][j] is not None and not self.jucator_curent_alb == self.matrix[i][j] and not Stare.este_in_moara(self.matrix, (i, j)):
                            new_matrix = copy.deepcopy(self.matrix)
                            new_matrix[i][j] = None
                            negre_ramase = self.piese_negre_pe_tabla
                            albe_ramase = self.piese_albe_pe_tabla
                            if self.jucator_curent_alb:
                                negre_ramase -= 1
                            else:
                                albe_ramase -= 1
                            stare_noua = Stare(tata=self, matrix=new_matrix, piese_albe_nefolosite=self.piese_albe_nefolosite, piese_albe_pe_tabla=albe_ramase,
                                               piese_negre_pe_tabla=negre_ramase, piese_negre_nefolosite=self.piese_negre_nefolosite, se_scoate_o_piesa=False, jucator_curent_alb=not self.jucator_curent_alb)
                            self.l_succesori.append(stare_noua)
                    else:
                        if (self.jucator_curent_alb and self.piese_albe_nefolosite == 0) or (not self.jucator_curent_alb and self.piese_negre_nefolosite == 0):
                            if (self.jucator_curent_alb and self.piese_albe_pe_tabla > 3) or (not self.jucator_curent_alb and self.piese_negre_pe_tabla > 3):
                                for lin, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                                    try:
                                        """
                                        obtinem linia si coloana reala a pozitiei curente. Apoi ne uitam sus, jos, stanga, dreapta, iar pt acele pozitii care exista
                                        obtinem linia si coloana din matrice la care se afla elementul adiacent. Daca este o pozitie libera, generam un nou succesor
                                        """
                                        linie_reala_actuala, coloana_reala_actuala = Stare.decodif_poz_matrice[i * 3 + j]
                                        idx_pozitie_noua = Stare.decodif_poz_matrice.index((linie_reala_actuala + lin, coloana_reala_actuala + col))
                                        lin_pozitie_noua = idx_pozitie_noua // 3
                                        col_pozitie_noua = idx_pozitie_noua % 3
                                        if self.matrix[lin_pozitie_noua][col_pozitie_noua] is None:
                                            new_matrix = copy.deepcopy(self.matrix)
                                            new_matrix[i][j] = None
                                            new_matrix[lin_pozitie_noua][col_pozitie_noua] = self.jucator_curent_alb
                                            eliminare = Stare.este_in_moara(new_matrix, (lin_pozitie_noua, col_pozitie_noua))
                                            if eliminare:
                                                jucator_nou = self.jucator_curent_alb
                                            else:
                                                jucator_nou = not self.jucator_curent_alb
                                            stare_noua = Stare(tata=self, matrix=new_matrix, piese_albe_nefolosite=self.piese_albe_nefolosite, piese_albe_pe_tabla=self.piese_albe_pe_tabla,
                                                               piese_negre_pe_tabla=self.piese_negre_pe_tabla, piese_negre_nefolosite=self.piese_negre_nefolosite, se_scoate_o_piesa=eliminare, jucator_curent_alb=jucator_nou)
                                            self.l_succesori.append(stare_noua)
                                    except Exception:
                                        continue
                            else:
                                """
                                au ramas 3 piese pentru jucatorul curent, deci poate sa sara cum vrea
                                """
                                if self.matrix[i][j] == self.jucator_curent_alb:
                                    for l in range(8):
                                        for c in range(3):
                                            if self.matrix[l][c] is None:
                                                new_matrix = copy.deepcopy(self.matrix)
                                                new_matrix[i][j] = None
                                                new_matrix[l][c] = self.jucator_curent_alb
                                                eliminare = Stare.este_in_moara(new_matrix, (l, c))
                                                if eliminare:
                                                    jucator_nou = self.jucator_curent_alb
                                                else:
                                                    jucator_nou = not self.jucator_curent_alb
                                                stare_noua = Stare(tata=self, matrix=new_matrix, piese_albe_nefolosite=self.piese_albe_nefolosite, piese_albe_pe_tabla=self.piese_albe_pe_tabla,
                                                                   piese_negre_pe_tabla=self.piese_negre_pe_tabla, piese_negre_nefolosite=self.piese_negre_nefolosite, se_scoate_o_piesa=eliminare, jucator_curent_alb=jucator_nou)
                                                self.l_succesori.append(stare_noua)

                        else:
                            """
                            adaugam o noua piesa
                            """
                            if self.matrix[i][j] is None:
                                negre_nefolosite = self.piese_negre_nefolosite
                                negre_ramase = self.piese_negre_pe_tabla
                                albe_nefolosite = self.piese_albe_nefolosite
                                albe_ramase = self.piese_albe_pe_tabla
                                if self.jucator_curent_alb:
                                    albe_ramase += 1
                                    albe_nefolosite -= 1
                                else:
                                    negre_ramase += 1
                                    negre_nefolosite -= 1
                                new_matrix = copy.deepcopy(self.matrix)
                                new_matrix[i][j] = self.jucator_curent_alb
                                eliminare = Stare.este_in_moara(new_matrix, (i, j))
                                if eliminare:
                                    jucator_nou = self.jucator_curent_alb
                                else:
                                    jucator_nou = not self.jucator_curent_alb
                                stare_noua = Stare(tata=self, matrix=new_matrix, piese_albe_nefolosite=albe_nefolosite, piese_albe_pe_tabla=albe_ramase,
                                                   piese_negre_pe_tabla=negre_ramase, piese_negre_nefolosite=negre_nefolosite, se_scoate_o_piesa=eliminare, jucator_curent_alb=jucator_nou)
                                self.l_succesori.append(stare_noua)

        return self.l_succesori


def f(s: Stare):
    l = s.generare_succesori()
    for i in l:
        print(i.matrix)


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
        self.stare_initiala = Stare()

        self.add_buttons(5)

        self.board_frame.grid(row=1, column=1)

        self.mainloop()

    def add_buttons(self, dim):
        for lin, col in Stare.decodif_poz_matrice:
            button = tkinter.Button(self.board_frame, height=dim, width=dim, command=functools.partial(f, self.stare_initiala))
            button.grid(row=lin, column=col)
            MorrisBoard.buttons.append(button)


if __name__ == "__main__":
    a = MorrisBoard()
