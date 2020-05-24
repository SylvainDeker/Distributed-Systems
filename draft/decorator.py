import time

def controler_temps(nb_secs):

    def decorateur(fonction_a_executer):

        def fonction_modifiee():

            tps_avant = time.time() # Avant d'exécuter la fonction
            valeur_renvoyee = fonction_a_executer() # On exécute la fonction
            tps_apres = time.time()
            tps_execution = tps_apres - tps_avant
            if tps_execution >= nb_secs:
                print("La fonction {0} a mis {1} pour s'exécuter".format( \
                        fonction_a_executer, tps_execution))
            return valeur_renvoyee
        return fonction_modifiee
    return decorateur

@controler_temps(1)
def fonction():
    for i in range(10):
        time.sleep(0.1)


if __name__ == '__main__':
    fonction()
