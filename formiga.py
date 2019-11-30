import random
# -*- coding: utf-8 -*-
class Formiga(object):
    Descricoes = {
        #[Tipo] : {[Valor 1], [Valor 2], ..., [Valor N]}
        1: { 1: "Professor Piva", 2: "Professora Maria" }, #Professores
        2: { 1: "disciplina IA", 2: "disciplina SO", 3: "disciplina BD", 4:"disciplina ED" }, #Disciplinas
        3: { 1: "Segunda", 2: "Terça", 3: "Quarta", 4: "Quinta", 5: "Sexta", 6: "Sábado" }, #Dias
        4: { 1: "1° horário", 2: "2° horário" }, #Horarios
        5: { 1: "Laboratório 1", 2: "Laboratório 2", 3: "Laboratório 3"} #Laboratorios   
    }

    def __init__(self, idFormiga, pontoInicial, arestas):
        self.Tour = [] 
        self.Visitas = []
        self.TourIteracao = []
        self.VisitasIteracao = []
        self.DistanciasPercorridas = []

        self.IdFormiga = idFormiga
        self.PontoInicial = pontoInicial
        self.PontoAtual = pontoInicial
        self.Visitas.append(pontoInicial)
        self.DistanciaPercorrida = 0
        self.Arestas = arestas
    
    def start(self):
        #print("\tFormiga #%d andando a partir do ponto: %d-%d" % (self.IdFormiga, self.PontoAtual.Valor, self.PontoAtual.Tipo))
        caminhoEscolhido = self.escolherCaminho()
        self.caminharAteDestino(caminhoEscolhido)
        if 0 <= (len(self.Tour)) < 4 and self.PontoAtual.Tipo != 5:
            self.start()
        else:
            #print("\tFormiga #%d chegou ao ponto: %d-%d" % (self.IdFormiga, self.PontoAtual.Valor, self.PontoAtual.Tipo))
            self.reset()
    
    def andar(self):
        self.trilharCaminho()
        if 0 <= (len(self.Tour)) < 4 and self.PontoAtual.Tipo != 5:
            self.start()
        else:
            #print("\tFormiga #%d chegou ao ponto: %d-%d" % (self.IdFormiga, self.PontoAtual.Valor, self.PontoAtual.Tipo))
            self.reset()
    
    def caminharAteDestino(self, caminho):
        self.DistanciaPercorrida += caminho.Distancia
        self.Tour.append(caminho)
        self.PontoAtual = caminho.PontoDestino
        self.Visitas.append(self.PontoAtual)
    
    def trilharCaminho(self):
        caminho = self.escolherCaminho()
        self.DistanciaPercorrida += caminho.Distancia
        self.Tour.append(caminho)
        self.PontoAtual = caminho.PontoDestino
        self.Visitas.append(self.PontoAtual)

    def escolherCaminho(self):
        #calcular probabilidade de transição e escolher a maior
        escolhido = self.roleta()
        return escolhido

    def roleta(self):
        #todas as arestas onde o ponto origem é o ponto atual da formiga
        arestasTipo = list(filter(lambda x: x.PontoOrigem.Tipo == self.PontoAtual.Tipo and x.PontoOrigem.Valor == self.PontoAtual.Valor
                                    and x.PontoDestino != self.PontoAtual, self.Arestas))
        count = 0
        maxProb = sum(a.Probabilidade for a in arestasTipo)
        escolhida = arestasTipo[0]
        prob = random.uniform(0, maxProb)

        for a in arestasTipo:
            aux = count
            count += a.Probabilidade
            if aux < prob <= count:
                escolhida = a
        return escolhida

    def reset(self):
        self.DistanciasPercorridas.append(self.DistanciaPercorrida)
        self.DistanciaPercorrida = 0
        self.TourIteracao.append(self.Tour.copy())

        visitas = []
        for v in self.Visitas:
            visitas.append(v)
        self.VisitasIteracao.append(visitas)

        self.PontoAtual = self.PontoInicial
        self.Tour.clear()
        self.Visitas.clear()
        self.Visitas.append(self.PontoAtual)

    def atualizarArestas(self, novasArestas):
        self.Arestas = novasArestas.copy()

    #print de todas as tours de todas as iterações
    def print(self):
        print("\nFormiga #%d:\n\tDistancia percorrida: %.2f\n\tPonto Inicial:" % (self.IdFormiga, self.DistanciasPercorridas[-1]), end=' ')
        self.PontoInicial.printPonto()

        count = 1
        print("\tTour:")
        for tour in self.TourIteracao:
            print("\tNa iteração %02d: " % count)
            distancia = 0
            count += 1
            for a in tour:
                print("\t\tDe %s até %s. Distância: %.2f. Feromônio: %.2f. Probabilidade: %.2f%%" 
                % (self.Descricoes[a.PontoOrigem.Tipo][a.PontoOrigem.Valor], self.Descricoes[a.PontoDestino.Tipo][a.PontoDestino.Valor], a.Distancia, a.Feromonio, a.Probabilidade * 100.0))
                distancia += a.Distancia
            print("\t\tDistância percorrida: %.2f\n" % (distancia))
    
    #print apenas da última tour realizada até o momento da chamada da função 
    def printTourAtual(self):
        print("\n\tFormiga #%d:\n\t\tDistancia percorrida: %.2f\n\t\tPonto Inicial: %s" 
        % (self.IdFormiga, self.DistanciasPercorridas[-1], self.Descricoes[self.PontoInicial.Tipo][self.PontoInicial.Valor]))
        count = 1
        print("\t\tTour:")
        for tour in self.TourIteracao[-1]:
            distancia = 0
            print("\t\t\tDe %s até %s.\0Distância: %.2f. Feromônio: %.2f. Probabilidade: %.2f%%." 
            % (self.Descricoes[tour.PontoOrigem.Tipo][tour.PontoOrigem.Valor], self.Descricoes[tour.PontoDestino.Tipo][tour.PontoDestino.Valor], tour.Distancia, tour.Feromonio, tour.Probabilidade * 100.0), end=' ')
            distancia += tour.Distancia
            print("Distância percorrida: %.2f" % (distancia))

    def solucoes(self, top):       
        for visita in self.VisitasIteracao[-top:]:
            print("\t\t[", end='')
            for p in visita:
                print(" %s" % (self.Descricoes[p.Tipo][p.Valor]), end=' \0\t')
            print("\b]")

    def melhorSolucao(self):
        print("\t\t[", end='')
        for v in self.VisitasIteracao[-1]:
            print(" %s" % (self.Descricoes[v.Tipo][v.Valor]), end=' \0\t')
        print("\b]\n")

   def atualizarProbabilidadeTransicao(self):
        for i in range(4):
            self.probabilidade(i+1)


