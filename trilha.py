import random
import math
from ponto import Ponto
from aresta import Aresta

#-*- coding utf-8 -*-
class Trilha(object):
    def __init__(self):
        self.Dias = {}
        self.Horarios = {}
        self.Prof = {}
        self.Disc = {}
        self.Labs = {}
        self.Arestas = []
        self.DiscXProf = { 1: [1, 2], 2: [3, 4] }
        self.DiasXDisc = { 1: [1,2,5], 2: [1,2,3], 3: [3,5], 4: [4, 5, 6] }
        self.HorariosXDisc = { 1: 1, 2: 2, 3: 2, 4: 1 }

        self.RecursosXDisc = { 1: [3,4,5,6], 2: [1,2,3,0], 3: [2,4,0,0], 4: [1,2,5,0] }
        self.RecursosXLabs = { 1: [1, 2, 3, 4], 2: [3, 4, 5, 6], 3: [1, 2, 4, 6] }
       
    def start(self, maxDias, maxHorarios, maxProf, maxDisc, maxLabs, qtPontos):
        print("\nDefinindo pontos...")

        for i in range(maxProf):
            self.Prof[i + 1] = Ponto(i + 1, 1)
            
        for i in range(maxDisc):
            self.Disc[i + 1] = Ponto(i + 1, 2)

        for i in range(maxDias):
            self.Dias[i + 1] = Ponto(i + 1, 3)

        for i in range(maxHorarios):
            self.Horarios[i + 1] = Ponto(i + 1, 4)

        for i in range(maxLabs):
            self.Labs[i + 1] = Ponto(i + 1, 5)  

        self.setDistancias()
        print("Caminho definido. Calculando probabilidades...")
        for i in range(4):
            self.probabilidade(i+1)
        print("Probabilidades calculadas com sucesso!\n")

    def setFormigas(self, formigas):
        self.Formigas = formigas

    def DisciplinaPorProfessor(self, prof, disc):
        dist = 10
        if disc.Valor in self.DiscXProf[prof.Valor]:
            dist = 0.2
        return dist
    
    def DiasPorDisciplina(self, disc, dia):
        dist = 10
        if dia.Valor in self.DiasXDisc[disc.Valor]:
            dist = 0.5
        return dist

    def HorariosPorDisciplina(self, disc, horario, distanciaDia):
        dist = 10 
        if horario.Valor == self.HorariosXDisc[disc.Valor]:
            dist = distanciaDia * 2
        return dist
    
    def DiscplinaPorLaboratorio(self, disc, lab, distanciaHorario):
        dist = 1 / (len(set(self.RecursosXDisc[disc.Valor]).intersection(set(self.RecursosXLabs[lab.Valor])))  + 1) 
        dist += distanciaHorario
        return dist 

    def setDistancias(self):    
        ''' 
        saltos = 
            1: Prof -> Disc
            2: Disc -> Dia
            3: Dia -> Horario
            4: Horario -> Labs
        '''                
        for p in self.Prof:
            for dc in self.Disc:
                distancia = self.DisciplinaPorProfessor(self.Prof[p], self.Disc[dc])
                self.Arestas.append(Aresta(1, self.Prof[p], self.Disc[dc], distancia))
            
        for dc in self.Disc:
            for di in self.Dias:
                distDia = self.DiasPorDisciplina(self.Disc[dc], self.Dias[di])
                self.Arestas.append(Aresta(2, self.Disc[dc], self.Dias[di], distDia))

                for h in self.Horarios:
                    distHorario = self.HorariosPorDisciplina(self.Disc[dc], self.Horarios[h], distDia)
                    self.Arestas.append(Aresta(3, self.Dias[di], self.Horarios[h], distHorario))

                    for l in self.Labs:
                        distLab = self.DiscplinaPorLaboratorio(self.Disc[dc], self.Labs[l], distHorario)
                        self.Arestas.append(Aresta(4, self.Horarios[h], self.Labs[l], distLab))
                
    def probabilidade(self, tipo):        
        #encontrar as influencias de todas as arestas que tem o mesmo ponto inicial e somar#
        arestasTipo = list(filter(lambda x: x.Tipo == tipo, self.Arestas))
        for a in arestasTipo:
            arestasDoPontoInicial = list(filter(lambda x: x.PontoOrigem.Valor == a.PontoOrigem.Valor 
                                                and x.PontoOrigem.Tipo == a.PontoOrigem.Tipo, arestasTipo))
            totalInfluencia = 0
            totalInfluencia = sum(api.Influencia for api in arestasDoPontoInicial)
            a.Probabilidade = a.Influencia / totalInfluencia

            a.ProbabilidadeTransicao = (pow(a.Feromonio, a.Alpha) * pow((1/a.Distancia), a.Beta)) / (sum((pow(api.Feromonio, api.Alpha) * pow((1/api.Distancia), api.Beta)) for api in arestasDoPontoInicial))           
    
    #atualiza o feromonio de todas as arestas
    def atualizarFeromonio(self, formigas):
        for a in self.Arestas:
            aposEvaporar = a.evaporarFeromonio()
            somaFeromoniosVisitantes = 0
            #achar as formigas que passaram por aquela aresta
            visitantes = list(filter(lambda x: a in x.Tour, formigas))
            for v in visitantes:
                v.print()
                somaFeromoniosVisitantes += sum(a.AtualizacaoFeromonio / v.DistanciaPercorrida for a in v.Tour)
            a.Feromonio = aposEvaporar + somaFeromoniosVisitantes
            a.atualizarInfluencia()

    #atualiza o feromonio apenas das arestas de um único caminho (o com menor distancia)
    def atualizarFeromonioMenorCaminho(self, caminho):
        for aresta in self.Arestas:
            if aresta in caminho:
                aposEvaporar = aresta.evaporarFeromonio()
                somaFeromoniosVisitantes = 0
                #achar as formigas que passaram por aquela aresta
                visitantes = list(filter(lambda x: aresta in x.Tour, self.Formigas))
                for v in visitantes:
                    somaFeromoniosVisitantes += sum(c.AtualizacaoFeromonio / v.DistanciaPercorrida for c in v.Tour)
                aresta.Feromonio = aposEvaporar + somaFeromoniosVisitantes
                aresta.atualizarInfluencia()
                #aresta.print()
        for f in self.Formigas:
            f.atualizarArestas(self.Arestas)
            
    def atualizarProbabilidadeTransicao(self):
        for i in range(4):
            self.probabilidade(i+1)
