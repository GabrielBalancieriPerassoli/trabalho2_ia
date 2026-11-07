# Etapa 2 - extração de objetivo, problema, método, contribuições e trabalhos futuros.
#
# Como funciona:
#   1. Cada frase do artigo recebe uma pontuação para cada elemento.
#      - gatilho forte encontrado: +3 pontos  (ex.: "the goal of this paper")
#      - gatilho fraco encontrado: +1 ponto   (ex.: "we propose")
#      - bônus ou desconto pela seção onde a frase está
#      - descontos para frases que enganam (legenda de tabela, frase curta etc.)
#   2. A frase vai para o elemento em que passou do limite mínimo com mais folga.
#   3. Para cada elemento ficam as frases com mais pontos.
#
# Objetivo x contribuição: o objetivo é o que o artigo pretende fazer; a
# contribuição é o que ele entrega para a área. Se a frase passou no limite de
# contribuição, ela é contribuição e não pode ser objetivo.

import re

from pln.secoes import dividir_sentencas

ELEMENTOS = ["objetivo", "problema", "metodo", "contribuicao", "trabalho_futuro"]

PESO_FORTE = 3
PESO_FRACO = 1

GATILHOS = {
    "objetivo": {
        "fortes": [
            r"\b(the|our|main|primary|overall) (\w+ )?(goal|aim|objective|purpose)s? (of (this|the|our) (paper|work|study|article|research)|is|was|here)\b",
            r"\b(this|the present|our) (position )?(paper|article|work|study|research) (aims?|seeks?|intends?|attempts?|tries) to\b",
            r"\bwe (aim|seek|intend|set out|attempt) to\b",
            r"\b(in|with) this (position )?(paper|article|work|study)\b",
            r"\b(this|the|our) (position )?(paper|article|work|study) (presents?|proposes?|introduces?|describes?|investigates?|explores?|addresses|examines?|studies|focuses|reports?|discusses|shows?|demonstrates?|argues?)\b",
            r"^(here,? |in short,? )?we (propose|present|introduce|describe|investigate|explore|address|examine|study|tackle|focus|argue|ask)\b",
        ],
        "fracos": [
            r"\bwe (propose|present|introduce|describe|investigate|explore|address|examine|study|argue|ask)\b",
            r"^to (improve|address|overcome|move towards|bridge|facilitate|enable|solve|better)\b",
        ],
    },
    "problema": {
        "fortes": [
            r"\b(difficult|difficulty|challenging|expensive|costly|time-consuming|labor-intensive|tedious|infeasible|unfeasible|impractical|prohibitive|unrealistic|insufficient|understudied|underexplored|unexplored|limits|limited|lacks?|lacking|unable|fails?|failed|suffers?|struggles?|problematic|rife|incoherent|uninformative|misled|overfitting|acute|noisy|sparse|scarce|bottleneck|demanding|unwieldy)\b",
            r"^(however|unfortunately|yet|nevertheless|despite|although|while|but)\b",
        ],
        "fracos": [
            r"\b(however|but|unfortunately)\b",
            r"\b(problems?|challenges?|issues?|limitations?|drawbacks?|shortcomings?|gaps?|barriers?)\b",
            r"\b(not well|little attention|few (solutions|studies|works)|has not been|have not been|no way|cannot|can not|remains? (unclear|open|unsolved|difficult|challenging)|do not|does not|did not)\b",
            r"\b(existing|current|previous|prior|standard|recent) (\w+ ){0,2}(methods?|approaches|systems?|models?|work|tools|corpora|datasets?|resources|setups|practices)\b",
        ],
    },
    "metodo": {
        "fortes": [
            r"\bwe (\w+ )?(use|used|employ|employed|apply|applied|adopt|adopted|train|trained|leverage|utili[sz]e|conduct|conducted|perform|performed|implement|implemented|build|built|combine|extend|extended|augment|deploy|evaluate|test|reduce|aggregate|formulate|sketch|characterize|revert|assess|model|compute)\b",
            r"\b(our|the proposed|this|the) (\w+ )?(method|approach|model|system|framework|algorithm|technique|architecture|pipeline|idea) (is|uses|consists|relies|combines|works|learns|incorporates|integrates|applies|ranks|maps|generates|implements)\b",
            r"\bwe (propose|present|introduce|develop|describe)\w* (a|an|the) (\w+ ){0,5}(method|approach|model|framework|algorithm|technique|system|parser|tool|toolkit|interface|learning)\b",
        ],
        "fracos": [
            r"\b(based on|by means of|using|through|via|by (comparing|training|combining|integrating|augmenting|pretraining|learning|adding))\b",
            r"\b(interviews?|surveys?|questionnaires?|case stud(y|ies)|content analysis|user stud(y|ies)|usability study|observational study|experiments?|annotation stud(y|ies)|human evaluation|simulations?)\b",
            r"\b(parser|kernel|features?|regulari[sz]ation|crfs?|svms?|hmms?|transformer|neural|statistical|supervised|unsupervised|pipeline|stochastic|corpus|corpora|n-gram|language models?|constraints?)\b",
        ],
    },
    "contribuicao": {
        "fortes": [
            r"\bcontribut(e|es|ed|ing|ion|ions)\b",
            r"\b(to (the best of )?our knowledge|we are the first|is the first|are the first|first (work|study|attempt|approach|dataset|system) to)\b",
            r"\b(fills? (an|the|a) (\w+ )?gap|advances? the state of the art)\b",
        ],
        "fracos": [
            r"\b(our|the|main|key|primary|major|additional) (\w+ )?contributions?\b",
        ],
    },
    "trabalho_futuro": {
        "fortes": [
            r"\bfuture (work|research|directions?|studies|investigations?|step|systems|efforts)\b",
            r"\bin (the )?future\b",
            r"\bwe (also )?(plan|intend|hope|would like|aim|are excited) to\b",
            r"\bwe are (also )?(currently )?(investigating|exploring|working on|extending)\b",
            r"\b(remains?|left|leave) (\w+ )?(open|for future|as future|to future)\b",
            r"\b(next steps?|could be extended|can be extended|promising (direction|avenue)|worth exploring|interesting (direction|avenue|area|potential)|another (item|area|direction)|would be interesting|research directions?|yet another area)\b",
        ],
        "fracos": [
            r"\b(further|additional) (\w+ ){0,4}(work|research|investigation|studies|experiments|improvements?|advances)\b",
        ],
    },
}

# (padrão, pontos descontados, elementos afetados)
DESCONTOS = [
    (r"\b(organized as follows|rest of (the|this) paper|remainder of (the|this) paper)\b", 6, ELEMENTOS),
    (r"^(figure|fig\.|table)\s*\d", 6, ELEMENTOS),
    (r"equal contribution|author contributions|contributions? of (each|individual) authors?", 15, ["contribuicao"]),
    (r"\b(can|could|may|might|which|that|they) (also )?contribut", 6, ["contribuicao"]),  # "contribute to" = causar
    (r"\b(in this paper|we (present|propose|introduce|describe|motivate))\b", 2, ["problema"]),
    (r"\bto (address|solve|overcome|tackle) (this|these|the|such)\b", 3, ["problema"]),
    (r"\b(our|we)\b.*\b(outperforms?|improves?|achieves?|reduces? error)", 2, ["problema"]),
    (r"\b(help|facilitate|enable|encourage|foster)\w* (further|future)\b", 4, ["trabalho_futuro"]),
]

# Bônus (positivo) ou desconto (negativo) pela seção onde a frase está.
# Seções que não aparecem valem 0.
BONUS_POR_SECAO = {
    "objetivo": {"resumo": 1, "introducao": 1, "trabalhos_relacionados": -3,
                 "metodologia": -2, "resultados": -2, "outra": -2},
    "problema": {"resumo": 1, "introducao": 1, "trabalhos_relacionados": -1, "conclusao": -2,
                 "metodologia": -2, "resultados": -2, "outra": -2},
    "metodo": {"resumo": 1, "introducao": 1, "metodologia": -1, "trabalhos_relacionados": -3,
               "resultados": -2, "outra": -2},
    "contribuicao": {"introducao": 1, "conclusao": 1, "trabalhos_relacionados": -5,
                     "metodologia": -3, "resultados": -3, "outra": -3},
    "trabalho_futuro": {"conclusao": 2, "resumo": -3, "introducao": -3, "trabalhos_relacionados": -3,
                        "metodologia": -2, "outra": -1},
}

# pontuação mínima e quantidade máxima de frases de cada elemento
LIMITE_MINIMO = {"objetivo": 3, "problema": 4, "metodo": 3, "contribuicao": 4, "trabalho_futuro": 3}
MAXIMO_DE_FRASES = {"objetivo": 2, "problema": 2, "metodo": 3, "contribuicao": 5, "trabalho_futuro": 4}

SECOES_ANALISADAS = {"resumo", "introducao", "metodologia", "resultados", "conclusao",
                     "trabalhos_relacionados", "outra"}

# frase que anuncia uma lista de contribuições ("Our contributions are as follows:")
ABRE_LISTA_DE_CONTRIBUICOES = re.compile(
    r"contributions?\s+(of\s+(this|the|our)\s+(paper|work)\s+)?(are|include|is)|"
    r"(paper|work|study)\s+contributes|following contributions|paper's contributions",
    re.IGNORECASE)
ITEM_DE_LISTA = re.compile(r"^(•|-|\(?\d{1,2}\)|\(?[ivx]{1,4}\)|\d\.\s|first,|second,|third,|finally,)",
                           re.IGNORECASE)


def separar_frases(secoes):
    """Lista as frases das seções analisadas, guardando de qual seção vieram."""
    tem_resumo = any(s["tipo"] == "resumo" for s in secoes)
    frases = []
    for secao in secoes:
        tipo = secao["tipo"]
        if tipo == "inicio":
            # artigos sem a palavra "Abstract" (formato ACM): o resumo fica no começo
            if tem_resumo:
                continue
            tipo = "resumo"
        if tipo not in SECOES_ANALISADAS:
            continue
        for texto in dividir_sentencas(secao["texto"]):
            frases.append({"texto": texto, "secao": tipo, "titulo_secao": secao["titulo"]})
    return frases


def parece_lixo(frase):
    """Pedaços de tabela ou figura têm muitos números e símbolos."""
    palavras = frase.split()
    simbolos = sum(1 for c in frase if not (c.isalpha() or c.isspace()))
    estranhas = sum(1 for p in palavras if re.search(r"\d|[^\w\s.,;:()'\"-]", p))
    return simbolos > 0.25 * len(frase) or estranhas > 0.2 * len(palavras)


def pontuar(frase, elemento):
    texto = frase["texto"].lower()
    pontos = 0
    for gatilho in GATILHOS[elemento]["fortes"]:
        if re.search(gatilho, texto):
            pontos += PESO_FORTE
    for gatilho in GATILHOS[elemento]["fracos"]:
        if re.search(gatilho, texto):
            pontos += PESO_FRACO
    if pontos == 0:
        return 0  # sem nenhum gatilho a frase não interessa

    for padrao, desconto, afetados in DESCONTOS:
        if elemento in afetados and re.search(padrao, texto):
            pontos -= desconto

    pontos += BONUS_POR_SECAO[elemento].get(frase["secao"], 0)
    if elemento == "trabalho_futuro" and "future" in frase["titulo_secao"].lower():
        pontos += 2

    quantidade_palavras = len(frase["texto"].split())
    if quantidade_palavras < 6:
        pontos -= 3
    elif quantidade_palavras > 90:
        pontos -= 2
    if parece_lixo(frase["texto"]):
        pontos -= 3
    return pontos


def marcar_listas_de_contribuicoes(frases, pontuacoes):
    """Os itens que vêm logo depois de "our contributions are:" também são contribuições."""
    for i, frase in enumerate(frases):
        texto = frase["texto"].rstrip()
        if not ABRE_LISTA_DE_CONTRIBUICOES.search(texto):
            continue
        if not (texto.endswith(":") or re.search(r":\s*\(?1\)|:\s*•", texto)):
            continue
        # a frase que só abre a lista ("The contributions are as follows:") não conta
        if texto.endswith(":") and len(texto.split()) < 12:
            pontuacoes[i]["contribuicao"] = 0
        for j in range(i + 1, min(i + 8, len(frases))):
            if frases[j]["secao"] != frase["secao"]:
                break
            if ITEM_DE_LISTA.match(frases[j]["texto"].strip()):
                pontuacoes[j]["contribuicao"] = max(pontuacoes[j]["contribuicao"], 0) + 6
                pontuacoes[j]["objetivo"] -= 3


def escolher_elemento(pontos):
    """Devolve o elemento da frase ou None se ela não passou em nenhum limite."""
    if pontos["contribuicao"] >= LIMITE_MINIMO["contribuicao"]:
        return "contribuicao"
    escolhido = None
    maior_folga = -1
    for elemento in ELEMENTOS:
        folga = pontos[elemento] - LIMITE_MINIMO[elemento]
        if folga >= 0 and folga > maior_folga:
            escolhido = elemento
            maior_folga = folga
    return escolhido


def extrair_elementos(secoes):
    frases = separar_frases(secoes)
    pontuacoes = [{elemento: pontuar(frase, elemento) for elemento in ELEMENTOS} for frase in frases]
    marcar_listas_de_contribuicoes(frases, pontuacoes)

    candidatas = {elemento: [] for elemento in ELEMENTOS}
    for i, pontos in enumerate(pontuacoes):
        elemento = escolher_elemento(pontos)
        if elemento:
            candidatas[elemento].append(i)

    resultado = {}
    for elemento in ELEMENTOS:
        melhores = sorted(candidatas[elemento], key=lambda i: pontuacoes[i][elemento], reverse=True)
        melhores = sorted(melhores[:MAXIMO_DE_FRASES[elemento]])  # volta para a ordem do texto
        resultado[elemento] = [{
            "texto": frases[i]["texto"].lstrip("• ").strip(),
            "secao": frases[i]["secao"],
            "pontuacao": pontuacoes[i][elemento],
        } for i in melhores]
    return resultado
