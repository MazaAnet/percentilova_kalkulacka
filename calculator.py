def vstupni_cislo(prompt, error_text, typ_cisla=float, nula=False):
    """
    Upravuje vstupní data
    """
    while True:
        hodnota = input(prompt).replace(",", ".").strip()
        try:
            cislo = typ_cisla(hodnota)
            if not nula and cislo == 0:
                print(error_text + " Hodnota nemůže být 0!")
                continue
            return cislo
        except ValueError:
            print(error_text + " Zadali jste neplatnou hodnotu!")

vek = vstupni_cislo("Věk (měsíce): ", "Chyba ve vstupu věku!", float)
hmotnost = vstupni_cislo("Hmotnost (kg): ", "Chyba ve vstupu hmotnosti!", float)
vyska = vstupni_cislo("Délka/výška (cm): ", "Chyba ve vstupu délky/výšky!", float)

while True: # ošetření vstupu hodnoty pohlaví
    pohlavi = input("Zadejte pohlaví (dívka = F/chlapec = M):").upper().strip()
    if pohlavi in ('F', 'M'):
        break
    print("Zadejte M nebo F!")

import csv

data = {}

with open('percentiles.csv', 'r', encoding='utf-8') as soubor:
    reader = csv.DictReader(soubor)
    for radek in reader:
        percentil_pohlavi = radek['pohlavi']
        percentil_vek = float(radek['vek'])
        if percentil_pohlavi not in data:
            data[percentil_pohlavi] = {}
        data[percentil_pohlavi][percentil_vek] = {
            'vyska': {
                'p3': float(radek['p3_vyska']),
                'p50': float(radek['p50_vyska']),
                'p97': float(radek['p97_vyska']),
            },
            'hmotnost': {
                'p3': float(radek['p3_hmotnost']),
                'p50': float(radek['p50_hmotnost']),
                'p97': float(radek['p97_hmotnost']),
            }
        }

class Percentily:
    def __init__(self, data):
        self.data = data

    def nejblizsi_vek(self, pohlavi, vek): #"pohlavi" je klíč k hodnotě věku
        """
        Hledá nejbližši věk, pro který jsou v csv souboru data
        """
        return min(self.data[pohlavi].keys(), key=lambda vek_z_dat: abs(vek_z_dat - vek))

    def percentilove_rozmezi(self, pohlavi, vek, typ, hodnota):
        """
        Pro nalezený nejbližší věk hledá příslušné hodnoty percentilů p3, p50, p97
        a vyhodnocuje do jakého pásma spadají vstupní hodnoty
        """
        nej_vek = self.nejblizsi_vek(pohlavi, vek)
        vstup_dat = self.data[pohlavi][nej_vek]

        if typ == 'vyska':
            p3 = vstup_dat['vyska']['p3']
            p50 = vstup_dat['vyska']['p50']
            p97 = vstup_dat['vyska']['p97']
        elif typ == 'hmotnost':
            p3 = vstup_dat['hmotnost']['p3']
            p50 = vstup_dat['hmotnost']['p50']
            p97 = vstup_dat['hmotnost']['p97']

        if hodnota < p3:
            return "podlimitní (pod percentilem 3)", nej_vek, p3, p97, p50
        elif hodnota > p97:
            return "nadlimitní (nad percentilem 97)", nej_vek, p3, p97, p50
        else:
            return "v optimálním rozmezí ", nej_vek, p3, p97, p50

p = Percentily(data)

vysledek_vyska = p.percentilove_rozmezi(pohlavi, vek, 'vyska', vyska)
vysledek_hmotnost = p.percentilove_rozmezi(pohlavi, vek, 'hmotnost', hmotnost)

print(f"\nZadáno:"
      f"\nvěk {vek} měsíců"
      f"\ndélka/výška {vyska} cm"
      f"\nhmotnost {hmotnost} kg"
      f"\npohlaví (M=chlapec, F=dívka) {pohlavi}")
print("\nVýsledky:")
print(f"Délka/výška: {vysledek_vyska[0]}")
print(f"Pro věk {int(vysledek_vyska[1])} měsíců je optimální délka/výška v "
      f"rozmezí {vysledek_vyska[2]}-{vysledek_vyska[3]} cm,"
      f"\npercentil 50 je {vysledek_vyska[4]} cm.")
print(f"\nHmotnost: {vysledek_hmotnost[0]}")
print(f"Pro věk {int(vysledek_hmotnost[1])} měsíců je optimální hmotnost v "
      f"rozmezí {vysledek_hmotnost[2]}-{vysledek_hmotnost[3]} kg,"
      f"\npercentil 50 je {vysledek_hmotnost[4]} kg.")


