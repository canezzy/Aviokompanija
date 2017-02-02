import flights
import tickets

def loadUsers():                                                     #Ucitava red po red iz fajla
    for line in open('korisnici.txt', 'r'):
        if len(line) > 1:
            user = str2user(line)
            korisnici.append(user)

def str2user(line):                                                  #Pretvara red iz fajla u recnik
    if line[-1] == '\n':
        line = line[:-1]
    username, password, ime, prezime, uloga = line.split('|')
    user = {
        'username': username,
        'password': password,
        'ime': ime,
        'prezime': prezime,
        'uloga': uloga
    }
    return user


def login():                                                        #Login funkcija
    username = raw_input("\nUnesite vase korisnicko ime: ")
    password = raw_input("Unesite vasu lozinku: ")
    print "\n"
    for user in korisnici:
        if user['username'] == username and user['password'] == password:
            if user['uloga'] == 'menadzer':
                menadzermenu()
            elif user['uloga'] == 'prodavac':
                prodavacmenu()
            return True
    return False


def menadzermenu():
    printmenadzermenu()
    komanda = raw_input(">>> ")
    while komanda.upper() not in ('1', '2', 'X'):
        print "\nUneli ste pogresnu komandu.\n"
        menadzermenu()
    if komanda.upper() != 'X':
        if komanda.upper() == '1':
            flights.pretraga()
        elif komanda.upper() == '2':
            tickets.izvestaj()
        menadzermenu()
    print "\n\n\n\nDovidjenja."


def prodavacmenu():
    printprodavacmenu()
    komanda = raw_input(">>> ")
    while komanda.upper() not in ('1', '2', '3', '4', 'X'):
        print "\nUneli ste pogresnu komandu.\n"
        prodavacmenu()
    while komanda.upper() != 'X':
        if komanda.upper() == '1':
            flights.pretraga()
        elif komanda.upper() == '2':
            tickets.unos()
        elif komanda.upper() == '3':
            tickets.izmena()
        elif komanda.upper() == '4':
            tickets.obrisi()
    print "\n\n\n\nDovidjenja."


def printmenadzermenu():
    print "\nIzaberite opciju:"
    print "  1 - pretraga letova"
    print "  2 - izvestavanje o prodatim kartama"
    print "  x - izlaz iz programa"
    print "\n"


def printprodavacmenu():
    print "\nIzaberite opciju:"

    print "  1 - pretraga letova"
    print "  2 - unos novih avionskih karata"
    print "  3 - izmena postojecih karata"
    print "  4 - brisanje postojecih karata"
    print "  x - izlaz iz programa"
    print "\n"

korisnici = []
loadUsers()


