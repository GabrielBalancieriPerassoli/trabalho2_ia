# Trabalho 2 – IIA: Análise de Artigos Científicos com PLN

Universidade Estadual de Maringá – Departamento de Informática
Disciplina: Introdução à Inteligência Artificial
Tema: Processamento de Linguagem Natural – base IEEE Xplore

Equipe:
- Felipe Matheus – RA 107496
- Gabriel Balancieri Perassoli – RA 135854
- Guilherme da Silva Nascimento – RA 130162

## O que o programa faz

1. **Etapa 1:** lê os PDFs, limpa o texto, remove stopwords, faz lematização e
   stemming, monta bag-of-words, n-gramas, TF-IDF e um modelo de bigramas,
   mostra os 10 termos mais citados (sem as referências) e extrai as referências.
2. **Etapa 2:** extrai objetivo, problema, método, contribuições e trabalhos
   futuros de cada artigo usando regras (frases-gatilho).
3. **Etapa 3:** salva tudo como instâncias da ontologia do artigo científico, em
   Turtle e em JSON-LD.
4. **Etapa 4:** compara o que foi extraído com um gabarito feito à mão e calcula
   precisão, revocação e F1.

Também gera os gráficos pedidos: termos mais citados, nuvem de palavras,
técnicas mais mencionadas, evolução temporal e trabalhos futuros, além de
coocorrência, similaridade entre artigos e árvore de palavras.

Nenhuma biblioteca de aprendizado de máquina foi usada. Do NLTK usamos só a lista
de stopwords, o lematizador do WordNet e o stemmer de Porter.

## Instalação

```
pip install -r requirements.txt
```

Na primeira execução o programa baixa os recursos `stopwords` e `wordnet` do NLTK
(precisa de internet só nessa vez).

## Como rodar

```
python main.py --avaliar
python main.py --pasta artigos_adicionais --saida saida_adicionais --avaliar
python consultar_ontologia.py saida/ontologia_artigos.ttl
```

O primeiro comando processa a pasta `artigos/` e salva os resultados em `saida/`.
O segundo faz a demonstração com os artigos adicionais. O terceiro mostra
consultas SPARQL na ontologia gerada.

## Arquivos

```
main.py                    executa as etapas na ordem
config.py                  pastas, tema, stopwords extras, técnicas e tarefas
consultar_ontologia.py     exemplos de consultas SPARQL
ontologia/artigo_cientifico.ttl   classes e propriedades da ontologia (OWL)
avaliacao/gabarito.json    anotação manual usada na Etapa 4
pln/
  leitura.py               leitura do PDF, limpeza, título e ano
  secoes.py                divisão em seções e sentenças
  preprocessamento.py      tokens, stopwords, lematização e stemming
  modelos.py               bag-of-words, n-gramas, TF-IDF e modelo de bigramas
  referencias.py           extração das referências
  extracao.py              objetivo, problema, método, contribuição e trabalho futuro
  ontologia.py             gravação em Turtle e JSON-LD
  avaliacao.py             precisão, revocação e F1
  graficos.py              visualizações
  relatorio.py             relatório, referências e JSON de saída
```

Na pasta `saida/` ficam: `relatorio.md`, `referencias/` (um arquivo por artigo),
`extracoes.json`, `ontologia_artigos.ttl`, `ontologia_artigos.jsonld`,
`avaliacao.json` e `graficos/` (15 gráficos).

## Como funciona a extração (Etapa 2)

Cada frase recebe pontos para cada elemento: +3 para cada gatilho forte
(ex.: "the goal of this paper"), +1 para cada gatilho fraco (ex.: "we propose") e
um bônus ou desconto pela seção onde está. A frase fica no elemento em que passou
do limite mínimo com mais folga. Se a frase passa no limite de contribuição, ela
é contribuição e não pode ser objetivo. As regras estão em `pln/extracao.py`.

## Trocando pelos artigos do IEEE Xplore

1. Coloque os 12 artigos do IEEE em `artigos/` e os da demonstração em `artigos_adicionais/`.
2. Rode `python main.py --gerar-gabarito` para criar `saida/gabarito_modelo.json`.
3. Preencha o modelo com os trechos de cada artigo e salve como `avaliacao/gabarito.json`.
4. Rode de novo com `--avaliar` e atualize os números dos slides.

O código já trata o formato do IEEE (títulos `I. INTRODUCTION`, `Abstract—`,
referências `[1]` e a linha "Authorized licensed use limited to..." do rodapé).
Se o ano de algum artigo sair errado, corrija em `ANOS_CORRIGIDOS` no `config.py`.

## Resultados com os artigos de teste

| Medida | 12 artigos | 3 novos |
|---|---|---|
| F1 objetivo | 0,70 | 0,67 |
| F1 problema | 0,38 | 0,67 |
| F1 método | 0,55 | 0,57 |
| F1 contribuição | 1,00 | 1,00 |
| F1 trabalho futuro | 0,93 | 0,57 |
| F1 médio | 0,71 | 0,70 |
| Referências corretas | 99,8% | 100% |
| Título e ano | 100% | 100% |
