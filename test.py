from spillbrett import Spillbrett
from sau import Sau
from gress import Gress
from sauehjerne import finn_vanligste_element_i_liste


def test_avstand():
    spillbrett = Spillbrett(3000)
    sau = Sau("sau", 400, 500, spillbrett)
    gress1 = Gress("gress", 100, 100)
    gress2 = Gress("gress", 200, 200)
    gress3 = Gress("gress", 300, 300)
    hjerne = sau.sauehjerne()
    assert hjerne.avstand_til_objekt(gress1) == 14, "Avstanden er feil"
    assert hjerne.avstand_til_objekt(gress2) == 10, "Avstanden er feil"
    assert hjerne.avstand_til_objekt(gress3) == 6, "Avstanden er feil"


def test_retning():
    spillbrett = Spillbrett(3000)
    sau = Sau("sau", 400, 500, spillbrett)
    gress1 = Gress("gress", 500, 400)
    hjerne = sau.sauehjerne()
    assert set(retninger) == set(["opp", "venstre"])


def finn_vanligste_element_i_liste(liste):
    if len(liste) == 1:
        return liste[0]
    elementer = {}

    # Dette funker bare dersom elementer i listen er strings
    for i in liste:
        if i not in elementer:
            elementer[i] = 0
        else:
            elementer[i] += 1

    max_element = None
    max_antall = 0

    for i in elementer:
        if max_element == None:
            if elementer[i] >= 0:
                max_element = i
                max_antall = 0
        else:
            if elementer[i] > max_antall:
                max_element = i
                max_antall = elementer[i]

    if max_element == None:
        return []

    return max_element


def test_finn_vanligste_element_i_liste():
    assert finn_vanligste_element_i_liste(["ned", "ned", "opp"]) == "ned"
    assert finn_vanligste_element_i_liste(["ned", "venstre", "opp", "venstre"]) == "venstre"
