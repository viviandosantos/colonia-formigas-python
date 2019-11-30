from formiga import Formiga
from trilha import Trilha
import random

def menorCaminho(atual, novo):
    distanciaAtual = 0 
    distanciaNovo = 0 
    retorno = atual

    distanciaAtual = sum(a.Distancia for a in atual)
    distanciaNovo = sum(n.Distancia for n in novo)

    if distanciaNovo < distanciaAtual or distanciaAtual == 0:
        retorno = novo.copy()
    return retorno

MAXDIAS, MAXHORARIOS, MAXPROF, MAXDISC, MAXLABS = 6, 2, 2, 4, 3
QTFORMIGAS, QTPONTOS, QTITERACOES = MAXPROF, 17, 300

trilha = Trilha()
trilha.start(MAXDIAS, MAXHORARIOS, MAXPROF, MAXDISC, MAXLABS, QTPONTOS)

#set ponto inicial de cada formiga
formigas = []
pontosIniciais = list(range(MAXPROF))

for i in range(QTFORMIGAS):
    ponto = random.choice(pontosIniciais)
    index = pontosIniciais.index(ponto)
    pontosIniciais.pop(index)

    formiga = Formiga(i + 1, trilha.Prof[ponto + 1], trilha.Arestas)
    formigas.append(formiga)

trilha.setFormigas(formigas)

menor = []
print("Rodando iterações...")
for n in range(QTITERACOES):
    menor.clear()
    print("Iteração", n+1, end=' ')
    for f in trilha.Formigas:
        trilha.antWalk()
        caminho = f.andar()
        f.printTourAtual()
        menor = menorCaminho(menor, f.TourIteracao[-1])
    trilha.atualizarFeromonioMenorCaminho(menor)

print("\nRelatório completo:")
for f in trilha.Formigas:
    print("\tTop %d melhores soluções:" % 10)
    f.solucoes(10)
    print("\n\tMelhor solução:")
    f.melhorSolucao()
