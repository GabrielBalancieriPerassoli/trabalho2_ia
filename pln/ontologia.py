# Etapa 3 - grava os dados extraídos como instâncias da ontologia de artigo
# científico (ontologia/artigo_cientifico.ttl), em Turtle e em JSON-LD.
# O rdflib só monta e salva grafos RDF; não tem aprendizado de máquina.

import re
import unicodedata

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import XSD

import config

ART = Namespace(config.NAMESPACE)

CLASSE_DA_SECAO = {
    "resumo": ART.Resumo,
    "introducao": ART.Introducao,
    "trabalhos_relacionados": ART.TrabalhosRelacionados,
    "metodologia": ART.Metodologia,
    "resultados": ART.Resultados,
    "conclusao": ART.Conclusao,
    "agradecimentos": ART.Agradecimentos,
    "referencias": ART.SecaoReferencias,
    "apendice": ART.Apendice,
}

# elemento extraído -> (classe, propriedade que liga o artigo a ele)
CLASSE_DO_ELEMENTO = {
    "objetivo": (ART.Objetivo, ART.temObjetivo),
    "problema": (ART.Problema, ART.temProblema),
    "metodo": (ART.Metodo, ART.temMetodo),
    "contribuicao": (ART.Contribuicao, ART.temContribuicao),
    "trabalho_futuro": (ART.TrabalhoFuturo, ART.temTrabalhoFuturo),
}


def identificador(texto):
    """Transforma um texto num pedaço de URI: sem acento, espaço ou símbolo."""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"\.pdf$", "", texto, flags=re.IGNORECASE)
    return re.sub(r"[^A-Za-z0-9]+", "_", texto).strip("_")


def adicionar_artigo(grafo, artigo, corpus):
    uri = ART["artigo_" + identificador(artigo["arquivo"])]
    grafo.add((uri, RDF.type, ART.ArtigoCientifico))
    grafo.add((corpus, ART.temArtigo, uri))
    grafo.add((uri, RDFS.label, Literal(artigo["titulo"])))
    grafo.add((uri, ART.titulo, Literal(artigo["titulo"], lang="en")))
    grafo.add((uri, ART.nomeArquivo, Literal(artigo["arquivo"])))
    grafo.add((uri, ART.numeroPaginas, Literal(artigo["num_paginas"], datatype=XSD.integer)))
    grafo.add((uri, ART.numeroReferencias, Literal(len(artigo["referencias"]), datatype=XSD.integer)))
    if artigo["ano"]:
        grafo.add((uri, ART.ano, Literal(str(artigo["ano"]), datatype=XSD.gYear)))

    # autores: só quando o PDF traz nos metadados
    for nome in re.split(r";|,| and ", artigo["autores"] or ""):
        nome = nome.strip()
        if len(nome) > 3:
            autor = ART["autor_" + identificador(nome)]
            grafo.add((autor, RDF.type, ART.Autor))
            grafo.add((autor, ART.nome, Literal(nome)))
            grafo.add((uri, ART.temAutor, autor))

    # seções
    secao_por_tipo = {}
    for ordem, secao in enumerate(artigo["secoes"]):
        if secao["tipo"] == "inicio":
            continue
        uri_secao = URIRef(f"{uri}_secao_{ordem}")
        grafo.add((uri_secao, RDF.type, CLASSE_DA_SECAO.get(secao["tipo"], ART.OutraSecao)))
        grafo.add((uri_secao, ART.tituloSecao, Literal(secao["titulo"])))
        grafo.add((uri_secao, ART.ordem, Literal(ordem, datatype=XSD.integer)))
        grafo.add((uri_secao, ART.numeroPalavras, Literal(secao["num_palavras"], datatype=XSD.integer)))
        grafo.add((uri, ART.temSecao, uri_secao))
        secao_por_tipo.setdefault(secao["tipo"], uri_secao)

    # objetivo, problema, método, contribuição e trabalho futuro
    for elemento, frases in artigo["elementos"].items():
        classe, propriedade = CLASSE_DO_ELEMENTO[elemento]
        for numero, frase in enumerate(frases, start=1):
            uri_frase = URIRef(f"{uri}_{elemento}_{numero}")
            grafo.add((uri_frase, RDF.type, classe))
            grafo.add((uri_frase, ART.texto, Literal(frase["texto"], lang="en")))
            grafo.add((uri_frase, ART.pontuacao, Literal(frase["pontuacao"], datatype=XSD.integer)))
            if frase["secao"] in secao_por_tipo:
                grafo.add((uri_frase, ART.extraidoDe, secao_por_tipo[frase["secao"]]))
            grafo.add((uri, propriedade, uri_frase))

    # referências
    for numero, (referencia, ano) in enumerate(zip(artigo["referencias"], artigo["anos_referencias"]), start=1):
        uri_ref = URIRef(f"{uri}_ref_{numero}")
        grafo.add((uri_ref, RDF.type, ART.Referencia))
        grafo.add((uri_ref, ART.texto, Literal(referencia)))
        grafo.add((uri_ref, ART.ordem, Literal(numero, datatype=XSD.integer)))
        if ano:
            grafo.add((uri_ref, ART.anoReferencia, Literal(str(ano), datatype=XSD.gYear)))
        grafo.add((uri, ART.citaReferencia, uri_ref))

    # 10 termos mais frequentes
    for posicao, (termo, frequencia, radical, _) in enumerate(artigo["top_termos"], start=1):
        uri_termo = ART["termo_" + identificador(termo)]
        grafo.add((uri_termo, RDF.type, ART.Termo))
        grafo.add((uri_termo, ART.lema, Literal(termo)))
        grafo.add((uri_termo, ART.radical, Literal(radical)))
        ocorrencia = URIRef(f"{uri}_termo_{posicao}")
        grafo.add((ocorrencia, RDF.type, ART.OcorrenciaTermo))
        grafo.add((ocorrencia, ART.doTermo, uri_termo))
        grafo.add((ocorrencia, ART.frequencia, Literal(frequencia, datatype=XSD.integer)))
        grafo.add((ocorrencia, ART.posicaoRanking, Literal(posicao, datatype=XSD.integer)))
        grafo.add((uri, ART.temOcorrencia, ocorrencia))

    # técnicas e tarefas mencionadas
    for chave, classe, propriedade in [("tecnicas", ART.Tecnica, ART.mencionaTecnica),
                                       ("tarefas", ART.Tarefa, ART.mencionaTarefa)]:
        for nome, quantidade in artigo[chave].items():
            if quantidade == 0:
                continue
            prefixo = "tecnica" if chave == "tecnicas" else "tarefa"
            uri_item = ART[f"{prefixo}_{identificador(nome)}"]
            grafo.add((uri_item, RDF.type, classe))
            grafo.add((uri_item, RDFS.label, Literal(nome, lang="pt")))
            mencao = URIRef(f"{uri}_{prefixo}_{identificador(nome)}")
            grafo.add((mencao, RDF.type, ART.Mencao))
            grafo.add((mencao, ART.refereSe, uri_item))
            grafo.add((mencao, ART.frequencia, Literal(quantidade, datatype=XSD.integer)))
            grafo.add((uri, propriedade, mencao))
    return uri


def adicionar_similaridades(grafo, uris, matriz, limite=0.15):
    for i in range(len(uris)):
        for j in range(i + 1, len(uris)):
            nome1 = uris[i].split("#")[-1]
            nome2 = uris[j].split("#")[-1]
            uri_sim = ART[f"sim_{nome1}__{nome2}"]
            grafo.add((uri_sim, RDF.type, ART.Similaridade))
            grafo.add((uri_sim, ART.entreArtigos, uris[i]))
            grafo.add((uri_sim, ART.entreArtigos, uris[j]))
            grafo.add((uri_sim, ART.valor, Literal(round(matriz[i][j], 4), datatype=XSD.decimal)))
            if matriz[i][j] >= limite:
                grafo.add((uris[i], ART.similarA, uris[j]))
                grafo.add((uris[j], ART.similarA, uris[i]))


def salvar_ontologia(artigos, matriz, arquivo_turtle, arquivo_jsonld, nome_corpus):
    grafo = Graph()
    grafo.parse(config.ARQUIVO_ONTOLOGIA, format="turtle")  # classes e propriedades
    grafo.bind("art", ART)

    corpus = ART["corpus_" + identificador(nome_corpus)]
    grafo.add((corpus, RDF.type, ART.Corpus))
    grafo.add((corpus, ART.tema, Literal(config.TEMA, lang="pt")))
    grafo.add((corpus, ART.baseDados, Literal(config.BASE_DE_DADOS)))

    uris = [adicionar_artigo(grafo, artigo, corpus) for artigo in artigos]
    adicionar_similaridades(grafo, uris, matriz)

    grafo.serialize(destination=arquivo_turtle, format="turtle", encoding="utf-8")
    contexto = {"art": config.NAMESPACE, "xsd": str(XSD), "rdfs": str(RDFS)}
    grafo.serialize(destination=arquivo_jsonld, format="json-ld", context=contexto, indent=2, encoding="utf-8")
    return len(grafo)
