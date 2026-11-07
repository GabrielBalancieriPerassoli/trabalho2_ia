"""
Trabalho 2 - Introdução à Inteligência Artificial (DIN/UEM)
Análise de artigos científicos com Processamento de Linguagem Natural.

Equipe: Felipe Matheus (RA 107496), Gabriel Balancieri Perassoli (RA 135854)
        e Guilherme da Silva Nascimento (RA 130162)

Uso:
    python main.py                      processa a pasta artigos/ e salva tudo em saida/
    python main.py --avaliar            também compara com o gabarito (Etapa 4)
    python main.py --pasta artigos_adicionais --saida saida_adicionais --avaliar
    python main.py --gerar-gabarito     cria um gabarito vazio para anotar à mão
"""

import argparse
import json
import os
import time
from collections import Counter

import config
from pln import modelos, preprocessamento
from pln.avaliacao import avaliar, carregar_gabarito, imprimir_avaliacao
from pln.extracao import extrair_elementos
from pln.graficos import gerar_graficos, grafico_avaliacao
from pln.leitura import ler_artigo, listar_pdfs
from pln.ontologia import salvar_ontologia
from pln.referencias import ano_da_referencia, extrair_referencias
from pln.relatorio import escrever_relatorio, gerar_modelo_gabarito, salvar_extracoes, salvar_referencias
from pln.secoes import dividir_secoes, dividir_sentencas, separar_referencias

# Palavras que só anunciam o trabalho futuro ("in future work we plan to
# investigate...") e não dizem qual é o assunto. Ficam fora da contagem.
PALAVRAS_DE_ANUNCIO = {"future", "plan", "interest", "interesting", "investigate", "explore", "direction",
                       "research", "step", "excite", "exciting", "hope", "item", "area", "suggest",
                       "natural", "aim", "intend", "question", "open", "leave", "remain", "promise",
                       "worth", "next", "ultimately", "help", "effort"}


def processar_artigo(caminho):
    """Etapas 1 e 2 para um artigo."""
    inicio = time.time()
    artigo = ler_artigo(caminho, config.ANOS_CORRIGIDOS)

    secoes = dividir_secoes(artigo["texto"])
    corpo, texto_referencias = separar_referencias(secoes)

    # o texto analisado é o corpo do artigo, sem o cabeçalho (título e autores)
    # e sem as referências
    tem_resumo = any(s["tipo"] == "resumo" for s in corpo)
    texto = "\n".join(s["texto"] for s in corpo if s["tipo"] != "inicio" or not tem_resumo)
    sentencas = dividir_sentencas(texto)

    # Etapa 1: pré-processamento, modelos e referências
    bag_of_words = modelos.bag_of_words(preprocessamento.preprocessar(texto))
    referencias, formato = extrair_referencias(texto_referencias)

    # Etapa 2: objetivo, problema, método, contribuições e trabalhos futuros
    elementos = extrair_elementos(secoes)
    texto_futuro = " ".join(frase["texto"] for frase in elementos["trabalho_futuro"])
    termos_futuro = Counter(lema for lema in preprocessamento.preprocessar(texto_futuro)
                            if lema not in PALAVRAS_DE_ANUNCIO)

    artigo.update({
        "secoes": [{"titulo": s["titulo"], "tipo": s["tipo"], "num_palavras": len(s["texto"].split())}
                   for s in secoes],
        "sentencas": sentencas,
        "bag_of_words": bag_of_words,
        "bigramas": modelos.contar_ngramas(sentencas, 2),
        "trigramas": modelos.contar_ngramas(sentencas, 3),
        "top_termos": modelos.termos_mais_frequentes(bag_of_words, config.QTD_TERMOS),
        "tecnicas": modelos.contar_mencoes(texto, config.TECNICAS),
        "tarefas": modelos.contar_mencoes(texto, config.TAREFAS),
        "referencias": referencias,
        "anos_referencias": [ano_da_referencia(r) for r in referencias],
        "formato_referencias": formato,
        "elementos": elementos,
        "termos_futuro": termos_futuro,
    })
    artigo["tempo"] = round(time.time() - inicio, 2)
    return artigo


def calcular_perplexidades(artigos):
    """Para cada artigo, treina o modelo de bigramas com os outros artigos e mede
    a perplexidade nele. Quanto maior, mais o vocabulário dele foge do resto."""
    sentencas = [[preprocessamento.preprocessar(s) for s in a["sentencas"]] for a in artigos]
    for i, artigo in enumerate(artigos):
        treino = []
        for j in range(len(artigos)):
            if j != i:
                treino += sentencas[j]
        modelo = modelos.ModeloBigramas().treinar(treino)
        artigo["perplexidade"] = modelo.perplexidade(sentencas[i])


def ler_argumentos():
    parser = argparse.ArgumentParser(description="Análise de artigos científicos com PLN")
    parser.add_argument("--pasta", default=config.PASTA_ARTIGOS, help="pasta com os PDFs")
    parser.add_argument("--saida", default=config.PASTA_SAIDA, help="pasta onde os resultados são salvos")
    parser.add_argument("--avaliar", action="store_true", help="compara com o gabarito (Etapa 4)")
    parser.add_argument("--gabarito", default=config.ARQUIVO_GABARITO)
    parser.add_argument("--gerar-gabarito", action="store_true", help="cria um gabarito vazio")
    parser.add_argument("--sem-graficos", action="store_true")
    return parser.parse_args()


def main():
    args = ler_argumentos()
    os.makedirs(args.saida, exist_ok=True)
    inicio = time.time()

    # Etapas 1 e 2
    pdfs = listar_pdfs(args.pasta)
    print(f"{len(pdfs)} PDFs encontrados em {args.pasta}\n")
    if not pdfs:
        return
    artigos = []
    for caminho in pdfs:
        print(f"Processando {os.path.basename(caminho)}...", end=" ", flush=True)
        artigo = processar_artigo(caminho)
        artigos.append(artigo)
        print(f"ok ({artigo['tempo']} s, {len(artigo['referencias'])} referências)")

    if args.gerar_gabarito:
        gerar_modelo_gabarito(artigos, os.path.join(args.saida, "gabarito_modelo.json"))
        print("Modelo de gabarito salvo em", os.path.join(args.saida, "gabarito_modelo.json"))

    # termos do corpus inteiro
    frequencias, bigramas, trigramas = Counter(), Counter(), Counter()
    for artigo in artigos:
        frequencias.update(artigo["bag_of_words"])
        bigramas.update(artigo["bigramas"])
        trigramas.update(artigo["trigramas"])

    print("\n10 termos mais citados (sem as referências):")
    for posicao, (termo, frequencia, _, _) in enumerate(modelos.termos_mais_frequentes(frequencias, 10), 1):
        print(f"  {posicao:2d}. {termo:<15} {frequencia}")

    # TF-IDF, similaridade entre artigos e perplexidade
    matriz, vetores = modelos.matriz_similaridade([a["bag_of_words"] for a in artigos])
    for artigo, vetor in zip(artigos, vetores):
        artigo["palavras_chave"] = modelos.palavras_chave(vetor)
    calcular_perplexidades(artigos)

    escrever_relatorio(artigos, frequencias, bigramas, trigramas, matriz, os.path.join(args.saida, "relatorio.md"))
    salvar_referencias(artigos, os.path.join(args.saida, "referencias"))
    salvar_extracoes(artigos, os.path.join(args.saida, "extracoes.json"))

    # Etapa 3: ontologia
    nome_corpus = os.path.basename(os.path.normpath(args.pasta))
    triplas = salvar_ontologia(artigos, matriz,
                               os.path.join(args.saida, "ontologia_artigos.ttl"),
                               os.path.join(args.saida, "ontologia_artigos.jsonld"),
                               nome_corpus)
    print(f"\nOntologia salva em Turtle e JSON-LD ({triplas} triplas)")

    # visualizações
    pasta_graficos = os.path.join(args.saida, "graficos")
    if not args.sem_graficos:
        graficos = gerar_graficos(artigos, matriz, pasta_graficos, config.RAIZ_ARVORE)
        print(f"{len(graficos)} gráficos salvos em {pasta_graficos}")

    # Etapa 4: avaliação
    if args.avaliar:
        gabarito = carregar_gabarito(args.gabarito)
        resumo, por_artigo = avaliar(artigos, gabarito)
        if resumo["artigos_avaliados"] == 0:
            print("Nenhum artigo desta pasta está no gabarito.")
        else:
            imprimir_avaliacao(resumo)
            with open(os.path.join(args.saida, "avaliacao.json"), "w", encoding="utf-8") as arquivo:
                json.dump({"resumo": resumo, "por_artigo": por_artigo}, arquivo, ensure_ascii=False, indent=2)
            if not args.sem_graficos:
                grafico_avaliacao(resumo, pasta_graficos, "15_avaliacao.png")

    print(f"\nConcluído em {time.time() - inicio:.1f} s. Resultados em {args.saida}")


if __name__ == "__main__":
    main()
