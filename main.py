import tkinter
import functools
import copy


class Stare:
    decodif_poz_matrice = [(1, 1), (1, 4), (1, 7), (2, 2), (2, 4), (2, 6), (3, 3), (3, 4), (3, 5), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5), (6, 2), (6, 4), (6, 6), (7, 1), (7, 4), (7, 7)]

    @staticmethod
    def generare_matrice():
        return [[None for _ in range(3)] for _ in range(8)]

    def __init__(self, matrix, piese_albe_nefolosite=9, piese_albe_pe_tabla=0, piese_negre_nefolosite=9, piese_negre_pe_tabla=0, jucator_curent_alb=True, tata=None, se_scoate_o_piesa=False):
        """
        Starea este retinuta sub forma unei matrici 8x3, cate o linie pt fiecare rand (linia din mijloc cu 6 intrari se considera doua linii separate, una pt stanga si una pt dreapta)
        :param piese_albe_nefolosite: nr de piese ce mai trb puse pe tabla (etapa1). Initial fiecare jucator are 9 piese
        :param piese_albe_pe_tabla: cate piese se gasesc pe tabla (fara cele din mana si fara cele scoase din joc)
        :param piese_negre_nefolosite: idem
        :param piese_negre_pe_tabla: idem
        :param jucator_curent_alb: ce jucator urmeaza sa mute. True daca e alb, False daca e Negru
        :param tata: starea din care s-a generat aceasta mutare
        :param matrix: matricea actuala a tablei de bord
        :param se_scoate_o_piesa: True daca la aceasta mutare se elimina o piesa a adversarului, False daca se continua jocul
        """
        self.tata = tata
        self.matrix = matrix
        self.piese_albe_nefolosite = piese_albe_nefolosite
        self.piese_albe_pe_tabla = piese_albe_pe_tabla
        self.piese_negre_nefolosite = piese_negre_nefolosite
        self.piese_negre_pe_tabla = piese_negre_pe_tabla
        self.jucator_curent_alb = jucator_curent_alb
        self.se_scoate_o_piesa = se_scoate_o_piesa
        self.l_succesori = None

    def __eq__(self, o):
        if self.__class__ == o.__class__:
            return self.matrix == o.matrix and self.jucator_curent_alb == o.jucator_curent_alb and self.piese_albe_nefolosite == o.piese_albe_nefolosite and \
                   self.piese_albe_pe_tabla == o.piese_albe_pe_tabla and self.piese_negre_nefolosite == o.piese_negre_nefolosite and self.piese_negre_pe_tabla == o.piese_negre_pe_tabla \
                   and self.se_scoate_o_piesa == o.se_scoate_o_piesa
        else:
            return False

    @classmethod
    def este_in_moara(cls, matrix, poz):
        lin_reala, col_reala = cls.decodif_poz_matrice[poz[0] * 3 + poz[1]]
        ok_moara_col = True
        ok_moara_lin = True
        for i in range(len(cls.decodif_poz_matrice)):
            lin_in_matrice = i // 3
            col_in_matrice = i % 3
            if cls.decodif_poz_matrice[i][0] == lin_reala:
                if matrix[lin_in_matrice][col_in_matrice] != matrix[poz[0]][poz[1]] and not (col_reala < 4 < cls.decodif_poz_matrice[i][1] or col_reala > 4 > cls.decodif_poz_matrice[i][1]):
                    ok_moara_col = False
            if cls.decodif_poz_matrice[i][1] == col_reala and not (lin_reala < 4 < cls.decodif_poz_matrice[i][0] or lin_reala > 4 > cls.decodif_poz_matrice[i][0]):
                if matrix[lin_in_matrice][col_in_matrice] != matrix[poz[0]][poz[1]]:
                    ok_moara_lin = False
        return ok_moara_lin or ok_moara_col

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
                        try:
                            self.l_succesori.append(self.eliminare_piesa(stare=self, lin=i, col=j))
                        except ValueError:
                            continue
                    else:
                        if (self.jucator_curent_alb and self.piese_albe_nefolosite > 0) or ((not self.jucator_curent_alb) and self.piese_negre_nefolosite > 0):
                            try:
                                self.l_succesori.append(self.adaugare_piesa(stare=self, lin=i, col=j))
                            except ValueError:
                                continue
                        else:
                            if self.matrix[i][j] == self.jucator_curent_alb:
                                if (self.jucator_curent_alb and self.piese_albe_pe_tabla > 3) or ((not self.jucator_curent_alb) and self.piese_negre_pe_tabla > 3):
                                    for lin, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                                        try:
                                            """
                                            obtinem linia si coloana reala a pozitiei curente. Apoi ne uitam sus, jos, stanga, dreapta, iar pt acele pozitii care exista
                                            obtinem linia si coloana din matrice la care se afla elementul adiacent. Daca este o pozitie libera, generam un nou succesor
                                            """
                                            linie_reala_actuala, coloana_reala_actuala = Stare.decodif_poz_matrice[i * 3 + j]
                                            idx_pozitie_noua = Stare.decodif_poz_matrice.index((linie_reala_actuala + lin * max(1, abs(coloana_reala_actuala - 4)), coloana_reala_actuala + col * max(1, abs(linie_reala_actuala - 4))))
                                            self.l_succesori.append(self.muta_piesa(stare=self, old_lin=i, old_col=j, new_lin=idx_pozitie_noua // 3, new_col=idx_pozitie_noua % 3))
                                        except ValueError:
                                            continue
                                else:
                                    """
                                    au ramas 3 piese pentru jucatorul curent, deci poate sa sara cum vrea
                                    """
                                    for lin in range(8):
                                        for col in range(3):
                                            if self.matrix[lin][col] is None:
                                                try:
                                                    self.l_succesori.append(self.muta_piesa(stare=self, old_lin=i, old_col=j, new_lin=lin, new_col=col))
                                                except ValueError:
                                                    continue
        return self.l_succesori

    @classmethod
    def muta_piesa(cls, stare, old_lin, old_col, new_lin, new_col):
        if stare.matrix[new_lin][new_col] is None:
            new_matrix = copy.deepcopy(stare.matrix)
            new_matrix[old_lin][old_col] = None
            new_matrix[new_lin][new_col] = stare.jucator_curent_alb
            eliminare = Stare.este_in_moara(new_matrix, (new_lin, new_col))
            if eliminare:
                jucator_nou = stare.jucator_curent_alb
            else:
                jucator_nou = not stare.jucator_curent_alb
            stare_noua = Stare(tata=stare, matrix=new_matrix, piese_albe_nefolosite=stare.piese_albe_nefolosite, piese_albe_pe_tabla=stare.piese_albe_pe_tabla,
                               piese_negre_pe_tabla=stare.piese_negre_pe_tabla, piese_negre_nefolosite=stare.piese_negre_nefolosite, se_scoate_o_piesa=eliminare, jucator_curent_alb=jucator_nou)
            return stare_noua
        else:
            raise ValueError

    @classmethod
    def eliminare_piesa(cls, stare, lin, col):
        if (not stare.jucator_curent_alb) == stare.matrix[lin][col] and (not Stare.este_in_moara(stare.matrix, (lin, col))):
            new_matrix = copy.deepcopy(stare.matrix)
            new_matrix[lin][col] = None
            negre_ramase = stare.piese_negre_pe_tabla
            albe_ramase = stare.piese_albe_pe_tabla
            if stare.jucator_curent_alb:
                negre_ramase -= 1
            else:
                albe_ramase -= 1
            stare_noua = Stare(tata=stare, matrix=new_matrix, piese_albe_nefolosite=stare.piese_albe_nefolosite, piese_albe_pe_tabla=albe_ramase,
                               piese_negre_pe_tabla=negre_ramase, piese_negre_nefolosite=stare.piese_negre_nefolosite, se_scoate_o_piesa=False, jucator_curent_alb=not stare.jucator_curent_alb)
            return stare_noua
        else:
            raise ValueError

    @classmethod
    def adaugare_piesa(cls, stare, lin, col):
        if stare.matrix[lin][col] is None:
            negre_nefolosite = stare.piese_negre_nefolosite
            negre_ramase = stare.piese_negre_pe_tabla
            albe_nefolosite = stare.piese_albe_nefolosite
            albe_ramase = stare.piese_albe_pe_tabla
            if stare.jucator_curent_alb:
                albe_ramase += 1
                albe_nefolosite -= 1
            else:
                negre_ramase += 1
                negre_nefolosite -= 1
            new_matrix = copy.deepcopy(stare.matrix)
            new_matrix[lin][col] = stare.jucator_curent_alb
            eliminare = Stare.este_in_moara(new_matrix, (lin, col))
            if eliminare:
                jucator_nou = stare.jucator_curent_alb
            else:
                jucator_nou = not stare.jucator_curent_alb
            stare_noua = Stare(tata=stare, matrix=new_matrix, piese_albe_nefolosite=albe_nefolosite, piese_albe_pe_tabla=albe_ramase,
                               piese_negre_pe_tabla=negre_ramase, piese_negre_nefolosite=negre_nefolosite, se_scoate_o_piesa=eliminare, jucator_curent_alb=jucator_nou)
            return stare_noua
        else:
            raise ValueError


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
        self.stare_initiala = Stare(Stare.generare_matrice())
        self.stare_curenta = self.stare_initiala
        self.add_buttons(5)
        self.poz_piesa_care_se_muta = None

        self.board_frame.grid(row=1, column=1)

        self.mainloop()

    def play_next_move(self, poz):
        idx = Stare.decodif_poz_matrice.index(poz)
        lin, col = (idx // 3, idx % 3)
        if self.stare_curenta.se_scoate_o_piesa:
            """
            se scoate o piesa a adversarului care nu este in moara
            """
            self.eliminare_piesa(idx=idx, lin=lin, col=col)
        else:
            if (self.stare_curenta.jucator_curent_alb and self.stare_curenta.piese_albe_nefolosite > 0) or ((not self.stare_curenta.jucator_curent_alb) and self.stare_curenta.piese_negre_nefolosite > 0):
                """
                se adauga o noua piese pe o pozitie goala
                """
                self.adaugare_piesa(idx=idx, lin=lin, col=col)
            else:
                """
                se muta o piesa
                """
                self.mutare_piesa(poz=poz, idx=idx, lin=lin, col=col)

    def add_buttons(self, dim):
        for lin, col in Stare.decodif_poz_matrice:
            button = tkinter.Button(self.board_frame, height=dim, width=dim, command=functools.partial(self.play_next_move, (lin, col)), bg="grey", activebackground='green')
            button.grid(row=lin, column=col)
            MorrisBoard.buttons.append(button)

    def eliminare_piesa(self, idx, lin, col):
        try:
            if self.stare_curenta.matrix[lin][col] == (not self.stare_curenta.jucator_curent_alb) and (not Stare.este_in_moara(self.stare_curenta.matrix, (lin, col))):
                stare = Stare.eliminare_piesa(stare=self.stare_curenta, lin=lin, col=col)
                if stare in self.stare_curenta.generare_succesori():
                    self.stare_curenta = stare
                    MorrisBoard.buttons[idx].configure(bg='grey')
        except ValueError:
            return

    def adaugare_piesa(self, idx, lin, col):
        try:
            if self.stare_curenta.matrix[lin][col] is None:
                stare = Stare.adaugare_piesa(stare=self.stare_curenta, lin=lin, col=col)
                if stare in self.stare_curenta.generare_succesori():
                    if self.stare_curenta.jucator_curent_alb:
                        MorrisBoard.buttons[idx].configure(bg='white')
                    else:
                        MorrisBoard.buttons[idx].configure(bg='black')
                    self.stare_curenta = stare
        except ValueError:
            return

    def mutare_piesa(self, poz, idx, lin, col):
        try:
            if self.poz_piesa_care_se_muta is None:
                if self.stare_curenta.matrix[lin][col] == self.stare_curenta.jucator_curent_alb:
                    self.poz_piesa_care_se_muta = poz
                    MorrisBoard.buttons[idx].configure(bg='cyan')
            else:
                old_idx = Stare.decodif_poz_matrice.index(self.poz_piesa_care_se_muta)
                old_lin, old_col = (old_idx // 3, old_idx % 3)
                if self.stare_curenta.jucator_curent_alb:
                    MorrisBoard.buttons[old_idx].configure(bg='white')
                else:
                    MorrisBoard.buttons[old_idx].configure(bg='black')
                if self.stare_curenta.matrix[lin][col] is None:
                    stare = Stare.muta_piesa(stare=self.stare_curenta, old_lin=old_lin, old_col=old_col, new_lin=lin, new_col=col)
                    if stare in self.stare_curenta.generare_succesori():
                        MorrisBoard.buttons[old_idx].configure(bg='grey')
                        if self.stare_curenta.jucator_curent_alb:
                            MorrisBoard.buttons[idx].configure(bg='white')
                        else:
                            MorrisBoard.buttons[idx].configure(bg='black')
                        self.stare_curenta = stare
                self.poz_piesa_care_se_muta = None
        except ValueError:
            return


if __name__ == "__main__":
    MorrisBoard()
