# Etapa 1 - divisão do artigo em seções e do texto em sentenças.

import re

# Palavras que indicam o tipo de cada seção. A ordem importa: "Conclusions and
# Future Work" tem que ser classificada como conclusão antes de qualquer outra.
TIPOS_DE_SECAO = [
    ("resumo", r"^abstract"),
    ("referencias", r"^(references?|bibliography|literature cited|referências)$"),
    ("agradecimentos", r"acknowledg"),
    ("apendice", r"appendix|supplementa"),
    ("palavras_chave", r"^(keywords?|index terms|ccs concepts|acm reference format)"),
    ("conclusao", r"conclu|future work|final remarks|summary and|closing remarks|limitations"),
    ("introducao", r"introduc|motivation"),
    ("trabalhos_relacionados", r"related|background|literature|previous work|prior work|state of the art"),
    ("resultados", r"experiment|evaluation|result|analysis|performance|simulation|discussion|case stud|comparison|error"),
    ("metodologia", r"method|approach|model|framework|propos|system|architecture|algorithm|design|material|"
                    r"data|corpus|setup|implementation|task|overview|formulation|definition|learning|"
                    r"training|annotation|pipeline"),
]

# títulos que aparecem sozinhos na linha, sem número
TITULOS_SEM_NUMERO = re.compile(
    r"^(abstract|introduction|related work|background|methods?|methodology|materials and methods|"
    r"results|discussion|conclusions?|conclusions? and future work|acknowledg(e)?ments?|"
    r"references|bibliography|appendix|keywords|index terms|ccs concepts|limitations|"
    r"ethics statement|ethical considerations)\s*:?$",
    re.IGNORECASE,
)

TITULO_NUMERADO = re.compile(r"^(\d{1,2})\.?\s+([A-Z][^\n]{1,80})$")      # "1 Introduction"
TITULO_ROMANO = re.compile(r"^([IVX]{1,4})\.\s+([A-Z][^\n]{1,80})$")      # "I. INTRODUCTION" (IEEE)
TITULO_REFERENCIAS = re.compile(r"^((\d{1,2}|[IVX]{1,4})\.?\s+)?(references|bibliography|referências)\s*$",
                                re.IGNORECASE)

ROMANOS = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8,
           "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15}


def tipo_da_secao(titulo):
    titulo = titulo.lower().strip()
    titulo = re.sub(r"^(\d+(\.\d+)*\.?|[ivx]+\.)\s+", "", titulo)  # tira a numeração
    for tipo, padrao in TIPOS_DE_SECAO:
        if re.search(padrao, titulo):
            return tipo
    return "outra"


def parece_titulo(texto):
    """Filtro para não confundir uma linha comum (ou de tabela) com título de seção."""
    texto = texto.strip()
    palavras = texto.split()
    if len(texto) < 3 or len(palavras) > 10:
        return False
    if texto.endswith((",", ";")) or texto.count(".") > 1:
        return False
    letras = sum(c.isalpha() for c in texto)
    if letras < 0.6 * len(texto.replace(" ", "")):
        return False
    # muitas palavras em minúsculo indicam uma frase normal
    minusculas = sum(p[0].islower() for p in palavras)
    if len(palavras) >= 7 and minusculas > 0.6 * len(palavras):
        return False
    return True


def titulo_de_apendice(linha, linhas_na_secao):
    """Depois das referências, os apêndices aparecem como "A Background" ou "Appendix A"."""
    if linhas_na_secao < 10:
        return False
    if re.match(r"^(appendix\b|supplementary material)", linha, re.IGNORECASE):
        return True
    encontrado = re.match(r"^[A-H](\.\d)?\s+([A-Z][A-Za-z\-]+(\s+\S+){0,7})$", linha)
    return bool(encontrado) and parece_titulo(encontrado.group(2)) and not linha.endswith(".")


def dividir_secoes(texto):
    """Percorre as linhas procurando títulos de seção.

    Para não pegar linhas de tabela ou listas numeradas, só aceitamos títulos
    numerados em sequência (1, 2, 3... ou I, II, III...). Antes do resumo só
    aceitamos a Introdução, senão um endereço como "1 University Station" vira seção.
    """
    secoes = []
    atual = {"titulo": "Início", "tipo": "inicio", "linhas": []}
    ultimo_numero = 0
    estilo = None  # "arabico" ou "romano", decidido pelo primeiro título encontrado

    for linha in texto.split("\n"):
        linha_limpa = linha.strip()
        novo_titulo = None
        resto_da_linha = ""

        numerado = TITULO_NUMERADO.match(linha_limpa)
        romano = TITULO_ROMANO.match(linha_limpa)
        resumo_na_linha = re.match(r"^abstract\s*([-:.]\s*|\s+)(.+)$", linha_limpa, re.IGNORECASE)
        palavras_chave = re.match(r"^(index terms|keywords?|ccs concepts|additional key words)[^:\-]{0,20}[-:]",
                                  linha_limpa, re.IGNORECASE)

        if TITULO_REFERENCIAS.match(linha_limpa):
            novo_titulo = linha_limpa

        elif atual["tipo"] == "referencias" and titulo_de_apendice(linha_limpa, len(atual["linhas"])):
            novo_titulo = "Appendix: " + linha_limpa

        elif numerado and estilo != "romano" and parece_titulo(numerado.group(2)):
            numero = int(numerado.group(1))
            # aceita pular um número, porque às vezes o pypdf perde um título
            if ultimo_numero < numero <= ultimo_numero + 2:
                if atual["tipo"] != "inicio" or tipo_da_secao(linha_limpa) == "introducao":
                    novo_titulo, ultimo_numero, estilo = linha_limpa, numero, "arabico"

        elif romano and estilo != "arabico" and romano.group(1) in ROMANOS and parece_titulo(romano.group(2)):
            numero = ROMANOS[romano.group(1)]
            if ultimo_numero < numero <= ultimo_numero + 2:
                if atual["tipo"] != "inicio" or tipo_da_secao(linha_limpa) == "introducao":
                    novo_titulo, ultimo_numero, estilo = linha_limpa, numero, "romano"

        elif TITULOS_SEM_NUMERO.match(linha_limpa):
            novo_titulo = linha_limpa

        elif resumo_na_linha and atual["tipo"] == "inicio":
            # formato IEEE: "Abstract—This paper ..." na mesma linha
            novo_titulo, resto_da_linha = "Abstract", resumo_na_linha.group(2)

        elif palavras_chave:
            novo_titulo = "Keywords"
            resto_da_linha = linha_limpa[palavras_chave.end():].strip()

        if novo_titulo:
            secoes.append(atual)
            atual = {"titulo": novo_titulo, "tipo": tipo_da_secao(novo_titulo), "linhas": []}
            if resto_da_linha:
                atual["linhas"].append(resto_da_linha)
        else:
            atual["linhas"].append(linha)
    secoes.append(atual)

    resultado = []
    for secao in secoes:
        corpo = "\n".join(secao["linhas"]).strip()
        if corpo or secao["tipo"] == "referencias":
            resultado.append({"titulo": secao["titulo"], "tipo": secao["tipo"], "texto": corpo})

    # artigo sem "Conclusion": a última seção ("Discussion") faz esse papel
    if not any(s["tipo"] == "conclusao" for s in resultado):
        conteudo = [s for s in resultado if s["tipo"] not in ("referencias", "agradecimentos", "apendice")]
        if conteudo and re.search(r"discussion|summary|remarks", conteudo[-1]["titulo"], re.IGNORECASE):
            conteudo[-1]["tipo"] = "conclusao"
    return resultado


def separar_referencias(secoes):
    """Devolve (seções do corpo, texto das referências).
    O corpo é tudo o que vem antes das referências, sem os agradecimentos."""
    posicao = None
    for i, secao in enumerate(secoes):
        if secao["tipo"] == "referencias":
            posicao = i
    if posicao is None:
        return secoes, ""
    corpo = [s for s in secoes[:posicao] if s["tipo"] != "agradecimentos"]
    return corpo, secoes[posicao]["texto"]


# abreviações cujo ponto não termina a frase
ABREVIACOES = [
    "et al.", "e.g.", "i.e.", "vs.", "Fig.", "Figs.", "fig.", "Eq.", "Eqs.", "eq.",
    "Sec.", "Sect.", "Tab.", "No.", "no.", "Dr.", "Mr.", "Ms.", "Prof.", "approx.",
    "cf.", "resp.", "Vol.", "vol.", "pp.", "Ref.", "Refs.", "Inc.", "Corp.", "Ltd.",
    "U.S.", "Jr.", "St.", "Ch.", "Def.", "Thm.", "Alg.",
]


def texto_corrido(texto):
    """Junta as linhas do PDF num texto só."""
    texto = re.sub(r"\s*\n\s*", " ", texto)
    return re.sub(r"\s{2,}", " ", texto).strip()


def dividir_sentencas(texto):
    texto = texto_corrido(texto)
    if not texto:
        return []

    # número de nota de rodapé colado no ponto: "community.4 In future work"
    texto = re.sub(r"([a-z]\.)\d{1,2}\s+(?=[A-Z])", r"\1 ", texto)

    # troca temporariamente os pontos que não terminam frase por <P>
    for abreviacao in ABREVIACOES:
        texto = re.sub(r"(?<![A-Za-z])" + re.escape(abreviacao), abreviacao.replace(".", "<P>"), texto)
    texto = re.sub(r"\b([A-Z])\.(?=\s?[A-Z])", r"\1<P>", texto)  # iniciais: "J. Smith"
    texto = re.sub(r"(\d)\.(\d)", r"\1<P>\2", texto)              # números: "3.5"

    # quebra depois de . ! ? quando a próxima frase começa com maiúscula,
    # aspas, parêntese, marcador de lista ou número de subseção ("8.5 Future")
    partes = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(\[•]|\d+<P>\d+\s+[A-Z])|\s+(?=•\s)", texto)

    sentencas = []
    for parte in partes:
        parte = parte.replace("<P>", ".").strip()
        if len(parte) > 1:
            sentencas.append(parte)
    return sentencas
