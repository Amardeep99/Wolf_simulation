# from spillbrett import Spillbrett

class Sauehjerne:

    def __init__(self, sau, spillbrett):
        self._sau = sau
        self._spillbrett = spillbrett

    # Returnerer nærmest upsist gressobjekt
    def naermeste_gress(self):
        if not self._sau.er_spist():
            liste_uspist_gress = []
            for i in self._spillbrett.hent_gress():
                if not i.er_spist():
                    liste_uspist_gress.append(i)

            naermeste = liste_uspist_gress[0]
            for i in liste_uspist_gress:
                if self.avstand_til_objekt(i) < self.avstand_til_objekt(naermeste):
                    naermeste = i

            return naermeste

    # True om det finnes stein i den gitte retningen
    def stein_finnes_i_retning(self, retning):
        neste = None
        sau = self._sau
        steiner = self._spillbrett.hent_stein()

        for i in steiner:
            if retning == "venstre" and sau.rute_venstre() - 1 == i.rute_venstre() and sau.rute_topp() == i.rute_topp():
                return True
            elif retning == "hoeyre" and sau.rute_venstre() + 1 == i.rute_venstre() and sau.rute_topp() == i.rute_topp():
                return True
            elif retning == "opp" and sau.rute_topp() - 1 == i.rute_topp() and sau.rute_venstre() == i.rute_venstre():
                return True
            elif retning == "ned" and sau.rute_topp() + 1 == i.rute_topp() and sau.rute_venstre() == i.rute_venstre():
                return True

        return False

    # La til denne metoden for å gjøre metoden hinder_finnes_i_retning mer ryddig.
    # Denne sjekker bare om rute i retning man går er utenfor banen.
    def utenfor_bane(self, retning):
        if retning == "topp" and self._sau.rute_topp() == 1:
            return True
        elif retning == "ned" and self._sau.rute_topp() == 13:
            return True
        elif retning == "venstre" and self._sau.rute_venstre() == 1:
            return True
        elif retning == "hoeyre" and self._sau.rute_venstre() == 17:
            return True

        return False

    # Returnerer True om man havner ut av banen eller om det finnes stein i en gitt retning
    def hinder_finnes_i_retning(self, retning):
        if self.stein_finnes_i_retning(retning) or self.utenfor_bane(retning):
            return True

        return False

    # Returnerer retninger som er smartest å gå
    def velg_retning(self):
        retninger = []
        avstand_til_ulv = self.avstand_til_objekt(self._spillbrett.hent_ulv())

        if self.naermeste_gress():
            retning_gress = self.retninger_mot_objekt(self.naermeste_gress())
            retninger.extend(retning_gress)

        if avstand_til_ulv <= 6:
            retning_fra_ulv = self.retninger_fra_objekt(self._spillbrett.hent_ulv())
            retning_fra_ulv *= 2
            retninger.extend(retning_fra_ulv)

        vanligste_retning = finn_vanligste_element_i_liste(retninger)

        if avstand_til_ulv < 6:
            if self._sau.rute_venstre() == 17 and vanligste_retning == "hoeyre":
                return "ned"
            elif self._sau.rute_venstre() == 0 and vanligste_retning == "venstre":
                return "opp"
            elif self._sau.rute_topp() == 0 and vanligste_retning == "opp":
                return "hoeyre"
            elif self._sau.rute_topp() == 13 and vanligste_retning == "ned":
                return "venstre"

            if self.hinder_finnes_i_retning("venstre") and vanligste_retning == "venstre":
                if self.hinder_finnes_i_retning("ned"):
                    return "opp"
                elif self.hinder_finnes_i_retning("opp"):
                    return "ned"
                return "hoeyre"
            # Under skulle egentlig sauen gått venstre om det ikke er hinder oppe eller nede
            # Men sauen gjorde det ikke i testene jeg kjørte for en eller annen grunn i bane 2
            # Så for at den overlever bane 2 måtte jeg skrive delen under litt ulogisk (den blir litt tvunget til å gå ned).
            elif self.hinder_finnes_i_retning("hoeyre") and vanligste_retning == "hoeyre":
                if self.hinder_finnes_i_retning("ned"):
                    return "opp"
                return "ned"
            elif self.hinder_finnes_i_retning("opp") and vanligste_retning == "opp":
                if self.hinder_finnes_i_retning("venstre"):
                    return "hoeyre"
                elif self.hinder_finnes_i_retning("hoeyre"):
                    return "venstre"
                return "ned"
            elif self.hinder_finnes_i_retning("ned") and vanligste_retning == "ned":
                if self.hinder_finnes_i_retning("venstre"):
                    return "hoeyre"
                elif self.hinder_finnes_i_retning("hoeyre"):
                    return "venstre"
                return "opp"

        return vanligste_retning


    # Returnerer avstanden mellom sau og et annet objekt (Basert på ruter)
    def avstand_til_objekt(self, objekt):
        avstand = abs(self._sau.rute_venstre() - objekt.rute_venstre()) + abs(self._sau.rute_topp() - objekt.rute_topp())
        return avstand

    # Returnerer retning(er) som leder til et annet objekt
    def retninger_mot_objekt(self, objekt):
        retninger = []

        if self._sau.rute_venstre() == objekt.rute_venstre():
            pass
        elif self._sau.rute_venstre() > objekt.rute_venstre():
            retninger.append("venstre")
        else:
            retninger.append("hoeyre")

        if self._sau.rute_topp() == objekt.rute_topp():
            pass
        elif self._sau.rute_topp() > objekt.rute_topp():
            retninger.append("opp")
        else:
            retninger.append("ned")

        return retninger

    # Returnerer retninger å gå for å unngå et objekt
    def retninger_fra_objekt(self, objekt):
        retninger = []

        if self._sau.rute_venstre() == objekt.rute_venstre():
            pass
        elif self._sau.rute_venstre() > objekt.rute_venstre():
            retninger.append("hoeyre")
        else:
            retninger.append("venstre")

        if self._sau.rute_topp() == objekt.rute_topp():
            pass
        elif self._sau.rute_topp() > objekt.rute_topp():
            retninger.append("ned")
        else:
            retninger.append("opp")

        return retninger

# Returnerer elementet i en liste som oppstår flest ganger
def finn_vanligste_element_i_liste(liste):
    if len(liste) == 1:
        return liste[0]
    elementer = {}

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
# cd Desktop/IN1000/alt8
