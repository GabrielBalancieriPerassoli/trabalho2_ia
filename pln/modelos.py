# Etapa 1 - modelos de representação do texto:
#   bag-of-words, n-gramas, TF-IDF com similaridade de cosseno e um modelo de
#   linguagem de bigramas com suavização de Laplace.
# Tudo foi implementado com dicionários e Counter, sem scikit-learn.

import math
import re
from collections import Counter, defaultdict

from pln import preprocessamento


def bag_of_words(lemas):
    return Counter(lemas)


def ngramas(palavras, n):
    return [tuple(palavras[i:i + n]) for i in range(len(palavras) - n + 1)]


def ngramas_da_sentenca(sentenca, n):
    """N-gramas formados só por palavras que estão juntas no texto original.

    Exemplo: em "extraction from the web", "from" e "the" são stopwords, então
    o bigrama ("extraction", "web") NÃO é gerado. Assim os n-gramas ficam
    parecidos com expressões de verdade, como "language model".
    """
    tokens = preprocessamento.tokenizar(preprocessamento.limpar_texto(sentenca))
    trechos = []
    trecho_atual = []
    for token in tokens:
        if token in preprocessamento.STOPWORDS:
            if trecho_atual:
                trechos.append(trecho_atual)
            trecho_atual = []
        else:
            trecho_atual.append(preprocessamento.lematizar(token))
    if trecho_atual:
        trechos.append(trecho_atual)

    resultado = []
    for trecho in trechos:
        resultado += ngramas(trecho, n)
    return resultado


def contar_ngramas(sentencas, n):
    contagem = Counter()
    for sentenca in sentencas:
        contagem.update(ngramas_da_sentenca(sentenca, n))
    return contagem


def termos_mais_frequentes(contagem, quantidade=10):
    """Agrupa os lemas pelo radical (stemming) e soma as frequências.

    Assim "extraction", "extract" e "extractive" contam como um termo só.
    O nome mostrado é o lema mais frequente do grupo.
    Devolve uma lista de (termo, frequência, radical, {lema: frequência}).
    """
    grupos = defaultdict(Counter)
    for lema, frequencia in contagem.items():
        grupos[preprocessamento.radical(lema)][lema] += frequencia

    ranking = []
    for radical, lemas in grupos.items():
        termo = lemas.most_common(1)[0][0]
        ranking.append((termo, sum(lemas.values()), radical, dict(lemas)))
    ranking.sort(key=lambda item: item[1], reverse=True)
    return ranking[:quantidade]


def contar_mencoes(texto, dicionario):
    """Conta quantas vezes cada técnica (ou tarefa) do dicionário aparece no texto."""
    texto = texto.lower()
    return {nome: len(re.findall(padrao, texto)) for nome, padrao in dicionario.items()}


# TF-IDF e similaridade entre artigos

def calcular_idf(lista_bag_of_words):
    total_documentos = len(lista_bag_of_words)
    documentos_com_termo = Counter()
    for bag in lista_bag_of_words:
        documentos_com_termo.update(bag.keys())
    # idf suavizado: evita divisão por zero e valores negativos
    return {termo: math.log((1 + total_documentos) / (1 + qtd)) + 1
            for termo, qtd in documentos_com_termo.items()}


def calcular_tfidf(bag, idf):
    total = sum(bag.values()) or 1
    return {termo: (frequencia / total) * idf.get(termo, 0) for termo, frequencia in bag.items()}


def cosseno(vetor1, vetor2):
    produto = sum(vetor1[t] * vetor2[t] for t in set(vetor1) & set(vetor2))
    norma1 = math.sqrt(sum(v * v for v in vetor1.values()))
    norma2 = math.sqrt(sum(v * v for v in vetor2.values()))
    if norma1 == 0 or norma2 == 0:
        return 0.0
    return produto / (norma1 * norma2)


def matriz_similaridade(lista_bag_of_words):
    idf = calcular_idf(lista_bag_of_words)
    vetores = [calcular_tfidf(bag, idf) for bag in lista_bag_of_words]
    n = len(vetores)
    matriz = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matriz[i][j] = matriz[j][i] = cosseno(vetores[i], vetores[j])
    return matriz, vetores


def palavras_chave(vetor_tfidf, quantidade=8):
    ordenado = sorted(vetor_tfidf.items(), key=lambda item: item[1], reverse=True)
    return [termo for termo, _ in ordenado[:quantidade]]


# Modelo de linguagem de bigramas

class ModeloBigramas:
    """P(w2 | w1) = (contagem(w1 w2) + 1) / (contagem(w1) + tamanho do vocabulário)"""

    def __init__(self):
        self.unigramas = Counter()
        self.bigramas = Counter()

    def treinar(self, sentencas):
        """sentencas: lista de listas de palavras."""
        for palavras in sentencas:
            sequencia = ["<s>"] + palavras + ["</s>"]  # marcadores de início e fim
            self.unigramas.update(sequencia)
            self.bigramas.update(ngramas(sequencia, 2))
        return self

    def probabilidade(self, w1, w2):
        vocabulario = len(self.unigramas)
        return (self.bigramas[(w1, w2)] + 1) / (self.unigramas[w1] + vocabulario)

    def perplexidade(self, sentencas):
        soma_log = 0.0
        quantidade = 0
        for palavras in sentencas:
            sequencia = ["<s>"] + palavras + ["</s>"]
            for w1, w2 in ngramas(sequencia, 2):
                soma_log += math.log(self.probabilidade(w1, w2))
                quantidade += 1
        if quantidade == 0:
            return float("inf")
        return math.exp(-soma_log / quantidade)
