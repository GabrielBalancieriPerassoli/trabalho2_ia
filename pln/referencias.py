# Etapa 1 - extração das referências bibliográficas.
#
# Três formatos são reconhecidos:
#   IEEE (colchetes):  [1] A. Autor, "Título", ...
#   lista numerada:    1. Autor, A.: Título ...
#   autor-ano (ACL):   Autor, A. 2005. Título. ...

import re

ANO = r"(?:19|20)\d{2}[a-z]?"

# No formato autor-ano o ano vem logo depois dos autores: ". 2005. ", ", 2005. " ou " (2005). "
MARCADOR_DE_ANO = re.compile(r"[.,]\s+\(?(" + ANO + r")\)?[.,:]\s")

# palavras que terminam com ponto mas não encerram uma referência
NAO_TERMINA_REFERENCIA = {"al", "jr", "dr", "st", "mc", "proc", "procs", "vol", "no", "pp", "ed",
                          "eds", "univ", "dept", "conf", "int", "intl", "assoc", "comput", "ling"}


def extrair_referencias(texto):
    """Devolve (lista de referências, formato encontrado)."""
    if not texto or not texto.strip():
        return [], None
    linhas = [linha.strip() for linha in texto.split("\n") if linha.strip()]

    linhas_com_colchete = [linha for linha in linhas if re.match(r"^\[\d{1,3}\]", linha)]
    if len(linhas_com_colchete) >= 3:
        formato = "ieee"
        referencias = re.split(r"\s*(?=\[\d{1,3}\]\s)", " ".join(linhas))
    elif lista_numerada(linhas):
        formato = "numerada"
        referencias = re.split(r"\n(?=\d{1,3}\.\s+[A-Z])", "\n".join(linhas))
    else:
        formato = "autor-ano"
        referencias = separar_autor_ano(" ".join(linhas))

    resultado = []
    for referencia in referencias:
        referencia = re.sub(r"\s+", " ", referencia).strip()
        referencia = re.sub(r"^\[\d+\]\s*|^\d{1,3}\.\s+", "", referencia).strip(" ;")
        # descarta pedaços curtos que não são referência
        if len(referencia) <= 20:
            continue
        if not re.search(ANO, referencia) and len(referencia) <= 60:
            continue
        resultado.append(referencia[:600])  # uma referência normal não passa disso
    return resultado, formato


def lista_numerada(linhas):
    if not linhas or not re.match(r"^1\.\s+[A-Z]", linhas[0]):
        return False
    numeros = []
    for linha in linhas:
        encontrado = re.match(r"^(\d{1,3})\.\s+[A-Z]", linha)
        if encontrado:
            numeros.append(int(encontrado.group(1)))
    return numeros[:3] == [1, 2, 3]


def separar_autor_ano(texto):
    """Para cada ano encontrado depois de uma lista de autores, volta no texto
    até o ponto final da referência anterior. Esse é o começo da referência."""
    texto = re.sub(r"\s+", " ", texto)
    inicios = []
    for marcador in MARCADOR_DE_ANO.finditer(texto):
        inicio = inicio_da_referencia(texto, marcador.start())
        if inicios and inicio <= inicios[-1]:
            continue
        # se o "autor" começa com "In Proceedings", "pages"... o ano estava no
        # meio do nome do evento e não depois dos autores
        if re.match(r"(In |Proceedings|pages|Journal|arXiv|Vol|[a-z])", texto[inicio:inicio + 12]):
            continue
        if marcador.start() - inicio > 900:  # lista de autores grande demais: erro
            continue
        inicios.append(inicio)

    referencias = []
    for i, inicio in enumerate(inicios):
        fim = inicios[i + 1] if i + 1 < len(inicios) else len(texto)
        referencias.append(texto[inicio:fim])
    return referencias


def inicio_da_referencia(texto, posicao):
    """Volta a partir da posição até achar ". " que não seja de uma inicial
    (como em "J. Smith") nem de uma abreviação (como "et al.")."""
    i = posicao - 1
    while i > 0:
        if texto[i] == "." and i + 1 < len(texto) and texto[i + 1] == " ":
            palavra = palavra_antes_do_ponto(texto, i)
            inicial = (len(palavra) == 1 and palavra.isupper()) or re.fullmatch(r"([A-Z]\.)*[A-Z]|[A-Z]\.-[A-Z]", palavra)
            if not palavra or (not inicial and palavra.lower() not in NAO_TERMINA_REFERENCIA):
                return i + 2
        i -= 1
    return 0


def palavra_antes_do_ponto(texto, posicao_do_ponto):
    j = posicao_do_ponto - 1
    while j >= 0 and texto[j] != " ":
        j -= 1
    palavra = texto[j + 1:posicao_do_ponto].strip("()[],;")
    if not palavra:
        # caso "P . Pantel": o pypdf às vezes coloca espaço antes do ponto
        anteriores = texto[:posicao_do_ponto].split()
        palavra = anteriores[-1] if anteriores else ""
    return palavra


def ano_da_referencia(referencia):
    anos = re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", referencia)
    return int(anos[0]) if anos else None
