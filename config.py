# Configurações do trabalho.
# Para trocar de tema, altere TEMA, BASE_DE_DADOS, TECNICAS e TAREFAS.

import os

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_ARTIGOS = os.path.join(PASTA_PROJETO, "artigos")
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "saida")
ARQUIVO_GABARITO = os.path.join(PASTA_PROJETO, "avaliacao", "gabarito.json")
ARQUIVO_ONTOLOGIA = os.path.join(PASTA_PROJETO, "ontologia", "artigo_cientifico.ttl")

TEMA = "Processamento de Linguagem Natural"
BASE_DE_DADOS = "IEEE Xplore"
NAMESPACE = "http://www.din.uem.br/iia/artigo#"

# quantidade de termos no ranking de cada artigo
QTD_TERMOS = 10

# palavra inicial da árvore de palavras
RAIZ_ARVORE = "language"

# Se o ano de algum artigo for detectado errado, corrija aqui.
# Exemplo: {"artigo.pdf": 2019}
ANOS_CORRIGIDOS = {}

# Palavras comuns em qualquer artigo científico. Elas são removidas junto com
# as stopwords do NLTK, porque não dizem nada sobre o assunto do artigo.
STOPWORDS_EXTRAS = [
    "able", "according", "across", "additionally", "al", "along", "also", "although",
    "among", "annual", "another", "appendix", "approach", "around", "association", "based",
    "best", "better", "can", "case", "conference", "consider", "considered", "could",
    "describe", "described", "different", "due", "e.g", "each", "eq", "equation", "et",
    "etc", "even", "every", "example", "fig", "figure", "figures", "finally", "find",
    "first", "follow", "following", "follows", "found", "furthermore", "general", "give",
    "given", "good", "high", "higher", "however", "i.e", "important", "include",
    "included", "includes", "including", "instead", "large", "larger", "least", "less",
    "let", "like", "linguistics", "low", "lower", "made", "make", "many", "may", "meeting",
    "might", "moreover", "much", "need", "number", "obtain", "obtained", "often", "one",
    "overall", "page", "pages", "paper", "papers", "particular", "per", "possible", "pp",
    "present", "presented", "proc", "proceedings", "propose", "proposed", "rather",
    "respectively", "result", "results", "second", "section", "sections", "see", "set",
    "sets", "several", "show", "shown", "shows", "similar", "since", "small", "smaller",
    "specific", "still", "table", "tables", "take", "third", "three", "thus", "toward",
    "towards", "two", "upon", "us", "use", "used", "uses", "using", "various", "via",
    "vol", "way", "well", "whether", "within", "without", "work", "would",
]

# Técnicas procuradas nos artigos. Cada uma tem uma expressão regular com as
# formas como ela costuma aparecer no texto (em minúsculas).
TECNICAS = {
    "Redes neurais": r"neural networks?|neural models?",
    "Deep learning": r"deep learning|deep neural",
    "Transformer / atenção": r"transformers?\b|self-attention|attention mechanism",
    "BERT / modelos pré-treinados": r"\bbert\b|scibert|roberta|pre-?trained (language )?models?",
    "LSTM / RNN": r"\blstm\b|recurrent neural|\brnns?\b|\bgru\b",
    "CNN": r"\bcnns?\b|convolutional",
    "Word embeddings": r"word embeddings?|word2vec|glove|embeddings?",
    "Modelo de linguagem": r"language models?",
    "LLM / GPT": r"\bgpt-?\d?\b|large language models?|\bllms?\b",
    "SVM": r"\bsvms?\b|support vector",
    "CRF": r"\bcrfs?\b|conditional random fields?",
    "HMM": r"\bhmms?\b|hidden markov",
    "Máxima entropia / regressão logística": r"maximum entropy|maxent|logistic regression|log-linear",
    "Perceptron": r"perceptron",
    "Naive Bayes": r"naive bayes",
    "Árvore de decisão / random forest": r"decision trees?|random forests?",
    "Métodos de kernel": r"\bkernels?\b",
    "Algoritmo EM": r"expectation[- ]maximi[sz]ation|\bem algorithm",
    "Programação dinâmica / Viterbi": r"dynamic programming|viterbi|\bcky\b",
    "Beam search": r"beam search",
    "Gradiente estocástico": r"stochastic gradient|\bsgd\b|stochastic learning",
    "Regularização": r"regulari[sz]ation|\bl1\b|\bl2\b",
    "Agrupamento (clustering)": r"clustering|clusters?\b",
    "Modelos de tópicos / LDA": r"topic models?|latent dirichlet|\blda\b",
    "TF-IDF / bag-of-words": r"tf-?idf|bag[- ]of[- ]words",
    "N-gramas": r"n-grams?|bigrams?|trigrams?|unigrams?",
    "Similaridade de cosseno / espaço vetorial": r"cosine|vector space|distributional",
    "Aprendizado supervisionado": r"\bsupervised",
    "Aprendizado não supervisionado": r"unsupervised|semi-supervised|self-supervised|weak(ly)? supervis",
    "Fine-tuning / transfer learning": r"fine-?tun|transfer learning",
    "Anotação manual / crowdsourcing": r"crowdsourc|mechanical turk|annotators?",
    "Questionário / entrevista / estudo com usuários": r"\bsurveys?\b|interviews?|user stud|usability study|questionnaires?",
}

# Tarefas de PLN mencionadas (aparecem num gráfico separado das técnicas)
TAREFAS = {
    "Análise sintática (parsing)": r"\bparsing\b|\bparsers?\b|parse trees?|dependency pars",
    "Análise semântica / papéis semânticos": r"semantic pars|semantic role",
    "Etiquetagem morfossintática (POS)": r"part-of-speech|\bpos tag",
    "Reconhecimento de entidades (NER)": r"named entit|\bner\b|entity extraction",
    "Extração de informação / relações": r"information extraction|relation extraction|open ie\b",
    "Tradução automática": r"machine translation|\bsmt\b|\bnmt\b",
    "Sumarização": r"summari[sz]ation",
    "Classificação de textos": r"text classification|document classification|topic classification",
    "Análise de sentimentos": r"sentiment",
    "Perguntas e respostas": r"question answering|\bqa\b",
    "Recuperação de informação / busca": r"information retrieval|search engines?|academic search",
    "Recomendação": r"recommendation|recommender",
    "Geração de texto / paráfrase": r"text generation|generation of|paraphras",
    "Reconhecimento de fala": r"speech recognition|\basr\b",
    "Grafos de conhecimento / ontologias": r"knowledge graphs?|knowledge bases?|ontolog",
    "Análise de citações": r"citation (graph|prediction|analysis|network|context)",
}
