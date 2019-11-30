#-*- coding utf-8 -*-
class Aresta(object):  
    def __init__(self, tipo, pontoOrigem, pontoDestino, distancia):
        self.Alpha = 1
        self.Beta = 1
        self.CoeficienteEvaporacao = 0.01
        self.ConstFeromonioInicial = 0.1
        self.FeromonioInicial = 0.1
        self.AtualizacaoFeromonio = 10

        self.PontoOrigem = pontoOrigem
        self.PontoDestino = pontoDestino
        self.Distancia = distancia
        self.Feromonio = self.ConstFeromonioInicial
        self.Tipo = tipo
        self.Influencia = pow((1/self.Distancia), self.Alpha) * pow(self.Feromonio, self.Beta)
        self.Probabilidade = 0 
        self.ProbabilidadeTransicao= 0.0
    
    def atualizarInfluencia(self):
        self.Influencia = pow((1/self.Distancia), self.Alpha) * pow(self.Feromonio, self.Beta)

    def evaporarFeromonio(self):
        self.FeromonioInicial = (1 - self.CoeficienteEvaporacao) * (1/self.Distancia)
        return self.FeromonioInicial                

    def print(self):
        print("Aresta: %d-%d -> %d-%d | Feromonio: %.2f | Influencia: %.2f | Probabilidade: %.2f" 
        % (self.PontoOrigem.Valor, self.PontoOrigem.Tipo, self.PontoDestino.Valor, self.PontoDestino.Tipo, self.Feromonio, self.Influencia, self.Probabilidade))