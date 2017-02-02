import users

def main():
    print "\n            AERODROM FTN"
    print "\n       ========================"
    while users.login() == False:                                                  #Pokrece program tako sto poziva funkciju
        print "\nUneli ste pogresno korisnicko ime i lozinku. Pokusajte ponovo."      #login sve dok se korisnik uspesno ne
        users.login()                                                                    #uloguje

if __name__ == "__main__":
    main()