from random import uniform
from time import sleep
from threading import Thread, Lock
import numpy as np

class Filosofo(Thread):
    execute = False  # Inicializado como False

    def __init__(self, nome, garfo_esquerda, garfo_direita):
        Thread.__init__(self)
        self.nome = nome
        self.garfo_esquerda = garfo_esquerda
        self.garfo_direita = garfo_direita

    def run(self):
        while self.execute:
            print(f"\n {self.nome} está pensando")
            sleep(uniform(5, 15))
            self.comer()

    def comer(self):
        garfo1, garfo2 = self.garfo_esquerda, self.garfo_direita

        while self.execute:
            garfo1.acquire()
            locked = garfo2.acquire(True) # indica que a tentativa de adquirir o garfo 2 e bloqueante, ou seja, ela espera até o semaforo estar disponivel
            if locked:
                print(f"\n {self.nome} começou a comer")
                sleep(uniform(5, 10))
                print(f"\n {self.nome} parou de comer")
                pratos[nomes.index(self.nome)] += 1
                print(pratos)
                garfo2.release()
                garfo1.release()
                break
            else:
                garfo1.release()
                sleep(uniform(2, 5))  # Adicione um pequeno atraso para evitar bloqueio contínuo

n_filosofos = int(input("Digite o número de filósofos: "))
nomes = [input(f"Digite o nome do filósofo {i+1}: ") for i in range(n_filosofos)]
pratos = np.zeros(shape=n_filosofos)
garfos = [Lock() for _ in range(n_filosofos)]

mesa = [Filosofo(nomes[i], garfos[i], garfos[(i + 1) % n_filosofos]) for i in range(n_filosofos)]

for i in range(20):
    Filosofo.execute = True
    threads = []
    for filosofo in mesa:
        thread = Thread(target=filosofo.run)
        thread.start()
        threads.append(thread)
        sleep(2)
    sleep(uniform(5, 15))
    Filosofo.execute = False
    for thread in threads:
        thread.join()
