# Etapa 1 - pré-processamento: limpeza, tokenização, stopwords, lematização e stemming.
#
# Do NLTK usamos só o que não é modelo treinado: a lista de stopwords, o
# lematizador do WordNet (consulta a um dicionário) e o stemmer de Porter
# (regras). A tokenização e a divisão em sentenças foram feitas com expressões
# regulares para não usar o "punkt", que é um modelo treinado.

import re

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

import config


def baixar_recursos_nltk():
    for nome, caminho in [("stopwords", "corpora/stopwords"), ("wordnet", "corpora/wordnet")]:
        try:
            nltk.data.find(caminho)
        except LookupError:
            print(f"Baixando o recurso '{nome}' do NLTK...")
            nltk.download(nome, quiet=True)


baixar_recursos_nltk()
from nltk.corpus import stopwords  # só pode ser importado depois do download

STOPWORDS = set(stopwords.words("english")) | set(config.STOPWORDS_EXTRAS)

lematizador = WordNetLemmatizer()
stemmer = PorterStemmer()
lemas_ja_calculados = {}


def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"https?://\S+|www\.\S+", " ", texto)          # links
    texto = re.sub(r"\S+@\S+", " ", texto)                        # e-mails
    texto = re.sub(r"\[[\d,\s\-]+\]", " ", texto)                 # citações [1], [2-4]
    texto = re.sub(r"\([^()]*?(19|20)\d\d[a-z]?\)", " ", texto)   # citações (Collins, 1997)
    texto = re.sub(r"\b[\w\-]*\d[\w\-]*\b", " ", texto)           # palavras com número
    texto = re.sub(r"[^a-z\-\s]", " ", texto)                     # pontuação e símbolos
    texto = re.sub(r"\s-+|-+\s", " ", texto)                      # hífens soltos
    return re.sub(r"\s+", " ", texto).strip()


def tokenizar(texto):
    # palavras com 3 letras ou mais (podem ter hífen: "state-of-the-art")
    return re.findall(r"[a-z][a-z\-]*[a-z]", texto)


def lematizar(palavra):
    """Tenta primeiro como substantivo ("studies" -> "study") e depois como verbo."""
    if palavra not in lemas_ja_calculados:
        lema = lematizador.lemmatize(palavra, "n")
        if lema == palavra:
            lema = lematizador.lemmatize(palavra, "v")
        lemas_ja_calculados[palavra] = lema
    return lemas_ja_calculados[palavra]


def radical(palavra):
    """Stemming de Porter: "extraction" e "extracting" viram "extract"."""
    return stemmer.stem(palavra)


def preprocessar(texto):
    """Devolve os lemas do texto, já sem stopwords."""
    lemas = []
    for token in tokenizar(limpar_texto(texto)):
        if token in STOPWORDS:
            continue
        lema = lematizar(token)
        if lema not in STOPWORDS and len(lema) >= 3:
            lemas.append(lema)
    return lemas
