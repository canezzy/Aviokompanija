import dates

def loadletovi():
    for line in open('letovi.txt', 'r'):
        if len(line) > 1:
            let = str2let(line)
            letovi.append(let)

def str2let(line):
    if line[-1] == '\n':
        line = line[:-1]
    brojleta, polaziste, odrediste, polazak, dolazak, prevoznik, dani, model, cena = line.split('|')
    let = {
        'brojleta': brojleta,
        'polaziste': polaziste,
        'odrediste': odrediste,
        'polazak': polazak,
        'dolazak': dolazak,
        'prevoznik': prevoznik,
        'dani': dani,
        'model': model,
        'cena': cena
    }
    return let

def pretraga():
    pretragamenu()
    komanda = raw_input(">> ")
    while komanda.upper() not in ('1', '2', '3', '4', '5', '6', '7', 'X'):
        print "\nUneli ste pogresnu komandu.\n"
        pretragamenu()
        komanda = raw_input(">> ")
    while komanda.upper() != 'X':
        if komanda.upper() == '1':
            search('polaziste', None)
        elif komanda.upper() == '2':
            search('odrediste', None)
        elif komanda.upper() == '3':
            searchdani('polazak', None)
        elif komanda.upper() == '4':
            searchdani('dolazak', None)
        elif komanda.upper() == '5':
            search('polazak', None)
        elif komanda.upper() == '6':
            search('dolazak', None)
        elif komanda.upper() == '7':
            search('prevoznik', None)
    print "\nDovidjenja."

def pretragamenu():
    print "\nIzaberite kriterijum po kom pretrazujete letove:"
    print "  1 - polaziste"
    print "  2 - odrediste"
    print "  3 - datum polaska aviona"
    print "  4 - datum dolaska aviona"
    print "  5 - vreme poletanja aviona"
    print "  6 - vreme sletanja aviona"
    print "  7 - prevoznik"
    print "  x - izlaz iz programa"
    print "\n"

def search(field, value):
    result = []
    if value is None:
        value = raw_input("\nUnesite vrednost po kojoj vrsite pretragu (x za povratak nazad): ")
    if value.upper() == 'X':
        pretraga()
    for let in letovi:
        if let[field].upper() == value.upper():
            result.append(let)
    if result != []:
        formatheader()
        formatletovi(result)
    else:
        print "\nNe postoji ni jedan let koji odgovara vasoj pretrazi!"
        pretraga()

def searchdani(field, value):
    dan = dates.obradadatuma(value)
    result = []
    for let in letovi:
        days = let['dani'].split(',')
        if field == 'polazak':
            for day in days:
                if day == dan:
                    result.append(let)
        if field == 'dolazak':
            if let['polazak'] > let['dolazak']:
                for day in days:
                    if sledecidan(day) == dan:
                        result.append(let)
            elif let['polazak'] < let['dolazak']:
                for day in days:
                    if day == dan:
                        result.append(let)
def sledecidan(dan):
    if dan == 'pon':
        day = 'uto'
    elif dan == 'uto':
        day = 'sre'
    elif dan == 'sre':
        day = 'cet'
    elif dan == 'cet':
        day = 'pet'
    elif dan == 'pet':
        day = 'sub'
    elif dan == 'sub':
        day = 'ned'
    elif dan == 'ned':
        day = 'pon'
    return day

def formatheader():
    print "\n\n"
    print \
        "Broj leta|Polazak|Polaziste|       Dani      |Odrediste|Dolazak| Model |   Prevoznik   |Cena\n" \
        "---------+-------+---------+-----------------+---------+-------+-------+---------------+----"

def formatletovi(result):
    for let in result:
        print u"{0:9}|{1:7}|{2:9}|{3:17}|{4:9}|{5:7}|{6:7}|{7:15}|{8:>4}".format(
            let['brojleta'],
            let['polazak'],
            let['polaziste'],
            let['dani'],
            let['odrediste'],
            let['dolazak'],
            let['model'],
            let['prevoznik'],
            let['cena'])


letovi = []
loadletovi()