# Etapa 4 - avaliação do desempenho da extração.
#
# Comparamos o que o sistema extraiu com o gabarito feito à mão
# (avaliacao/gabarito.json). A frase extraída pode vir um pouco diferente da
# anotada (hífen, espaço, um pedaço a mais), então usamos a sobreposição de
# palavras: se o F1 entre as palavras das duas frases for pelo menos 0,5,
# contamos como acerto (é a mesma ideia do ROUGE-1).

import json
import re
from collections import Counter

from pln.extracao import ELEMENTOS
from pln.preprocessamento import STOPWORDS

LIMITE_ACERTO = 0.5


def palavras_da_frase(frase):
    palavras = re.findall(r"[a-z0-9]+", frase.lower())
    sem_stopwords = [p for p in palavras if p not in STOPWORDS]
    return sem_stopwords or palavras


def semelhanca(frase1, frase2):
    """F1 entre as palavras das duas frases (0 = nada em comum, 1 = iguais)."""
    palavras1 = Counter(palavras_da_frase(frase1))
    palavras2 = Counter(palavras_da_frase(frase2))
    comuns = sum((palavras1 & palavras2).values())
    if comuns == 0:
        return 0.0
    precisao = comuns / sum(palavras1.values())
    revocacao = comuns / sum(palavras2.values())
    return 2 * precisao * revocacao / (precisao + revocacao)


def contar_acertos(extraidas, gabarito):
    """Cada frase do gabarito só pode ser usada uma vez. Os pares mais
    parecidos são casados primeiro."""
    pares = []
    for i, extraida in enumerate(extraidas):
        for j, anotada in enumerate(gabarito):
            pares.append((semelhanca(extraida, anotada), i, j))
    pares.sort(reverse=True)

    usadas_extraidas, usadas_gabarito = set(), set()
    acertos = 0
    for valor, i, j in pares:
        if valor < LIMITE_ACERTO:
            break
        if i in usadas_extraidas or j in usadas_gabarito:
            continue
        usadas_extraidas.add(i)
        usadas_gabarito.add(j)
        acertos += 1
    return acertos


def calcular_metricas(acertos, extraidas, anotadas):
    precisao = acertos / extraidas if extraidas else (1.0 if anotadas == 0 else 0.0)
    revocacao = acertos / anotadas if anotadas else (1.0 if extraidas == 0 else 0.0)
    f1 = 2 * precisao * revocacao / (precisao + revocacao) if precisao + revocacao else 0.0
    return {"precisao": precisao, "revocacao": revocacao, "f1": f1}


def carregar_gabarito(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return {nome: valor for nome, valor in dados.items() if not nome.startswith("_")}


def avaliar(artigos, gabarito):
    totais = {elemento: {"acertos": 0, "extraidas": 0, "anotadas": 0} for elemento in ELEMENTOS}
    trocas = Counter()  # frase do gabarito de um elemento extraída como outro elemento
    erros_referencias = []
    total_referencias = 0
    titulos_certos = 0
    anos_certos = 0
    tempos = []
    por_artigo = []

    avaliados = [a for a in artigos if a["arquivo"] in gabarito]
    for artigo in avaliados:
        anotacao = gabarito[artigo["arquivo"]]
        linha = {"arquivo": artigo["arquivo"]}

        for elemento in ELEMENTOS:
            extraidas = [e["texto"] for e in artigo["elementos"][elemento]]
            anotadas = anotacao.get(elemento, [])
            acertos = contar_acertos(extraidas, anotadas)
            totais[elemento]["acertos"] += acertos
            totais[elemento]["extraidas"] += len(extraidas)
            totais[elemento]["anotadas"] += len(anotadas)
            linha[elemento] = {"acertos": acertos, "extraidas": len(extraidas), "anotadas": len(anotadas)}

            for outro in ELEMENTOS:
                if outro != elemento:
                    extraidas_outro = [e["texto"] for e in artigo["elementos"][outro]]
                    trocas[f"{elemento} -> {outro}"] += contar_acertos(extraidas_outro, anotadas)

        quantidade = len(artigo["referencias"])
        erros_referencias.append(abs(quantidade - anotacao["num_referencias"]))
        total_referencias += anotacao["num_referencias"]
        linha["referencias"] = {"sistema": quantidade, "gabarito": anotacao["num_referencias"]}

        if semelhanca(artigo["titulo"], anotacao["titulo"]) >= 0.9:
            titulos_certos += 1
        if artigo["ano"] == anotacao["ano"]:
            anos_certos += 1
        tempos.append(artigo["tempo"])
        por_artigo.append(linha)

    n = len(avaliados)
    resumo = {"artigos_avaliados": n}
    for elemento in ELEMENTOS:
        t = totais[elemento]
        resumo[elemento] = calcular_metricas(t["acertos"], t["extraidas"], t["anotadas"])
        resumo[elemento].update(t)
    resumo["media"] = {metrica: sum(resumo[e][metrica] for e in ELEMENTOS) / len(ELEMENTOS)
                       for metrica in ("precisao", "revocacao", "f1")}
    resumo["referencias"] = {
        "erro_medio": sum(erros_referencias) / n if n else 0,
        "artigos_sem_erro": erros_referencias.count(0),
        "acerto": 1 - sum(erros_referencias) / total_referencias if total_referencias else 0,
    }
    resumo["titulo_correto"] = titulos_certos / n if n else 0
    resumo["ano_correto"] = anos_certos / n if n else 0
    resumo["tempo_medio"] = sum(tempos) / n if n else 0
    resumo["trocas_entre_elementos"] = {chave: valor for chave, valor in trocas.items() if valor}
    return resumo, por_artigo


def imprimir_avaliacao(resumo):
    print(f"\nArtigos avaliados: {resumo['artigos_avaliados']}")
    print(f"{'Elemento':<17}{'Precisão':>10}{'Revocação':>11}{'F1':>7}   acertos/extraídas/anotadas")
    for elemento in ELEMENTOS:
        r = resumo[elemento]
        print(f"{elemento:<17}{r['precisao']:>10.2f}{r['revocacao']:>11.2f}{r['f1']:>7.2f}"
              f"   {r['acertos']}/{r['extraidas']}/{r['anotadas']}")
    m = resumo["media"]
    print(f"{'média':<17}{m['precisao']:>10.2f}{m['revocacao']:>11.2f}{m['f1']:>7.2f}")

    ref = resumo["referencias"]
    print(f"\nReferências: {ref['acerto']:.1%} de acerto, contagem exata em {ref['artigos_sem_erro']} artigos")
    print(f"Título correto: {resumo['titulo_correto']:.0%}   Ano correto: {resumo['ano_correto']:.0%}")
    print(f"Tempo médio por artigo: {resumo['tempo_medio']:.2f} s")
    if resumo["trocas_entre_elementos"]:
        print("Frases do gabarito extraídas como outro elemento:", resumo["trocas_entre_elementos"])
