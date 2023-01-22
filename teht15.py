# -----------------------------------------------------------------------------

# Ohjelma kysyy käyttäjältä toimintoa, jonka mukaan se lataa ja tallentaa ohjeen mukaisen 
# kuvan NASA:n sivustolta.

# Versio 1.0

# (C) 2021 Nina Laaksonen, Tampere, Suomi

# Sähköposti nina.laaksonen@gmail.com

# Teamissa ei ole vielä ketään, koska olen vähän kiirehtinyt.

# -----------------------------------------------------------------------------

import datetime, os, urllib.request, random

def paivamaara():
    """Muodostaa ja palauttaa tämän päivän päivämäärän"""
    paivamaara = datetime.date.today()
    return paivamaara

def kansion_checks(polku):
    """Tarkistaa kansion olemassaolon ja luo sellaisen, jos ei ole olemassa."""  
    if os.path.isdir(polku) == False:
        os.mkdir(polku)

def kansioiden_luonti(pvm):
    """Luo kaikki tarvittavat kansiot homedir:n
    palauttaa:
        lopullinen polku, luodun tallennettavan tiedoston nimi"""
    vuosi = pvm.strftime("%Y")
    kuu = pvm.strftime("%m")
    pva = pvm.strftime("%d")
    # luo ensimmäisen polun ja tarkistaa onko polku jo olemassa, jos ei: luo sen
    polku = os.path.expanduser("~") + f"\{vuosi}"   
    kansion_checks(polku)
    # luo pidemmän polun ja tarkastaa onko se jo olemassa, jos ei: luo sen
    polku = polku + f"\{kuu}"
    kansion_checks(polku)
    # luo tallennettavan tiedoston nimen jo valmiiksi jatkokäyttöä varten
    filename = f"{vuosi}-{kuu}-{pva}"
    return polku, filename

def hae_kuva(polku, filename):
    """"Hakee kuvan annetulta sivustolta pvm mukaan ja palauttaa kansio-pathin 
    ja totuusarvon vikojen estämiseksi
    Palauttaa: tallennusosoite, totuusarvo"""
    urli = f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={filename}"
    osoite = f"{polku}\\{filename}.jpg"
    totuus = os.path.isfile(osoite)
    # Kokeilee tuleeko sivuston avaamisen yhteydessä erroria ja jos tulee:
    # palauttaa vain osoitteen ja totuusarvon testauksia varten, muuten:
    # avaa sivuston käytön ajaksi, lukee sen, muuntaa byten -> merkkijono ->
    # sanakirja ja poimii sanakirjasta kuvan tiedon
    try:
        with urllib.request.urlopen(urli) as vastaus:
            tieto = vastaus.read()
            tieto = tieto.decode("UTF-8")
            tieto = eval(tieto)
    except urllib.error.URLError:
        print("Tiedoston haku sivustolta epäonnistui: netti ei toimi tai käyttöoikeuksissa on vikaa.")
        return osoite, True
    # Jos tahtoo normaalikokoisen kuvan (ei HD), voi tämän vaihtaa käyttöön:
    #kuvaosoite = tieto["url"] 
    kuvaosoite = tieto["hdurl"] 
    # jos tiedosto oli jo olemassa, ilmoittaa siitä
    if totuus:
        print("Tiedosto oli jo olemassa.")
    # Yrittää noutaa tiedoston kuva-urlista ja palauttaa kommentin jos ei onnaa
    elif totuus != True:
        try:
            urllib.request.urlretrieve(kuvaosoite, osoite)
        except urllib.error.ContentTooShortError():
            print("Tila koneeltasi on lopussa tai ladattava tiedosto on read only.")
    return osoite, totuus

def randpvm_luonti(pvm):
    """Luo ja palauttaa randomin päivämäärän 16.6.1995 - tämä päivä -väliltä"""
    alkupvm = datetime.date(1995, 6, 16)
    aikavali = pvm - alkupvm  # aikaobjektien välinen aikaväli
    pvat_valissa = aikavali.days  # aikaobjektien välinen aikaväli päivinä
    # Valitsee päivien määrän ja 0 välistä numeron
    randmaara = random.randrange(pvat_valissa) 
    # lisää alkupäivämäärään aiemmin määritellyn randomin määrän päiviä
    randpvm = alkupvm + datetime.timedelta(days=randmaara)
    return randpvm

def paaohjelma():
    """Pääfunktio, joka pyytää käyttäjältä toimintoa ja toimii sen mukaisesti"""
    # Luo päivämäärän ja sille "hyvänmallisen" merkkijonon
    pvm = paivamaara()
    pvmstr = pvm.strftime("%d.%m.%Y")
    # Kysyy ohjeenmukaisia toimintoja käyttäjältä ja toimii niiden mukaisesti
    while True:
        print(f"Mitä haluat tehdä:\n1 - ladata tämän päivän astronomisen kuvan.\n2 - ladata eilisen päivän astronomisen kuvan.\n3 - ladata satunnaisen astronomisen kuvan väliltä: 16.6.1995 - {pvmstr}\n0 - lopettaa ohjelma")
        toiminto = input("Syötä toiminto: ")
        # Jos toiminto on 0, ohjelma lopetetaan
        if toiminto == "0":
            print("Kiitos ohjelman käytöstä.")
            break

        # Jos toiminto on 1, yrittää luoda kansiot tälle päivälle ja tallentaa 
        # tämän päivän kuvan.
        elif toiminto == "1":
            filename = kansioiden_luonti(pvm)
            hakemisto = hae_kuva(filename[0], filename[1])
            # Jos on ongelmia ollut, ei tulosta onnistumisriviä: ohjelma jatkuu
            if hakemisto[1]:
                continue
            else:  #.. muuten kertoo mitä teki ja minne.
                print("Päivän astronomikuva on tallennettu nimellä hakemistoon:", hakemisto[0])   

        # Jos toiminto on 2, yrittää luoda kansion eiliselle ja yrittää 
        # tallentaa eilisen kuvan.
        elif toiminto == "2":
            # luon muuttujan tän päivän päivämäärästä miinus yks päivä
            eilinen = pvm - datetime.timedelta(days=1)
            filename = kansioiden_luonti(eilinen)
            hakemisto = hae_kuva(filename[0], filename[1])
            # Jos on ongelmia ollut, ei tulosta onnistumisriviä: ohjelma jatkuu
            if hakemisto[1]:
                continue
            else:  #.. muuten kertoo mitä teki ja minne.
                print("Eilisen päivän astronominen kuva on tallennettu hakemistoon:", hakemisto[0])
        # Jos toiminto on 3, yrittää luoda kansion random päivämäärälle ja
        # yrittää tallentaa sen päivän kuvan.
        elif toiminto == "3":
            # luo muuttujan kutsuen randomin päivämäärän luonti -funktioo.
            randpvm = randpvm_luonti(pvm)
            filename = kansioiden_luonti(randpvm)
            hakemisto = hae_kuva(filename[0], filename[1])
            # Jos on ongelmia ollut, ei tulosta onnistumisriviä: ohjelma jatkuu
            if hakemisto[1]:
                continue
            else:  #.. muuten kertoo mitä teki ja minne.
                print("Satunnaisen päivän astronominen kuva on tallennettu hakemistoon:", hakemisto[0])
        # Jos toimintoa ei ole koodattu tähän, se kertoo käyttäjälle palautetta.
        else: 
            print("Toimintoon ei ole ohjelmoitu mitään, yritä uudelleen.")
            

if __name__ == "__main__":
    paaohjelma()

