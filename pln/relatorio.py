# Arquivos de saída: relatório em Markdown, referências em texto, extrações em
# JSON e o modelo de gabarito para anotar à mão.

import json
import os

import config
from pln import modelos

NOMES_DOS_ELEMENTOS = {
    "objetivo": "Objetivo",
    "problema": "Problema",
    "metodo": "Método",
    "contribuicao": "Contribuições",
    "trabalho_futuro": "Trabalhos futuros",
}


def escrever_relatorio(artigos, frequencias, bigramas, trigramas, matriz, caminho):
    linhas = [f"# Análise de artigos científicos - {config.TEMA}", "",
              f"Artigos analisados: {len(artigos)}", "",
              "## 10 termos mais citados (sem as referências)", ""]

    for posicao, (termo, frequencia, radical, lemas) in enumerate(modelos.termos_mais_frequentes(frequencias, 10), 1):
        variacoes = ", ".join(f"{lema} ({qtd})" for lema, qtd in sorted(lemas.items(), key=lambda x: -x[1]))
        linhas.append(f"{posicao}. **{termo}**: {frequencia} ocorrências (radical '{radical}': {variacoes})")

    linhas += ["", "## Bigramas e trigramas mais frequentes", ""]
    linhas.append("Bigramas: " + "; ".join(f"{' '.join(b)} ({q})" for b, q in bigramas.most_common(10)))
    linhas.append("")
    linhas.append("Trigramas: " + "; ".join(f"{' '.join(t)} ({q})" for t, q in trigramas.most_common(10)))
    linhas.append("")

    for i, artigo in enumerate(artigos):
        secoes = ", ".join(s["titulo"] for s in artigo["secoes"] if s["tipo"] != "inicio")
        linhas += [
            "---", "",
            f"## {artigo['titulo']}", "",
            f"- Arquivo: {artigo['arquivo']} | Ano: {artigo['ano']} | Páginas: {artigo['num_paginas']}",
            f"- Seções: {secoes}",
            f"- Referências: {len(artigo['referencias'])} (formato {artigo['formato_referencias']})",
            f"- Perplexidade do modelo de bigramas: {artigo['perplexidade']:.0f}",
            "- 10 termos mais citados: " + ", ".join(f"{t[0]} ({t[1]})" for t in artigo["top_termos"]),
            "- Palavras-chave (TF-IDF): " + ", ".join(artigo["palavras_chave"]),
            "",
        ]
        for elemento, nome in NOMES_DOS_ELEMENTOS.items():
            linhas.append(f"**{nome}:**")
            frases = artigo["elementos"][elemento]
            if not frases:
                linhas.append("- (não encontrado)")
            for frase in frases:
                linhas.append(f"- {frase['texto']}  _[{frase['secao']}, {frase['pontuacao']} pontos]_")
            linhas.append("")

        parecidos = sorted(((matriz[i][j], artigos[j]["arquivo"]) for j in range(len(artigos)) if j != i),
                           reverse=True)[:3]
        linhas.append("Artigos mais parecidos (cosseno TF-IDF): "
                      + ", ".join(f"{nome} ({valor:.2f})" for valor, nome in parecidos))
        linhas.append("")

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas))


def salvar_referencias(artigos, pasta):
    os.makedirs(pasta, exist_ok=True)
    for artigo in artigos:
        nome = os.path.splitext(artigo["arquivo"])[0] + ".txt"
        with open(os.path.join(pasta, nome), "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Referências de: {artigo['titulo']} ({len(artigo['referencias'])})\n\n")
            for numero, referencia in enumerate(artigo["referencias"], 1):
                arquivo.write(f"[{numero}] {referencia}\n")


def salvar_extracoes(artigos, caminho):
    dados = []
    for artigo in artigos:
        dados.append({
            "arquivo": artigo["arquivo"],
            "titulo": artigo["titulo"],
            "ano": artigo["ano"],
            "num_paginas": artigo["num_paginas"],
            "secoes": artigo["secoes"],
            "top_termos": [{"termo": t[0], "frequencia": t[1]} for t in artigo["top_termos"]],
            "tecnicas": {nome: qtd for nome, qtd in artigo["tecnicas"].items() if qtd},
            "tarefas": {nome: qtd for nome, qtd in artigo["tarefas"].items() if qtd},
            "elementos": artigo["elementos"],
            "num_referencias": len(artigo["referencias"]),
            "referencias": artigo["referencias"],
            "tempo": artigo["tempo"],
        })
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def gerar_modelo_gabarito(artigos, caminho):
    modelo = {"_instrucoes": "Copie para cada lista os trechos do artigo. "
                             "Confira no PDF o título, o ano e o número de referências."}
    for artigo in artigos:
        modelo[artigo["arquivo"]] = {
            "titulo": artigo["titulo"],
            "ano": artigo["ano"],
            "num_referencias": len(artigo["referencias"]),
            "objetivo": [], "problema": [], "metodo": [], "contribuicao": [], "trabalho_futuro": [],
        }
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(modelo, arquivo, ensure_ascii=False, indent=2)
