from abc import ABC, abstractmethod
import random

# abstraktne baasklass "Tegelane"
class Tegelane(ABC):
    # Kirjuta konstruktor (__init__), mis võtab:
    #   nimi (str), elu (int)
    # NÕUE (kapseldamine): salvesta need _nimi ja _elu väljadena
    def __init__(self, nimi, elu):
        self._nimi = nimi
        self._elu = elu

    # Lisa meetod on_elus(), mis tagastab True kui elu > 0
    def on_elus(self):
        try:
            if self._elu > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Viga: {e}")

    # Lisa meetod võta_kahju(kogus), mis vähendab elupunkte
    # NÕUE: elu ei tohi minna negatiivseks (min 0)
    def võta_kahju(self, kogus):
        try:
            if not isinstance(kogus, int):
                raise TypeError

            self._elu -= kogus
            if self._elu < 0:
                self._elu = 0

        except Exception as e:
            print(f"Viga: {e}")

    # Lisa meetod seisund(), mis tagastab alati teksti:
    #   "<nimi>: <elu> elu"
    # (Maag ja Vibukütt teevad selle üle ja lisavad ressursi)
    def seisund(self):
        try:
            return f"{self._nimi}: {self._elu} elu"

        except Exception as e:
            print(f"Viga: {e}")

    # Tee abstraktne meetod ründa(vastane)
    @abstractmethod
    def ründa(self, vastane):
        pass

# Loo klass Sõdalane, mis PÄRIB klassist Tegelane
class Sõdalane(Tegelane):
    # Konstruktor: sõdalasel olgu nt 100 elu
    def __init__(self, nimi):
        super().__init__(nimi=nimi, elu=100)

    # Realiseeri ründa()
    # NÕUE: tekita juhuslik kahju vahemikus 10..20, rakenda vastasele
    # NÕUE: print peab olema arusaadav (näiteks: "Karl lõi Mari ja tegi 12 kahju.")
    def ründa(self, vastane):
        try:
            kahju = random.randint(10, 20)
            print(f"{self._nimi} andis mõõgahoobi ja {vastane._nimi} sai {kahju} kahju.")
            vastane.võta_kahju(kahju)
        except Exception as e:
            print(f"Viga: {e}")

# Loo klass Maag, mis PÄRIB klassist Tegelane
class Maag(Tegelane):
    # Konstruktor: maagil nt 70 elu ja lisaks _mana = 30 (kapseldamine)
    def __init__(self, nimi):
        super().__init__(nimi=nimi, elu=70)
        self._mana = 30

    # Kirjuta seisund() üle nii, et tagastab:
    #   "<nimi>: <elu> elu, <mana> mana"
    def seisund(self):
        return f"{self._nimi}: {self._elu} elu, {self._mana} mana"

    # Realiseeri ründa()
    # NÕUE:
    #  - Kui mana >= 5: kahju 15..25, mana -5, vastane võtab kahju
    #  - Kui mana < 5: rünnak ei õnnestu (prindi teade, kus on sõna "mana")
    # NÕUE: mana ei tohi minna negatiivseks
    def ründa(self, vastane):
        try:
            if self._mana < 5:
                print("Liiga vähe mana")
            else:
                kahju = random.randint(15, 25)
                print(f"{self._nimi} lausus loitsu ja {vastane._nimi} sai {kahju} kahju.")
                vastane.võta_kahju(kahju)
                self._mana -= 5

        except Exception as e:
            print(f"Viga: {e}")

# Loo klass Vibukütt, mis PÄRIB klassist Tegelane
class Vibukütt(Tegelane):
    # Konstruktor: vibukütil nt 80 elu ja _nooled = 5
    def __init__(self, nimi):
        super().__init__(nimi=nimi, elu=80)
        self._nooled = 5

    # Kirjuta seisund() üle nii, et tagastab:
    #   "<nimi>: <elu> elu, <nooled> noolt"
    def seisund(self):
        return f"{self._nimi}: {self._elu} elu, {self._nooled} noolt"

    # Realiseeri ründa()
    # NÕUE:
    #  - Kui nooli > 0: kahju 8..18, nool -1, vastane võtab kahju
    #  - Kui nooli == 0: rünnak ei õnnestu (prindi teade, kus on sõna "nool")
    # NÕUE: noolte arv ei tohi minna negatiivseks
    def ründa(self, vastane):
        try:
            if self._nooled == 0:
                print("Nooled on otsas")
            else:
                kahju = random.randint(8, 18)
                print(f"{self._nimi} lasi noole ja {vastane._nimi} sai {kahju} kahju.")
                vastane.võta_kahju(kahju)
                self._nooled -= 1

        except Exception as e:
            print(f"Viga: {e}")

######################################################################################

# Realiseeri lahing(t1, t2)
# NÕUE (polümorfism): ära kasuta if/elif kontrolli tüübi järgi!
# Lihtsalt kutsu t1.ründa(t2) ja t2.ründa(t1)
#
# UUS NÕUE: iga käigu lõpus prindi:
#   "Seis: <t1.seisund()> | <t2.seisund()>"
def lahing(t1, t2):
    # prindi algus + algseis (kasuta seisund())
    # print("Algab lahing:", ...)
    # print("Algseis:", t1.seisund(), "|", t2.seisund())

    print(f"Algab lahing: {t1._nimi} vs {t2._nimi}")
    print(f"Algseis: {t1.seisund()} | {t2.seisund()}")
    kord = 1

    while t1.on_elus() and t2.on_elus():
        print("\nKäik", kord)

        # t1 ründab t2
        t1.ründa(t2)
        # kui t2 on elus, siis t2 ründab t1
        if t2.on_elus():
            t2.ründa(t1)

        # prindi alati seis (kasuta seisund())
        # print("Seis:", t1.seisund(), "|", t2.seisund())
        print(f"Seis: {t1.seisund()} | {t2.seisund()}")

        kord += 1

    # prindi võitja nimi ("Võitja on ...")
    võitja = t1 if t1.on_elus() else t2
    print(f"Võitja on {võitja._nimi}")

# Siit allapoole ei pea enam muutma:
if __name__ == "__main__":
    sõdalane = Sõdalane("Karl")
    maag = Maag("Liisa")
    vibukütt = Vibukütt("Mari")

    #lahing(sõdalane, maag)
    #lahing(vibukütt, sõdalane)
    #lahing(maag, vibukütt)

# Uue tegelase lisamisegks tuleb luua uus alamklass nt Slamõrtsukas(Tegelane):
# Seejärel implementeerida kõik vastavad meetodid
#
#