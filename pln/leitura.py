# Etapa 1 - leitura dos PDFs e limpeza do texto.
# O texto de cada página é extraído com o pypdf (sucessor do PyPDF2).
# O pdfplumber é usado só para achar o título, que é o texto com a maior fonte.

import logging
import os
import re
import unicodedata
from collections import Counter
from datetime import date

import pdfplumber
from pypdf import PdfReader

# esconde os avisos que as bibliotecas mostram em alguns PDFs
logging.getLogger("pypdf").setLevel(logging.ERROR)
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# linhas que aparecem nos PDFs do IEEE e da ACM e não fazem parte do texto
LINHAS_IGNORADAS = [
    r"authorized licensed use limited to",
    r"downloaded on .* from ieee xplore",
    r"restrictions apply",
    r"permission to make digital or hard copies",
    r"^\s*\d+\s*$",  # número de página
]

# caracteres que o PDF traz e que trocamos por versões simples
TROCAS_CARACTERES = {
    "“": '"', "”": '"',    # aspas curvas
    "‘": "'", "’": "'",    # apóstrofos curvos
    "–": "-", "—": " - ",  # travessões
    "−": "-",                   # sinal de menos
    "­": "",                    # hífen invisível
    " ": " ",                   # espaço não separável
    "•": " • ",            # marcador de lista (deixa espaço em volta)
}


def listar_pdfs(pasta):
    if not os.path.isdir(pasta):
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")
    arquivos = sorted(f for f in os.listdir(pasta) if f.lower().endswith(".pdf"))
    return [os.path.join(pasta, f) for f in arquivos]


def ler_paginas(caminho):
    leitor = PdfReader(caminho)
    paginas = []
    for pagina in leitor.pages:
        try:
            paginas.append(pagina.extract_text() or "")
        except Exception as erro:
            print(f"  aviso: não consegui ler uma página de {os.path.basename(caminho)} ({erro})")
            paginas.append("")

    metadados = {"titulo": "", "autores": "", "data": ""}
    if leitor.metadata:
        metadados["titulo"] = leitor.metadata.get("/Title") or ""
        metadados["autores"] = leitor.metadata.get("/Author") or ""
        metadados["data"] = str(leitor.metadata.get("/CreationDate") or "")
    return paginas, metadados


def normalizar_caracteres(texto):
    # NFKC separa as ligaduras ("ﬁ" vira "fi")
    texto = unicodedata.normalize("NFKC", texto)
    for antigo, novo in TROCAS_CARACTERES.items():
        texto = texto.replace(antigo, novo)
    texto = re.sub(r"[\x00-\x08\x0b-\x1f]", " ", texto)  # caracteres de controle
    return texto


def remover_cabecalho_rodape(paginas):
    """Remove as linhas que se repetem em metade ou mais das páginas."""
    if len(paginas) < 3:
        return paginas

    def chave(linha):
        # troca números por # para "Page 1" e "Page 2" contarem como a mesma linha
        return re.sub(r"\d+", "#", linha.strip().lower())

    repeticoes = Counter()
    for pagina in paginas:
        linhas_da_pagina = {chave(linha) for linha in pagina.split("\n") if linha.strip()}
        repeticoes.update(linhas_da_pagina)

    limite = max(3, len(paginas) // 2)
    repetidas = {linha for linha, qtd in repeticoes.items() if qtd >= limite and len(linha) < 120}

    paginas_limpas = []
    for pagina in paginas:
        linhas = []
        for linha in pagina.split("\n"):
            if chave(linha) in repetidas:
                continue
            if any(re.search(padrao, linha, re.IGNORECASE) for padrao in LINHAS_IGNORADAS):
                continue
            linhas.append(linha.rstrip())
        paginas_limpas.append("\n".join(linhas))
    return paginas_limpas


def juntar_palavras_hifenizadas(texto):
    """Junta palavras quebradas no fim da linha ("seman-\\ntic" vira "semantic").
    Se a palavra com hífen aparece mais vezes no texto (ex.: "state-of-the-art"),
    o hífen é mantido."""
    vocabulario = Counter(re.findall(r"[a-z][a-z\-]+", texto.lower()))

    def juntar(match):
        inicio, fim = match.group(1), match.group(2)
        sem_hifen = (inicio + fim).lower()
        com_hifen = (inicio + "-" + fim).lower()
        if vocabulario[com_hifen] > vocabulario[sem_hifen]:
            return inicio + "-" + fim
        return inicio + fim

    return re.sub(r"([A-Za-z]+)-[ \t]*\n[ \t]*([a-z][A-Za-z]*)", juntar, texto)


def juntar_versalete(texto):
    """Nomes em versalete saem separados do PDF ("R EVERB", "S CISSOR").
    Junta a letra solta com o resto. "A" e "I" ficam de fora porque são palavras."""
    return re.sub(r"\b([B-HJ-Z]) ([A-Z]{2,})\b", r"\1\2", texto)


def encontrar_ano(primeira_pagina, metadados):
    ano_atual = date.today().year
    padrao_ano = r"(?<!\d)(19[5-9]\d|20\d\d)(?!\d)"
    linhas = [l for l in primeira_pagina.split("\n")
              if not re.search(r"authorized licensed|downloaded on", l, re.IGNORECASE)]

    # 1) linhas de copyright, nome do evento ou arXiv costumam ter o ano certo
    anos = []
    for linha in linhas:
        if re.search(r"©|\(c\)|copyright|proceedings|conference|arxiv|journal|ieee|acm", linha, re.IGNORECASE):
            anos += [int(a) for a in re.findall(padrao_ano, linha)]
    anos = [a for a in anos if a <= ano_atual]
    if anos:
        return max(anos)

    # 2) senão, o maior ano da primeira página (as citações são sempre mais antigas)
    anos = [int(a) for a in re.findall(padrao_ano, "\n".join(linhas))]
    anos = [a for a in anos if a <= ano_atual]
    if anos:
        return max(anos)

    # 3) por último, a data de criação do PDF
    encontrado = re.search(r"(19|20)\d\d", metadados["data"])
    return int(encontrado.group(0)) if encontrado else None


def titulo_valido(titulo):
    if not titulo or len(titulo) < 12 or len(titulo) > 300 or len(titulo.split()) < 3:
        return False
    palavras_ruins = ["untitled", "microsoft word", ".dvi", ".pdf", ".doc", "latex",
                      "proceedings", "conference"]
    return not any(p in titulo.lower() for p in palavras_ruins)


def titulo_pela_fonte(caminho):
    """Pega as palavras da primeira página escritas com a maior fonte."""
    with pdfplumber.open(caminho) as pdf:
        palavras = pdf.pages[0].extract_words(extra_attrs=["size"], x_tolerance=1.5)
    palavras = [p for p in palavras if p.get("upright", True)]  # ignora texto girado
    if not palavras:
        return ""

    # maior tamanho de fonte usado em pelo menos 2 palavras (evita letra capitular)
    tamanhos = Counter(round(p["size"], 1) for p in palavras)
    candidatos = [tamanho for tamanho, qtd in tamanhos.items() if qtd >= 2]
    if not candidatos:
        return ""
    maior = max(candidatos)

    # linhas do título = linhas onde aparece a fonte maior. Usamos a base da letra
    # ("bottom") porque no versalete as letras têm alturas diferentes.
    bases = [p["bottom"] for p in palavras if round(p["size"], 1) >= maior - 0.3]
    do_titulo = [p for p in palavras
                 if p["size"] >= 0.6 * maior and any(abs(p["bottom"] - b) < 2 for b in bases)]
    # numera as linhas de cima para baixo e ordena da esquerda para a direita
    do_titulo.sort(key=lambda p: p["bottom"])
    numero_linha, base_anterior = 0, None
    for palavra in do_titulo:
        if base_anterior is not None and palavra["bottom"] - base_anterior > 3:
            numero_linha += 1
        palavra["linha"] = numero_linha
        base_anterior = palavra["bottom"]
    do_titulo.sort(key=lambda p: (p["linha"], p["x0"]))

    titulo = ""
    anterior = None
    for palavra in do_titulo:
        mesma_linha = anterior is not None and palavra["linha"] == anterior["linha"]
        if mesma_linha and palavra["x0"] - anterior["x1"] < 1:
            titulo += palavra["text"]  # pedaço da mesma palavra (troca de fonte no meio)
        else:
            titulo += " " + palavra["text"]
        anterior = palavra
    return re.sub(r"\s+", " ", normalizar_caracteres(titulo)).strip()


def encontrar_titulo(caminho, metadados):
    titulo = re.sub(r"\s+", " ", normalizar_caracteres(metadados["titulo"])).strip()
    if titulo_valido(titulo):
        return titulo
    try:
        titulo = titulo_pela_fonte(caminho)
        if titulo_valido(titulo) and len(titulo.split()) <= 30:
            return titulo
    except Exception as erro:
        print(f"  aviso: pdfplumber falhou em {os.path.basename(caminho)} ({erro})")
    return os.path.splitext(os.path.basename(caminho))[0]


def ler_artigo(caminho, anos_corrigidos=None):
    """Lê o PDF e devolve o texto limpo com título, ano e outras informações."""
    nome = os.path.basename(caminho)
    paginas, metadados = ler_paginas(caminho)
    paginas = [normalizar_caracteres(p) for p in paginas]

    if anos_corrigidos and nome in anos_corrigidos:
        ano = anos_corrigidos[nome]
    else:
        ano = encontrar_ano(paginas[0] if paginas else "", metadados)

    paginas = remover_cabecalho_rodape(paginas)
    texto = "\n".join(paginas)
    texto = juntar_palavras_hifenizadas(texto)
    texto = juntar_versalete(texto)
    texto = re.sub(r"[ \t]+", " ", texto)

    return {
        "arquivo": nome,
        "titulo": encontrar_titulo(caminho, metadados),
        "ano": ano,
        "autores": metadados["autores"],
        "num_paginas": len(paginas),
        "texto": texto,
    }
