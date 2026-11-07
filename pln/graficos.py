# Visualizações pedidas nas observações do trabalho: termos mais citados, nuvem
# geral, técnicas mais mencionadas, evolução temporal e trabalhos futuros.
# Também geramos as sugeridas: mapa de calor, coocorrência, similaridade entre
# artigos e árvore de palavras.

import os
import random
from collections import Counter, defaultdict

import matplotlib

matplotlib.use("Agg")  # só salva os arquivos, não abre janela
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from wordcloud import WordCloud

from pln import modelos, preprocessamento

COR_FUNDO = "#ffffff"
COR_TEXTO = "#222222"
COR_TEXTO_CLARO = "#555555"
COR_GRADE = "#e6e6e6"
COR_PRINCIPAL = "#1d8279"   # verde-azulado
COR_SECUNDARIA = "#e07b39"  # laranja
COR_TERCEIRA = "#3d4a57"    # cinza-azulado
TONS = ["#d4ece9", "#a8d8d2", "#74beb6", "#3fa197", "#1d8279", "#10655e", "#0a4842"]
ESCALA = LinearSegmentedColormap.from_list("tons", ["#ffffff"] + TONS)
sorteio = random.Random(7)  # mesma nuvem toda vez que rodar

plt.rcParams.update({
    "figure.facecolor": COR_FUNDO,
    "axes.facecolor": COR_FUNDO,
    "savefig.facecolor": COR_FUNDO,
    "axes.edgecolor": "#cccccc",
    "axes.labelcolor": COR_TEXTO_CLARO,
    "xtick.color": COR_TEXTO_CLARO,
    "ytick.color": COR_TEXTO_CLARO,
    "text.color": COR_TEXTO,
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def nome_curto(artigo, tamanho=26):
    titulo = artigo["titulo"]
    if ":" in titulo[:30]:
        titulo = titulo.split(":")[0]
    if len(titulo) > tamanho:
        titulo = titulo[:tamanho].rsplit(" ", 1)[0] + "..."
    return f"{titulo} ({artigo['ano']})"


def salvar(figura, pasta, nome):
    caminho = os.path.join(pasta, nome)
    figura.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(figura)
    return caminho


def grafico_barras(nomes, valores, eixo_x, pasta, arquivo, cor=COR_PRINCIPAL, notas=None):
    altura = 0.38 * len(nomes) + 1.0
    figura, eixo = plt.subplots(figsize=(9, altura))
    posicoes = np.arange(len(nomes))[::-1]
    eixo.barh(posicoes, valores, color=cor, height=0.65)
    eixo.set_yticks(posicoes)
    eixo.set_yticklabels(nomes)
    eixo.set_xlabel(eixo_x)
    eixo.xaxis.grid(True, color=COR_GRADE)
    eixo.set_axisbelow(True)
    eixo.spines["left"].set_visible(False)
    eixo.tick_params(axis="y", length=0)

    maior = max(valores) if valores else 1
    for i, (y, valor) in enumerate(zip(posicoes, valores)):
        rotulo = str(valor) if not notas else f"{valor}  ({notas[i]})"
        eixo.text(valor + maior * 0.01, y, rotulo, va="center", fontsize=9, color=COR_TEXTO_CLARO)
    eixo.set_xlim(0, maior * 1.18)
    return salvar(figura, pasta, arquivo)


def cor_da_nuvem(*args, **kwargs):
    # sorteia um dos tons mais escuros para cada palavra
    return sorteio.choice(TONS[2:])


def nuvem_de_palavras(frequencias, pasta, arquivo):
    if not frequencias:
        return None
    nuvem = WordCloud(width=1400, height=750, background_color=COR_FUNDO, max_words=120,
                      color_func=cor_da_nuvem, prefer_horizontal=0.9, random_state=7)
    nuvem.generate_from_frequencies(dict(frequencias))
    figura, eixo = plt.subplots(figsize=(12, 6.5))
    eixo.imshow(nuvem, interpolation="bilinear")
    eixo.axis("off")
    return salvar(figura, pasta, arquivo)


def mapa_de_calor(matriz, linhas, colunas, legenda, pasta, arquivo, formato="{:.1f}", tamanho=None):
    matriz = np.array(matriz, dtype=float)
    tamanho = tamanho or (1.0 * len(colunas) + 3.5, 0.5 * len(linhas) + 2)
    figura, eixo = plt.subplots(figsize=tamanho)
    imagem = eixo.imshow(matriz, cmap=ESCALA, aspect="auto")
    eixo.set_xticks(range(len(colunas)))
    eixo.set_xticklabels(colunas, rotation=45, ha="right")
    eixo.set_yticks(range(len(linhas)))
    eixo.set_yticklabels(linhas)
    eixo.tick_params(length=0)
    for borda in eixo.spines.values():
        borda.set_visible(False)

    # escreve o valor em cada célula (branco nas células escuras)
    limite = matriz.max() * 0.55 if matriz.size else 0
    for i in range(len(linhas)):
        for j in range(len(colunas)):
            if matriz[i, j] != 0:
                cor = "white" if matriz[i, j] > limite else COR_TEXTO
                eixo.text(j, i, formato.format(matriz[i, j]), ha="center", va="center", fontsize=8, color=cor)

    barra = figura.colorbar(imagem, ax=eixo, fraction=0.03, pad=0.02)
    barra.set_label(legenda)
    barra.outline.set_visible(False)
    return salvar(figura, pasta, arquivo)


def grafo_coocorrencia(sentencas, frequencias, pasta, arquivo, qtd_termos=25, qtd_ligacoes=45):
    """Liga dois termos quando aparecem na mesma sentença."""
    termos = {termo for termo, _ in frequencias.most_common(qtd_termos)}
    pares = Counter()
    for sentenca in sentencas:
        presentes = sorted(set(preprocessamento.preprocessar(sentenca)) & termos)
        for i in range(len(presentes)):
            for j in range(i + 1, len(presentes)):
                pares[(presentes[i], presentes[j])] += 1
    if not pares:
        return None

    grafo = nx.Graph()
    for (termo1, termo2), quantidade in pares.most_common(qtd_ligacoes):
        grafo.add_edge(termo1, termo2, peso=quantidade)

    posicoes = nx.kamada_kawai_layout(grafo)
    maior_peso = max(d["peso"] for _, _, d in grafo.edges(data=True))
    maior_freq = max(frequencias[n] for n in grafo.nodes)

    figura, eixo = plt.subplots(figsize=(12, 9))
    larguras = [0.6 + 5 * grafo[a][b]["peso"] / maior_peso for a, b in grafo.edges]
    nx.draw_networkx_edges(grafo, posicoes, ax=eixo, width=larguras, edge_color=TONS[1])
    tamanhos = [80 + 900 * frequencias[n] / maior_freq for n in grafo.nodes]
    nx.draw_networkx_nodes(grafo, posicoes, ax=eixo, node_size=tamanhos, node_color=COR_PRINCIPAL)
    for termo, (x, y) in posicoes.items():
        eixo.annotate(termo, (x, y), xytext=(0, 13), textcoords="offset points", ha="center", fontsize=11,
                      bbox=dict(boxstyle="round,pad=0.2", fc=COR_FUNDO, ec="none", alpha=0.85))
    eixo.axis("off")
    eixo.margins(0.08)
    return salvar(figura, pasta, arquivo)


def arvore_de_palavras(sentencas, raiz, pasta, arquivo, ramos=5, sub_ramos=3):
    """Mostra as palavras que mais aparecem depois da raiz (bigramas) e, para
    cada uma, as que vêm depois do par (trigramas)."""
    bigramas, trigramas = Counter(), Counter()
    for sentenca in sentencas:
        palavras = preprocessamento.preprocessar(sentenca)
        bigramas.update(modelos.ngramas(palavras, 2))
        trigramas.update(modelos.ngramas(palavras, 3))

    seguintes = Counter({b: qtd for (a, b), qtd in bigramas.items() if a == raiz}).most_common(ramos)
    if not seguintes:
        return None

    filhos = {}
    for palavra, _ in seguintes:
        filhos[palavra] = Counter({c: qtd for (a, b, c), qtd in trigramas.items()
                                   if a == raiz and b == palavra}).most_common(sub_ramos)
    total_linhas = sum(max(1, len(f)) for f in filhos.values())

    figura, eixo = plt.subplots(figsize=(12, 7.5))
    eixo.axis("off")
    eixo.set_xlim(0, 3.3)
    eixo.set_ylim(-0.8, total_linhas)
    meio = (total_linhas - 1) / 2
    eixo.text(0.1, meio, raiz, fontsize=24, fontweight="bold", va="center")

    maior = seguintes[0][1]
    y = total_linhas - 1
    for palavra, quantidade in seguintes:
        n_filhos = max(1, len(filhos[palavra]))
        y_palavra = y - (n_filhos - 1) / 2
        eixo.plot([0.85, 1.2], [meio, y_palavra], color=TONS[1], linewidth=1 + 5 * quantidade / maior)
        eixo.text(1.23, y_palavra, palavra, fontsize=12 + 8 * quantidade / maior, color=COR_PRINCIPAL,
                  va="center", fontweight="bold")
        eixo.text(2.0, y_palavra, f"{quantidade}x", fontsize=9, color=COR_TEXTO_CLARO, va="center", ha="right")
        for k, (seguinte, qtd) in enumerate(filhos[palavra]):
            eixo.plot([2.08, 2.38], [y_palavra, y - k], color=COR_GRADE, linewidth=1.5)
            eixo.text(2.42, y - k, f"{seguinte}  ({qtd})", fontsize=11, color=COR_TEXTO_CLARO, va="center")
        y -= n_filhos
    return salvar(figura, pasta, arquivo)


def grafico_anos_referencias(artigos, pasta, arquivo):
    anos = Counter(ano for a in artigos for ano in a["anos_referencias"] if ano)
    if not anos:
        return None
    figura, eixo = plt.subplots(figsize=(11, 4))
    lista_anos = sorted(anos)
    eixo.bar(lista_anos, [anos[a] for a in lista_anos], color=COR_PRINCIPAL, width=0.8)
    eixo.set_xlabel("Ano de publicação da referência")
    eixo.set_ylabel("Quantidade")
    eixo.yaxis.grid(True, color=COR_GRADE)
    eixo.set_axisbelow(True)
    return salvar(figura, pasta, arquivo)


def grafico_avaliacao(resumo, pasta, arquivo):
    elementos = ["objetivo", "problema", "metodo", "contribuicao", "trabalho_futuro", "media"]
    nomes = ["Objetivo", "Problema", "Método", "Contribuição", "Trab. futuro", "Média"]
    metricas = [("precisao", "Precisão", COR_PRINCIPAL), ("revocacao", "Revocação", COR_SECUNDARIA),
                ("f1", "F1", COR_TERCEIRA)]
    x = np.arange(len(elementos))
    largura = 0.26

    figura, eixo = plt.subplots(figsize=(11, 5))
    for k, (chave, rotulo, cor) in enumerate(metricas):
        valores = [resumo[e][chave] for e in elementos]
        barras = eixo.bar(x + (k - 1) * largura, valores, largura, label=rotulo, color=cor)
        if chave == "f1":
            for barra, valor in zip(barras, valores):
                eixo.text(barra.get_x() + barra.get_width() / 2, valor + 0.015, f"{valor:.2f}",
                          ha="center", fontsize=9)
    eixo.set_xticks(x)
    eixo.set_xticklabels(nomes)
    eixo.set_ylim(0, 1.1)
    eixo.yaxis.grid(True, color=COR_GRADE)
    eixo.set_axisbelow(True)
    eixo.legend(frameon=False, ncol=3, loc="upper left")
    return salvar(figura, pasta, arquivo)


def somar_mencoes(artigos, chave):
    """Total de menções e número de artigos em que cada técnica (ou tarefa) aparece."""
    total, em_artigos = Counter(), Counter()
    for artigo in artigos:
        for nome, quantidade in artigo[chave].items():
            total[nome] += quantidade
            if quantidade:
                em_artigos[nome] += 1
    return total, em_artigos


def gerar_graficos(artigos, matriz_similaridade, pasta, raiz_arvore):
    os.makedirs(pasta, exist_ok=True)
    arquivos = []

    frequencias = Counter()
    bigramas = Counter()
    for artigo in artigos:
        frequencias.update(artigo["bag_of_words"])
        bigramas.update(artigo["bigramas"])
    ranking = modelos.termos_mais_frequentes(frequencias, 20)
    todas_sentencas = [s for artigo in artigos for s in artigo["sentencas"]]

    # 1. termos mais citados e bigramas
    arquivos.append(grafico_barras([r[0] for r in ranking], [r[1] for r in ranking],
                                   "Frequência (lemas agrupados pelo radical)", pasta, "01_termos_mais_citados.png"))
    mais_bigramas = bigramas.most_common(15)
    arquivos.append(grafico_barras([" ".join(b) for b, _ in mais_bigramas], [q for _, q in mais_bigramas],
                                   "Frequência", pasta, "02_bigramas.png"))

    # 2. nuvem de palavras geral
    arquivos.append(nuvem_de_palavras(frequencias, pasta, "03_nuvem_geral.png"))

    # 3. técnicas e tarefas mais mencionadas
    for chave, arquivo, cor, quantidade in [("tecnicas", "04_tecnicas.png", COR_PRINCIPAL, 15),
                                             ("tarefas", "05_tarefas.png", COR_TERCEIRA, 12)]:
        total, em_artigos = somar_mencoes(artigos, chave)
        mais = [(nome, q) for nome, q in total.most_common(quantidade) if q > 0]
        arquivos.append(grafico_barras([n for n, _ in mais], [q for _, q in mais],
                                       "Menções (entre parênteses: em quantos artigos aparece)", pasta, arquivo,
                                       cor=cor, notas=[f"{em_artigos[n]} art." for n, _ in mais]))

    # 4. evolução temporal: ocorrências por 1.000 palavras em cada ano
    palavras_por_ano = defaultdict(Counter)
    tecnicas_por_ano = defaultdict(Counter)
    total_por_ano = Counter()
    for artigo in artigos:
        ano = artigo["ano"] or 0
        palavras_por_ano[ano].update(artigo["bag_of_words"])
        tecnicas_por_ano[ano].update(artigo["tecnicas"])
        total_por_ano[ano] += sum(artigo["bag_of_words"].values())
    anos = sorted(total_por_ano)

    termos = [r[0] for r in ranking[:15]]
    matriz = [[1000 * palavras_por_ano[ano][t] / total_por_ano[ano] for ano in anos] for t in termos]
    arquivos.append(mapa_de_calor(matriz, termos, [str(a) for a in anos], "por 1.000 palavras",
                                  pasta, "06_evolucao_termos.png"))

    total_tecnicas, _ = somar_mencoes(artigos, "tecnicas")
    tecnicas = [n for n, q in total_tecnicas.most_common(12) if q > 0]
    matriz = [[1000 * tecnicas_por_ano[ano][t] / total_por_ano[ano] for ano in anos] for t in tecnicas]
    arquivos.append(mapa_de_calor(matriz, tecnicas, [str(a) for a in anos], "por 1.000 palavras",
                                  pasta, "07_evolucao_tecnicas.png", formato="{:.2f}"))

    # 5. termos dos trabalhos futuros
    termos_futuro = Counter()
    for artigo in artigos:
        termos_futuro.update(artigo["termos_futuro"])
    arquivos.append(nuvem_de_palavras(termos_futuro, pasta, "08_nuvem_trabalhos_futuros.png"))
    mais_futuro = termos_futuro.most_common(15)
    if mais_futuro:
        arquivos.append(grafico_barras([t for t, _ in mais_futuro], [q for _, q in mais_futuro],
                                       "Frequência", pasta, "09_termos_trabalhos_futuros.png", cor=COR_SECUNDARIA))

    # 6. termos x artigos
    nomes = [nome_curto(a) for a in artigos]
    matriz = [[1000 * a["bag_of_words"][t] / max(sum(a["bag_of_words"].values()), 1) for a in artigos]
              for t in termos]
    arquivos.append(mapa_de_calor(matriz, termos, nomes, "por 1.000 palavras", pasta,
                                  "10_termos_por_artigo.png", formato="{:.0f}"))

    # 7. coocorrência, similaridade e árvore de palavras
    arquivos.append(grafo_coocorrencia(todas_sentencas, frequencias, pasta, "11_coocorrencia.png"))
    tamanho = (0.75 * len(nomes) + 4, 0.6 * len(nomes) + 2)
    arquivos.append(mapa_de_calor(matriz_similaridade, nomes, nomes, "cosseno", pasta,
                                  "12_similaridade.png", formato="{:.2f}", tamanho=tamanho))
    arquivos.append(arvore_de_palavras(todas_sentencas, raiz_arvore, pasta, "13_arvore_de_palavras.png"))

    # 8. ano das referências citadas
    arquivos.append(grafico_anos_referencias(artigos, pasta, "14_anos_das_referencias.png"))

    return [a for a in arquivos if a]
