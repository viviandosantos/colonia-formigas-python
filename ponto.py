#-*- coding utf-8 -*-
class Ponto(object):
    def __init__(self, valor, tipo):
        self.Valor = valor
        self.Tipo = tipo
        
    def printPonto(self):
        print("Valor: %d - tipo: %d" % (self.Valor, self.Tipo))