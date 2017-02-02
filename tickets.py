import flights
from datetime import date
from datetime import datetime
from datetime import timedelta
import dates

def loadkarte():
    for line in open('karte.txt', 'r'):
        if len(line) > 1:
            karta = str2kar(line)
            karte.append(karta)


def str2kar(line):
    if line[-1] == '\n':
        line = line[:-1]
    brojleta, polaziste, odrediste, polazak, dolazak, prevoznik, dani, model, cena,\
    datum, ime, prezime, drzavljanstvo, pasos, datumprodaje, prodavac, mesto = line.split('|')
    karta = {
        'brojleta': brojleta,
        'polaziste': polaziste,
        'odrediste': odrediste,
        'polazak': polazak,
        'dolazak': dolazak,
        'prevoznik': prevoznik,
        'dani': dani,
        'model': model,
        'cena': cena,
        'datum': datum,
        'ime' : ime,
        'prezime' : prezime,
        'drzavljanstvo' : drzavljanstvo,
        'pasos': pasos,
        'datumprodaje' : datumprodaje,
        'prodavac' : prodavac,
        'mesto' : mesto
    }
    return karta

def unos():
    brojleta = raw_input("\nUnesite broj leta koji zelite da rezervisete: ")
    datum = raw_input("Unesite datum kada zelite da letite (format dd-mm-yyyy): ")
    ime = raw_input("Ime: ")
    prezime = raw_input("Prezime: ")
    drzavljanstvo = raw_input("Drzavljanstvo: ")
    pasos = raw_input("Broj pasosa: ")
    prodavac = raw_input("Prodavac: ")
    datumprodaje = str(date.today())
    if proverabroja(brojleta) == False:
        print "\nNe postoji let sa brojem", brojleta, ". Izaberite drugi let."
        unos()
    if proveradatuma(brojleta, datum) == False:
        print "\nTaj let ne postoji na datum", datum, ". Izaberite drugi let."
        unos()
    if proverasedista(brojleta, datum) == False:
        print "\n U letu sa brojem", brojleta, "za datum", datum, "nema slobodnih mesta. Izaberite drugi let."
        unos()
    rezervacija(brojleta, datum, ime, prezime, drzavljanstvo, pasos, prodavac, datumprodaje)
    print "\n Ako zelite da rezervisete jos jedan let, unesite 1. U suprotnom, unesite 0."
    komanda = raw_input(">> ")
    if komanda == '1':
        uslovniunosprovera(brojleta, datum)
    else:
        stampajkarte()


def proverabroja(brojleta):
    for let in flights.letovi:
        if let['brojleta'] == brojleta:
            return True
    return False

def proveradatuma(brojleta, datum):
    for let in flights.letovi:
        if let['brojleta'] == brojleta:
            days = let['dani'].split(',')
            for day in days:
                if day == dates.obradadatuma(datum):
                    return True
            return False

def proverasedista(brojleta, datum):
    for let in flights.letovi:
        if let['brojleta'] == brojleta:
            dimenzija = let['model'].split('/')
            brojsedista = eval(dimenzija[0]) * eval(dimenzija[1])
            rezervisano = 0
            for karta in karte:
                if karta['brojleta'] == brojleta and karta['datum'] == datum:
                    rezervisano = rezervisano + 1
            if brojsedista >= rezervisano:
                return True
            return False

def rezervacija(brojleta, datum, ime, prezime, drzavljanstvo, pasos, prodavac, datumprodaje):
    slobodnasedista = listaslobodnih(brojleta, datum)
    sediste = raw_input("Sediste (format: red(broj) / kolona(veliko slovo): ")
    if sediste not in slobodnasedista:
        print "Pogresno ste uneli sediste. Pokusajte ponovo."
        rezervacija(brojleta, datum, ime, prezime, drzavljanstvo, pasos, prodavac, datumprodaje)
    else:
        for let in flights.letovi:
            if let['brojleta'] == brojleta:
                string = '|'.join([let['brojleta'], let['polaziste'], let['odrediste'],
                           let['polazak'], let['dolazak'], let['prevoznik'], let['dani'],
                           let['model'], let['cena'], datum, ime, prezime, drzavljanstvo,
                        pasos, datumprodaje, prodavac, sediste])
                savekarta(string)
                savekartaprivremeno(string)

def savekarta(string):
    file = open('karte.txt', 'a')
    file.write(string)
    file.write('\n')
    file.close()

def savekartaprivremeno(string):
    file = open('privremeno.txt', 'w')
    file.write(string)
    file.write('\n')
    file.close()


def dodajkartaprivremeno(string):
    file = open('privremeno.txt', 'a')
    file.write(string)
    file.write('\n')
    file.close()


def uslovniunosprovera(brojleta, datum):
    result = []
    polaziste = ""
    vreme = ""
    for let in flights.letovi:
        if let['brojleta'] == brojleta:
            polaziste = let['odrediste']
            vreme = let['dolazak']
    for let in flights.letovi:
        if let['polaziste'] == polaziste:
            if checkdatum(let, datum) == True:
                if checkvreme(let, vreme) == True:
                    result.append(let)
    print "\nMozete izabrati jedan od sledecih letova.\n"
    flights.formatheader()
    flights.formatletovi(result)
    broj = raw_input("\nUnesite broj leta koji zelite da rezervisete: ")
    uslovniunos(broj, result, datum)

def checkdatum(let, datum):
    dan = dates.datum(datum)
    days = let['dani'].split(',')
    for day in days:
        if dan == day:
            return True
    return False

def checkvreme(let, vreme):
    vremeuslovno = dodajsat(vreme)
    uslovno = datetime.strptime(vremeuslovno,'%H:%M')
    polazak = datetime.strptime(let['polazak'],'%H:%M')
    if polazak >= uslovno:
        return True
    else:
        return False

def dodajsat(vreme):
    razdvojeno = vreme.split(':')
    sati = eval(razdvojeno[0])
    minutistr = razdvojeno[1]
    sati += 1
    satistr = str(sati)
    spojeno = (':').join([satistr, minutistr])
    return spojeno

def uslovniunos(brojleta, result, datum):
    slobodnasedista = listaslobodnih(brojleta, datum)
    ime = raw_input("Ime: ")
    prezime = raw_input("Prezime: ")
    drzavljanstvo = raw_input("Drzavljanstvo: ")
    pasos = raw_input("Broj pasosa: ")
    prodavac = raw_input("Prodavac: ")
    sediste = raw_input("Sediste (format: red(broj) / kolona(veliko slovo): ")
    if sediste not in slobodnasedista:
        print "Pogresno ste uneli sediste. Pokusajte ponovo."
        uslovniunos(brojleta, result, datum)
    datumprodaje = str(date.today())
    for let in result:
        if brojleta == let['brojleta']:
            string = '|'.join([let['brojleta'], let['polaziste'], let['odrediste'],
                       let['polazak'], let['dolazak'], let['prevoznik'], let['dani'],
                       let['model'], let['cena'], datum, ime, prezime, drzavljanstvo,
                       pasos, datumprodaje, prodavac, sediste])
            savekarta(string)
            dodajkartaprivremeno(string)
    print "\n Ako zelite da rezervisete jos jedan let, unesite 1. U suprotnom, unesite 0."
    komanda = raw_input(">> ")
    if komanda == '1':
        uslovniunosprovera(brojleta, datum)
    else:
        stampajkarte()

def stampajkarte():
    privremenekarte = []
    loadprivremene(privremenekarte)
    formatheader()
    formattickets(privremenekarte)

def loadprivremene(privremenekarte):
    for line in open('privremeno.txt', 'r'):
        if len(line) > 1:
            karta = str2kar(line)
            privremenekarte.append(karta)

def formatheader():
    print "\n\n"
    print \
        "Broj leta|Polazak|Polaziste|Odrediste|Dolazak|Cena|Model|  Prevoznik  |   Datum   |Sediste|Datum prodaje|\n" \
        "---------+-------+---------+---------+-------+----+-----+-------------+-----------+-------+-------------"

def formattickets(result):
    for karta in result:
        print u"{0:9}|{1:7}|{2:9}|{3:9}|{4:7}|{5:4}|{6:5}|{7:13}|{8:11}|{9:7}|{10:>13}".format(
            karta['brojleta'],
            karta['polazak'],
            karta['polaziste'],
            karta['odrediste'],
            karta['dolazak'],
            karta['cena'],
            karta['model'],
            karta['prevoznik'],
            karta['datum'],
            karta['mesto'],
            karta['datumprodaje'])

def izmena():
    brojleta = raw_input("\nUnesite broj leta koji zelite da promenite: ")
    datum = raw_input("Unesite datum polaska: ")
    pasos = raw_input("Unesite broj pasosa: ")
    karta = findkarta(brojleta, datum, pasos)
    if karta == None:
        print "\nNe postoji takva karta u listi prodatih."
        izmena()
    komanda = izmenamenu()
    if komanda not in ('1', '2', '3'):
        print "\nUneli ste pogresnu komandu.\n"
        izmena()
    if komanda == '1':
        promenabroja(karta)
    elif komanda == '2':
        promenadatuma(karta)
    elif komanda == '3':
        promenasedista(karta)

def findkarta(brojleta, datum, pasos):
    for karta in karte:
        if karta['brojleta'] == brojleta and karta['datum'] == datum and karta['pasos'] == pasos:
            return karta

def izmenamenu():
    print "\nUnesite broj u zavisnosti sta zelite da izmenite: "
    print " 1 - Broj leta"
    print " 2 - Datum polaska"
    print " 3 - Broj sedista"
    komanda = raw_input("\n>> ")
    return komanda

def promenabroja(karta):
    i = ""
    broj = raw_input("\nUnesite broj novog leta: ")
    for let in flights.letovi:
        if let['brojleta'] == broj:
            i = let
    if checkdatum(i, karta['datum']) == False:
        print "Ne postoji let sa brojem", broj, "na datum", karta['datum'],". Unesite novi datum"
        datum = raw_input(">> ")
        karta['datum'] = datum
        promenabroja(karta)
    izbrisikartu(karta)
    rezervacija(broj, karta['datum'], karta['ime'], karta['prezime'], karta['drzavljanstvo'], karta['datum'],
                karta['prodavac'], karta['datumprodaje'])
    print "\nUspesno ste promenili kartu. Dovidjenja."

def promenadatuma(karta):
    i = ""
    datum = raw_input("\nUnesite datum novog leta: ")
    for let in flights.letovi:
        if let['brojleta'] == karta['brojleta']:
            i = let
    if checkdatum(i, datum) == False:
        print "Ne postoji let sa brojem", karta['brojleta'], "na datum", datum, ". Unesite novi datum."
        promenadatuma(karta)
    izbrisikartu(karta)
    rezervacija(karta['brojleta'], datum, karta['ime'], karta['prezime'], karta['drzavljanstvo'], karta['datum'],
                karta['prodavac'], karta['datumprodaje'])
    print "\nUspesno ste promenili kartu. Dovidjenja."

def promenasedista(karta):
    brojleta = karta['brojleta']
    datum = karta['datum']
    slobodnasedista = listaslobodnih(brojleta, datum)
    sediste = raw_input("Sediste (format: red(broj) / kolona(veliko slovo): ")
    if sediste not in slobodnasedista:
        print "Pogresno ste uneli sediste. Pokusajte ponovo."
        promenasedista(karta)
    izbrisikartu(karta)
    string = '|'.join([karta['brojleta'], karta['polaziste'], karta['odrediste'],
                       karta['polazak'], karta['dolazak'], karta['prevoznik'], karta['dani'],
                       karta['model'], karta['cena'], datum, karta['ime'], karta['prezime'], karta['drzavljanstvo'],
                       karta['pasos'], karta['datumprodaje'], karta['prodavac'], sediste])
    savekarta(string)
    savekartaprivremeno(string)


def izbrisikartu(karta):
    privremeni = []
    for card in karte:
        if card != karta:
            privremeni.append(card)
    global karte
    karte = privremeni
    zamenitekst()

def obrisi():
    broj = raw_input("\nUnesite broj leta koji zelite da otkazete: ")
    datum = raw_input("\nUnesite datum leta koji zelite da otkazete: ")
    pasos = raw_input("\nUnesite vas broj pasosa: ")
    karta = findkarta(broj, datum, pasos)
    izbrisikartu(karta)

def zamenitekst():
    file = open('karte.txt', 'w')
    file.close()
    file = open('karte.txt', 'a')
    for karta in karte:
        string = ('|').join([karta['brojleta'], karta['polaziste'], karta['odrediste'], karta['polazak'],
                             karta['dolazak'], karta['prevoznik'], karta['dani'], karta['model'], karta['cena'],
                             karta['datum'], karta['ime'], karta['prezime'], karta['drzavljanstvo'],
                             karta['pasos'], karta['datumprodaje'], karta['prodavac'], karta['mesto']])
        file.write(string)
        file.write("\n")

def izvestaj():
    komanda = izvestajmenu()
    if komanda == '1':
        search('datumprodaje', None)
    if komanda == '2':
        search('datum', None)
    if komanda == '3':
        search('datumprodaje', 'prodavac')
    if komanda == '4':
        report('datumprodaje', None)
    if komanda == '5':
        report('datum', None)
    if komanda == '6':
        report('datumprodaje', 'prodavac')
    if komanda == '7':
        ukupno()

def izvestajmenu():
    print "\nIzaberite opciju: "
    print "\n 1 - pretraga karata na osnovu datuma prodaje"
    print " 2 - pretraga karata na osnovu datuma poletanja"
    print " 3 - pretraga datuma na osnovu datuma prodaje i prodavca"
    print " 4 - izvestaj o ukupnom broju i ceni prodatih karata za zadati datum prodaje"
    print " 5 - izvestaj o ukupnom broju i ceni prodatih karata za zadati datum poletanja"
    print " 6 - izvestaj o ukupnom broju i ceni prodatih karata za zadati datum prodaje i prodavca"
    print " 7 - izvestaj o ukupnom broju i ceni prodatih karata za prethodnih 30 dana, po prodavcima"
    komanda = raw_input(">> ")
    return komanda


def search(field1, field2):
    result = []
    if field1 == 'datum':
        print "format datuma: dd-mm-yyyy"
    else:
        print "format datuma: yyyy-mm-dd"
    vrednost1 = raw_input("Unesite vrednost po kojoj pretrazujete: ")
    if field2 != None:
        vrednost2 = raw_input("Unesite ime prodavca po kome pretrazujete: ")
        for karta in karte:
            if karta[field1] == vrednost1 and karta[field2] == vrednost2:
                result.append(karta)
    else:
        for karta in karte:
            if karta[field1] == vrednost1:
                result.append(karta)
    formatheader()
    formattickets(result)

def report(field1, field2):
    broj = 0
    cena = 0
    if field1 == 'datum':
        print "format datuma: dd-mm-yyyy"
    else:
        print "format datuma: yyyy-mm-dd"
    vrednost1 = raw_input("Unesite vrednost po kojoj pretrazujete: ")
    if field2 != None:
        vrednost2 = raw_input("Unesite ime prodavca po kome pretrazujete: ")
        for karta in karte:
            if karta[field1] == vrednost1 and karta[field2] == vrednost2:
                cena = cena + int(karta['cena'])
                broj += 1
    else:
        for karta in karte:
            if karta[field1] == vrednost1:
                cena = cena + int(karta['cena'])
                broj += 1
    print "\nBroj prodatih karata: ", broj
    print "\nUkupna cena prodatih karata: ", cena

def ukupno():
    result = []
    cena = 0
    prodato = 0
    danas = str(date.today())
    uslov = datetime.strptime(danas, '%Y-%m-%d') - timedelta(days=30)
    for karta in karte:
        if datetime.strptime(karta['datum'], '%d-%m-%Y') >= uslov:
            result.append(karta)
    for karta in result:
        cena = cena + int(karta['cena'])
        prodato = prodato + 1
    print "\nUkupna cena prodatih karata u prethodnih 30 dana:: ", cena
    print "\nUkupan broj prodatih karata u prethodnih 30 dana: ", prodato

def listasvih(brojleta):
    matrica = ""
    for karta in karte:
        if karta['brojleta'] == brojleta:
            matrica = karta['model']
    dim = matrica.split('/')
    kolone = []
    redovi = []
    sedista = []
    for red in range(int(dim[0]) + 1):
        if red != 0:
            redovi.append(red)
    for kolona in range(int(dim[1]) + 1):
        if kolona != 0:
            kolonastr = chr(kolona + 64)
            kolone.append(kolonastr)
    for red in redovi:
        for kolona in kolone:
            sediste = ('/').join([str(red),kolona])
            sedista.append(sediste)
    return sedista

def listazauzetih(brojleta, datum):
    sedista = []
    for karta in karte:
        if karta['brojleta'] == brojleta and karta['datum'] == datum:
            sedista.append(karta['mesto'])
    return sedista

def listaslobodnih(brojleta, datum):
    slobodna = listasvih(brojleta)
    zauzeta = listazauzetih(brojleta, datum)
    for i in zauzeta:
        slobodna.remove(i)
    return slobodna

karte = []
loadkarte()