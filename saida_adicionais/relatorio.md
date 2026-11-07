# Análise de artigos científicos - Processamento de Linguagem Natural

Artigos analisados: 3

## 10 termos mais citados (sem as referências)

1. **read**: 258 ocorrências (radical 'read': read (258))
2. **plain**: 190 ocorrências (radical 'plain': plain (190))
3. **participant**: 177 ocorrências (radical 'particip': participant (176), participate (1))
4. **summary**: 172 ocorrências (radical 'summari': summary (172))
5. **information**: 168 ocorrências (radical 'inform': information (157), inform (6), informative (5))
6. **question**: 166 ocorrências (radical 'question': question (166))
7. **answer**: 140 ocorrências (radical 'answer': answer (138), answerable (2))
8. **reader**: 137 ocorrências (radical 'reader': reader (137))
9. **gist**: 137 ocorrências (radical 'gist': gist (137))
10. **medical**: 119 ocorrências (radical 'medic': medical (117), medically (1), medication (1))

## Bigramas e trigramas mais frequentes

Bigramas: key question (76); answer gist (66); question index (51); plain language (46); medical research (41); healthcare consumer (41); term definition (33); source document (29); read medical (24); expository write (22)

Trigramas: key question index (51); plain language summary (18); read medical research (13); natural language process (9); typical pdf reader (7); plain language answer (7); read difficulty understand (7); r-lf bsf word (7); in-situ plain language (6); generate plain language (5)

---

## Paper Plain: Making Medical Research Papers Approachable to Healthcare Consumers with Natural Language Processing

- Arquivo: 2203.00130v1.pdf | Ano: 2022 | Páginas: 39
- Seções: Keywords, Keywords, 1 INTRODUCTION, 2 BACKGROUND AND RELATED WORK, 3 OBSERVATIONS OF NON-EXPERT READERS, 4 PAPER PLAIN: READING SUPPORT FOR MEDICAL RESEARCH PAPERS, 5 IMPLEMENTATION, 6 USABILITY STUDY, 7 RESULTS, 8 DISCUSSION & FUTURE WORK, 9 CONCLUSION, ACKNOWLEDGMENTS, REFERENCES, Appendix: A INTERVIEWS WITH HEALTHCARE CONSUMERS AND PROVIDERS
- Referências: 111 (formato ieee)
- Perplexidade do modelo de bigramas: 1036
- 10 termos mais citados: read (237), plain (189), participant (176), question (161), answer (138), reader (137), gist (136), information (135), medical (119), research (110)
- Palavras-chave (TF-IDF): plain, read, reader, participant, question, medical, answer, gist

**Objetivo:**
- In this paper, we ask how interactive information interfaces can make the research literature approachable to non-expert healthcare consumers that need it - whom we refer to as "readers" in this paper.  _[introducao, 5 pontos]_
- In this paper we ask how interactive interfaces can make medical research papers approachable to healthcare consumers that need it.  _[conclusao, 4 pontos]_

**Problema:**
- Reading medical papers, however, can be a challenging experience.  _[resumo, 5 pontos]_
- However, these resources do not cover all medical conditions and treatments [9, 90], especially those which are the focus of emerging research [17, 86].  _[introducao, 6 pontos]_

**Método:**
- To improve access to medical papers, we introduce a novel interactive interface - Paper Plain1 - with four features powered by natural language processing: definitions of unfamiliar terms, in-situ plain language section summaries, a collection of key questions that guide readers to answering passages, and plain language summaries of the answering passages.  _[resumo, 5 pontos]_
- To improve access to medical papers, we develop a novel interactive system, Paper Plain, through an iterative design process.  _[introducao, 5 pontos]_
- The system is designed to make medical papers accessible with four features (illustrated in Figure 1) that combine to provide support at multiple levels of granularity (e.g., term, paragraph, section) and throughout the reading process.  _[introducao, 5 pontos]_

**Contribuições:**
- In summary, this paper contributes: (1) A characterization of the barriers readers face when they approach medical research papers.  _[introducao, 4 pontos]_
- (2) Paper Plain, an interactive reading interface for research papers that integrates existing affordances like term definition tooltips with novel affordances like in-situ plain language summaries of paper sections and a collection of key questions that guide readers to answering passages in the paper with paired plain language answers (§4).  _[introducao, 6 pontos]_
- (3) Evidence from our usability study that these new affordances helped readers quickly find places in a paper that were informative to them.  _[introducao, 6 pontos]_

**Trabalhos futuros:**
- We offer the following guidance for developing such future systems: Provide reading guidance Interactive reading systems for non-experts can provide more active support for guiding readers.  _[conclusao, 7 pontos]_
- Future systems could go further by reporting factuality measures along with generated text [83] or integrating a feedback mechanism for reporting inconsistent information in order to crowd-source these factuality checks.  _[conclusao, 7 pontos]_
- We are excited to integrate new advances for measuring and ensuring factuality in generations (e.g., [33, 60, 77]) into Paper Plain to help realize the promise of such models in real-world settings.  _[conclusao, 7 pontos]_
- In future work we are excited to observe the use of Paper Plain in more naturalistic settings.  _[conclusao, 13 pontos]_

Artigos mais parecidos (cosseno TF-IDF): 2304.02623v1.pdf (0.19), 2206.10883v3.pdf (0.15)

---

## Multi-LexSum: Real-World Summaries of Civil Rights Lawsuits at Multiple Granularities

- Arquivo: 2206.10883v3.pdf | Ano: 2022 | Páginas: 37
- Seções: Abstract, 1 Introduction, 2 Related work, 3 Multi-LexSum, 4 Experiments, 5 Human evaluation, 6 Conclusion, Acknowledgements, References, Appendix: A Multi-LexSum release
- Referências: 64 (formato ieee)
- Perplexidade do modelo de bigramas: 1480
- 10 termos mais citados: summary (126), summarization (58), model (53), document (47), multi-lexsum (43), source (41), task (31), train (29), long (29), generate (28)
- Palavras-chave (TF-IDF): summary, multi-lexsum, model, document, summarization, source, train, crlc

**Objetivo:**
- We present extensive analysis demonstrating that despite the high-quality summaries in the training data (adhering to strict content and style guidelines), state-of-the-art summarization models perform poorly on this task.  _[resumo, 5 pontos]_
- In this paper, we present a new dataset, Multi-LexSum, for studying automatic summarization in an important real-world application setting found in the Civil Rights Litigation Clearinghouse (CRLC).  _[introducao, 5 pontos]_

**Problema:**
- With the advent of large language models, methods for abstractive summarization have made great strides, creating potential for use in applications to aid knowledge workers processing unwieldy document collections.  _[resumo, 4 pontos]_
- Multi-LexSum presents a challenging multi-document summarization task given the length of the source documents, often exceeding two hundred pages per case.  _[resumo, 4 pontos]_

**Método:**
- We conduct a series of experiments on Multi-LexSum, and find that existing summarization models perform poorly.  _[introducao, 5 pontos]_

**Contribuições:**
- But to our knowledge, Multi-LexSum is the first dataset to provide summaries at multiple levels of granularity.  _[introducao, 4 pontos]_

**Trabalhos futuros:**
- (não encontrado)

Artigos mais parecidos (cosseno TF-IDF): 2304.02623v1.pdf (0.26), 2203.00130v1.pdf (0.15)

---

## Beyond Summarization: Designing AI Support for Real-World Expository Writing Tasks

- Arquivo: 2304.02623v1.pdf | Ano: 2023 | Páginas: 4
- Seções: ABSTRACT, KEYWORDS, 1 INTRODUCTION, 2 CHARACTERIZING EXPOSITORY, 3 DESIGNING AI SUPPORTS FOR, 4 CONCLUSION, ACKNOWLEDGMENTS, REFERENCES
- Referências: 35 (formato ieee)
- Perplexidade do modelo de bigramas: 1623
- 10 termos mais citados: write (77), author (27), support (23), expository (23), new (22), document (22), generation (19), source (18), read (17), model (16)
- Palavras-chave (TF-IDF): write, expository, author, support, new, document, source, read

**Objetivo:**
- In this position paper, we argue that developing AI supports for expository writing has unique and exciting research challenges and can lead to high real-world impacts.  _[resumo, 5 pontos]_
- In this paper, we argue that the unique characteristics in expository writing open up new opportunities for designing AI support.  _[conclusao, 4 pontos]_

**Problema:**
- However, AI-supported expository writing - including real-world tasks like scholars writing literature reviews or doctors writing progress notes - is relatively understudied.  _[resumo, 8 pontos]_
- While prior work has explored many exciting applications for LLMs, we argue thatexpository writing is a task that is understudied in existing work on AI augmented writing.  _[introducao, 8 pontos]_

**Método:**
- We characterize expository writing as evidence-based and knowledge-generating: it contains summaries of external documents as well as new information or knowledge.  _[resumo, 4 pontos]_
- We sketch three components for AI support design and discuss considerations for future research.  _[resumo, 4 pontos]_
- For example, when starting writing a survey paper, the authors come up with the query to find relevant papers first, and AI helps execute the search and discover related documents; after authors read the retrieved papers and come up with ideas for the writing, AI can help generate the writing text based on authors' ideas, and the writers only need to proofread model output.  _[introducao, 3 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- (não encontrado)

Artigos mais parecidos (cosseno TF-IDF): 2206.10883v3.pdf (0.26), 2203.00130v1.pdf (0.19)
