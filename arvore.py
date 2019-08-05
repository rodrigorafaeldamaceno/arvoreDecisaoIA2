import numpy as np
from math import log2
import sys


def lerArray():
    data = []
    arquivo = open(sys.argv[1], 'r')

    arq = arquivo.read()
    linhas = arq.split('\n')
    #colunas = len(linhas[0].split(' '))

    #print('Linhas: ', len(linhas), 'Atributos: ', colunas)
    for i in range(len(linhas)):
        data.append(linhas[i].split(' '))

    # print(data)
    '''
    if(sys.argv[1] == 'no3.txt'):
        data = np.array(data).reshape(7, 5)
    elif(sys.argv[1] == 'vote.txt'):
        data = np.array(data).reshape(409, 4)
    elif(sys.argv[1] == 'contact-lenses.txt'):
        data = np.array(data).reshape(25, 4)
    '''
    arquivo.close()
    return data


def arraysDeSaida(arg):
    data = []
    arquivo = open(sys.argv[arg], 'r')

    arq = arquivo.read()
    linhas = arq.split('\n')
    # print(linhas)
    for i in range(len(linhas)-1):
        data.append(linhas[i].split(' '))

    # print(data)

    arquivo.close()
    return data


def lerArraySaida(data, coluna):
    qtdColunas = np.shape(data)[1]
    qtdLinhas = np.shape(data)[0]-1

    arq_0 = open(sys.argv[2], 'w')
    arq_1 = open(sys.argv[3], 'w')

    j = 0

    for i in range(qtdLinhas):

        if(data[i+1][coluna] == '1'):
            for j in range(qtdColunas):
                arq_1.write(data[i+1][j])
                if j < qtdColunas-1:
                    arq_1.write(' ')

            arq_1.write('\n')

        else:
            for j in range(qtdColunas):
                arq_0.write(data[i+1][j])
                if j < qtdColunas-1:
                    arq_0.write(' ')

            arq_0.write('\n')

    arq_1.close()
    arq_0.close()


def erroClassificacao(data, classe):
    qtdLinhas = np.shape(data)[0]

    negativos = 0
    positivos = 0

    # print(classe)

    for i in range(qtdLinhas):
        if(data[i][classe] == '0' or data[i][classe] == '1'):
            if(data[i][classe] == '0'):
                negativos += 1
            else:
                positivos += 1

    total = negativos+positivos
    erro = 1 - max((positivos/(total)),
                   (negativos/(total)))
    return erro


def gini_criterion(data, classe):
    positivos = 0
    negativos = 0
    qtdLinhas = np.shape(data)[0]

    for i in range(qtdLinhas):
        if(data[i][classe] == '0' or data[i][classe] == '1'):
            if(data[i][classe] == '0'):
                negativos += 1
            else:
                positivos += 1

    total = positivos + negativos

    gini = 1 - ((positivos/(total)) ** 2) - ((negativos/(total)) ** 2)

    return gini


def entropy(data, classe):
    positivos = 0
    negativos = 0

    qtdLinhas = np.shape(data)[0]
    for i in range(qtdLinhas):
        if(data[i][classe] == '0' or data[i][classe] == '1'):
            if(data[i][classe] == '0'):
                negativos += 1
            else:
                positivos += 1

    total = positivos + negativos

    positivos += 0.000001
    negativos += 0.000001

    entropy = -(positivos/(total) * log2(positivos/(total)) -
                negativos/(total) * log2(negativos/(total)))
    return abs(entropy)


def infoGain(impPai, impEsq, impDir, total, qtdEsq, qtdDir):

    infoGain = impPai - ((qtdEsq * impEsq) + (qtdDir * impDir))/total
    return abs(infoGain)


def parte1():
    dataSet = lerArray()

    '''dataSet = [
        ['febre', 'enjoo', 'manchas', 'dores', 'diagnostico'],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0]]
    '''

    atributo = sys.argv[4]
    impureza = sys.argv[5]

    # print(dataSet)

    qtdColunas = np.shape(dataSet)[1]
    qtdLinhas = np.shape(dataSet)[0]

    print(qtdLinhas, qtdColunas)

    for i in range(qtdColunas):
        if dataSet[0][i] == atributo:
            coluna = i

    lerArraySaida(dataSet, coluna)
    no6 = arraysDeSaida(2)
    no7 = arraysDeSaida(3)

    if (impureza == '1'):
        imp = erroClassificacao
    elif(impureza == '2'):
        imp = gini_criterion
    elif(impureza == '3'):
        imp = entropy
    else:
        print('Impureza invalida')

    impNo3 = imp(dataSet, qtdColunas-1)
    impNo6 = imp(no6, qtdColunas-1)
    impNo7 = imp(no7, qtdColunas-1)

    lin6 = np.shape(no6)[0]
    lin7 = np.shape(no7)[0]

    ganho = infoGain(impNo3, impNo6, impNo7, lin6+lin7, lin6, lin7)

    print('Impureza em ', sys.argv[1], ': ', round(impNo3, 3),
          '\nImpureza em ', sys.argv[2], ': ', round(impNo6, 3),
          '\nImpureza em ', sys.argv[3], ': ', round(impNo7, 3),
          '\nGanho: ', round(ganho, 3)
          )


def parte2():
    dataSet = lerArray()
    #atributo = sys.argv[4]
    qtdColunas = np.shape(dataSet)[1]
    qtdLinhas = np.shape(dataSet)[0]

    # Definindo como teste o primeiro atributo
    coluna = 0
    ganho = 0.0
    for i in range(qtdColunas-1):
        # carregando arquivos
        lerArraySaida(dataSet, coluna)
        filho1 = arraysDeSaida(2)
        filho2 = arraysDeSaida(3)

        # numero de instancias
        linFilho1 = np.shape(filho1)[0]
        linFilho2 = np.shape(filho2)[0]

        # impurezas
        impPai = gini_criterion(dataSet, qtdColunas-1)
        impFilho1 = gini_criterion(filho1, qtdColunas-1)
        impFilho2 = gini_criterion(filho2, qtdColunas-1)

        ganhoAtual = infoGain(impPai, impFilho1, impFilho2,
                              linFilho1+linFilho2, linFilho1, linFilho2)
        if (ganhoAtual > ganho):
            ganho = ganhoAtual
            coluna = i

    print("Atributo escolhido: ", coluna+1, '-', dataSet[0][coluna])

    print('Impureza em ', sys.argv[1], ': ', impPai,
          '\nImpureza em ', sys.argv[2], ': ', impFilho1,
          '\nImpureza em ', sys.argv[3], ': ', impFilho2,
          '\nGanho: ', round(ganho, 3)
          )


if __name__ == '__main__':

    parte1()
