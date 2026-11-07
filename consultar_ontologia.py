"""
Exemplos de consultas SPARQL na ontologia gerada (Etapa 3).
Mostra que os dados salvos podem ser consultados como uma base de conhecimento.

Uso: python consultar_ontologia.py [saida/ontologia_artigos.ttl]
"""

import sys

from rdflib import Graph

arquivo = sys.argv[1] if len(sys.argv) > 1 else "saida/ontologia_artigos.ttl"
formato = "json-ld" if arquivo.endswith(".jsonld") else "turtle"

g = Graph()
g.parse(arquivo, format=formato)
print(f"{len(g)} triplas carregadas de {arquivo}\n")

PREFIXOS = """
PREFIX art: <http://www.din.uem.br/iia/artigo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

consultas = {
    "Objetivo de cada artigo (primeiro trecho encontrado)": """
        SELECT ?ano ?titulo (SAMPLE(?txt) AS ?objetivo) WHERE {
            ?a a art:ArtigoCientifico ; art:titulo ?titulo ; art:ano ?ano ; art:temObjetivo ?o .
            ?o art:texto ?txt .
        } GROUP BY ?ano ?titulo ORDER BY ?ano
    """,
    "Artigos que declaram contribuições explicitamente": """
        SELECT ?titulo (COUNT(?c) AS ?qtd) WHERE {
            ?a art:titulo ?titulo ; art:temContribuicao ?c .
        } GROUP BY ?titulo ORDER BY DESC(?qtd)
    """,
    "Técnicas mencionadas em mais artigos": """
        SELECT ?tecnica (COUNT(DISTINCT ?a) AS ?artigos) (SUM(?f) AS ?mencoes) WHERE {
            ?a art:mencionaTecnica ?m .
            ?m art:refereSe ?t ; art:frequencia ?f .
            ?t rdfs:label ?tecnica .
        } GROUP BY ?tecnica ORDER BY DESC(?artigos) DESC(?mencoes) LIMIT 8
    """,
    "Número de referências por artigo": """
        SELECT ?titulo ?n WHERE {
            ?a art:titulo ?titulo ; art:numeroReferencias ?n .
        } ORDER BY DESC(?n)
    """,
    "Pares de artigos mais parecidos (cosseno TF-IDF)": """
        SELECT ?a1 ?a2 ?v WHERE {
            ?s a art:Similaridade ; art:valor ?v ; art:entreArtigos ?x, ?y .
            ?x art:nomeArquivo ?a1 . ?y art:nomeArquivo ?a2 .
            FILTER(STR(?a1) < STR(?a2))
        } ORDER BY DESC(?v) LIMIT 5
    """,
}

for titulo, q in consultas.items():
    print("=" * 80)
    print(titulo)
    print("-" * 80)
    for linha in g.query(PREFIXOS + q):
        valores = [str(v) for v in linha]
        valores = [v if len(v) < 110 else v[:107] + "..." for v in valores]
        print("  " + " | ".join(valores))
    print()
