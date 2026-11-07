# Análise de artigos científicos - Processamento de Linguagem Natural

Artigos analisados: 12

## 10 termos mais citados (sem as referências)

1. **model**: 397 ocorrências (radical 'model': model (396), modeler (1))
2. **extraction**: 322 ocorrências (radical 'extract': extraction (234), extract (81), extractive (5), extractiveness (2))
3. **relation**: 297 ocorrências (radical 'relat': relation (258), relate (27), relational (12))
4. **train**: 269 ocorrências (radical 'train': train (269))
5. **word**: 252 ocorrências (radical 'word': word (252))
6. **feature**: 252 ocorrências (radical 'featur': feature (252))
7. **phrase**: 196 ocorrências (radical 'phrase': phrase (196))
8. **sentence**: 192 ocorrências (radical 'sentenc': sentence (191), sentencize (1))
9. **task**: 180 ocorrências (radical 'task': task (180))
10. **system**: 173 ocorrências (radical 'system': system (173))

## Bigramas e trigramas mais frequentes

Bigramas: relation phrase (86); language model (65); text runner (58); human evaluation (48); story element (44); train data (38); full text (36); source document (34); open ie (25); semantic label (25)

Trigramas: open ie system (15); bm bm bm (9); word confusion network (9); long-form summarization datasets (8); relational n-gram model (8); semantic role label (8); cy bn bn (8); np player player (8); transformer language model (7); pretrained language model (7)

---

## SPECTER: Document-level Representation Learning using Citation-informed Transformers

- Arquivo: 2020.acl-main.207.pdf | Ano: 2020 | Páginas: 13
- Seções: Abstract, 1 Introduction, 2 Model, 3 SCIDOCS Evaluation Framework, 4 Experiments, 5 Results, 6 Analysis, 7 Related Work, 8 Conclusions and Future Work, Acknowledgements, References, Appendix: A Appendix A - Baseline Details, 9. Sentence BERT Sentence BERT (Reimers and
- Referências: 57 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2643
- 10 termos mais citados: model (83), task (62), citation (53), specter (44), representation (40), embeddings (39), train (38), document (28), pretrained (27), dataset (27)
- Palavras-chave (TF-IDF): specter, citation, embeddings, model, transformer, scibert, task, fine-tune

**Objetivo:**
- We propose SPECTER , a new method to generate document-level embedding of scientific documents based on pretraining a Transformer language model on a powerful signal of document-level relatedness: the citation graph.  _[resumo, 5 pontos]_
- Here, we study how to leverage the power of pretrained language models to learn embeddings for scientific documents.  _[introducao, 5 pontos]_

**Problema:**
- Recent Transformer language models like BERT learn powerful textual representations, but these models are targeted towards token- and sentence-level training objectives and do not leverage information on inter-document relatedness, which limits their document-level representation power.  _[resumo, 7 pontos]_
- While such models are widely used for representing individual words ∗ Equal contribution 1 https://github.com/allenai/specter or sentences, extensions to whole-document embeddings are relatively underexplored.  _[introducao, 7 pontos]_

**Método:**
- We specifically use citations as a naturally occurring, inter-document incidental supervision signal indicating which documents are most related and formulate the signal into a triplet-loss pretraining objective.  _[introducao, 4 pontos]_
- In experiments, we show that SPECTER 's representations substantially outperform the state- 2SPECTER : Scientific Paper Embeddings using Citation-informed TransformERs of-the-art on a variety of document-level tasks, including topic classification, citation prediction, and recommendation.  _[introducao, 3 pontos]_
- Inspired by the recent success of pretrained Transformer language models across various NLP tasks, we use the Transformer model architecture as basis of encoding the input paper.  _[metodologia, 3 pontos]_

**Contribuições:**
- As an additional contribution of this work, we introduce and release SCIDOCS 3 , a novel collection of data sets and an evaluation suite for document-level embeddings in the scientific domain.  _[introducao, 5 pontos]_

**Trabalhos futuros:**
- It would be interesting to initialize our model weights from more recent Transformer models to investigate if additional gains are possible.  _[conclusao, 7 pontos]_
- Another item of future work is to develop better multitask approaches to leverage multiple signals of relatedness information during training.  _[conclusao, 10 pontos]_
- Including other information such as outgoing citations as additional input to the model would be yet another area to explore in future.  _[conclusao, 10 pontos]_

Artigos mais parecidos (cosseno TF-IDF): 2020.acl-main.447.pdf (0.31), N18-3011.pdf (0.29), roark13.pdf (0.16)

---

## S2ORC: The Semantic Scholar Open Research Corpus

- Arquivo: 2020.acl-main.447.pdf | Ano: 2020 | Páginas: 15
- Seções: Abstract, 1 Introduction, 2 Constructing the corpus, 3 The S2ORC dataset, 4 Evaluation, 5 Pretraining BERT on S2ORC, 6 Applications of S2ORC, 7 Related work, 8 Conclusion, Acknowledgements, References, Appendix: A Background & Terminology
- Referências: 55 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2772
- 10 termos mais citados: text (63), citation (53), link (43), corpus (41), parse (38), pdfs (36), full (35), latex (34), academic (33), bibliography (33)
- Palavras-chave (TF-IDF): citation, latex, bibliography, grobid, text, academic, link, entry

**Objetivo:**
- We introduce S2ORC, 1 a large corpus of 81.1M English-language academic papers spanning many academic disciplines.  _[resumo, 5 pontos]_
- In this paper, we describe the construction of S2ORC (§2).  _[introducao, 5 pontos]_

**Problema:**
- Yet, existing corpora are not without their limitations.  _[introducao, 6 pontos]_
- Although these papers that lack text may be useful as cite-able nodes in S2ORC, they are generally of lower quality and are filtered out of the corpus to improve corpus quality.  _[metodologia, 4 pontos]_

**Método:**
- In S2ORC, we aggregate papers from hundreds of academic publishers and digital archives into a unified source, and create the largest publicly-available collection of machine-readable academic text to date.  _[resumo, 4 pontos]_
- We then evaluate a BERT model pretrained on S2ORC (§5), and discuss potential applications to a variety of NLP and analysis tasks over academic text (§6).  _[introducao, 4 pontos]_
- The output of this pipeline is visualized in Figure 1.  _[metodologia, 3 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- (não encontrado)

Artigos mais parecidos (cosseno TF-IDF): 2020.acl-main.207.pdf (0.31), N18-3011.pdf (0.30), fader11.pdf (0.09)

---

## LONGEVAL: Guidelines for Human Evaluation of Faithfulness in Long-form Summarization

- Arquivo: 2023.eacl-main.121.pdf | Ano: 2023 | Páginas: 20
- Seções: Abstract, 1 Introduction, 2 Survey of human evaluation practices, 3 The LONG EVAL guidelines for, 4 Related Work, 5 Conclusion, Limitations, Ethical Considerations, Acknowledgments, References, Appendix: Appendix
- Referências: 66 (formato autor-ano)
- Perplexidade do modelo de bigramas: 3042
- 10 termos mais citados: summary (144), annotation (137), evaluation (89), human (73), source (52), fine (51), unit (49), summarization (43), long-form (42), document (41)
- Palavras-chave (TF-IDF): summary, fine, human, annotation, long-form, coarse, unit, summarization

**Objetivo:**
- To move towards a more consistent and efficient human evaluation, we present LONG EVAL, a set of guidelines for human evaluation of faithfulness in long-form summarization (Section 3).  _[introducao, 3 pontos]_
- We present the LONG EVAL guidelines, a set of recommendations for moving towards standardized human evaluation of long-form summarization.  _[conclusao, 4 pontos]_

**Problema:**
- While human evaluation remains best practice for accurately judging the faithfulness of automatically-generated summaries, few solutions exist to address the increased difficulty and workload when evaluating long-form summaries.  _[resumo, 5 pontos]_
- Unfortunately, human evaluation tends to be labor-intensive, expensive to scale, and difficult to design.  _[introducao, 8 pontos]_

**Método:**
- We deploy LONG EVAL in annotation studies on two long-form summarization datasets in different domains (SQuALITY and PubMed), and we find that switching to a finer granularity of judgment (e.g., clause-level) reduces inter-annotator variance in faithfulness scores (e.g., std-dev from 18.5 to 6.8).  _[resumo, 5 pontos]_
- To better understand the challenges of human evaluation on long-form summaries (150 words or longer), we first conduct a comprehensive survey of 162 publications and preprints on long-form summarization (Section 2).  _[introducao, 5 pontos]_
- We empirically evaluate LONG EVAL using human annotation studies on two long-form summarization datasets: SQuALITY (Wang et al., 2022) and PubMed (Cohan et al., 2018).  _[introducao, 6 pontos]_

**Contribuições:**
- Overall, our contributions are: (1) a 162-paper survey of current human evaluation practices in long-form summarization; (2) LONG EVAL, a set of three guidelines for evaluating faithfulness in long-form summarization; (3) an empirical validation of LONG EVAL guidelines on two long-form summarization datasets in different domains (SQuALITY and PubMed); (4) A dataset with 3-way fine-grained human faithfulness judgments for 120 SQuALITY & PubMed summaries annotated using LONG EVAL which can be used for benchmarking automatic metrics.  _[introducao, 5 pontos]_

**Trabalhos futuros:**
- As future work, we plan to conduct experiments on other aspects of summarization evaluation like salience and coherence.  _[conclusao, 8 pontos]_
- Designing non-uniform weighing schemes is an interesting direction for future research.  _[conclusao, 8 pontos]_

Artigos mais parecidos (cosseno TF-IDF): 2020.acl-main.447.pdf (0.09), N18-3011.pdf (0.08), 2020.acl-main.207.pdf (0.07)

---

## Construction of the Literature Graph in Semantic Scholar

- Arquivo: N18-3011.pdf | Ano: 2018 | Páginas: 8
- Seções: Abstract, 1 Introduction, 2 Structure of The Literature Graph, 3 Extracting Metadata, 4 Entity Extraction and Linking, 5 Other Research Problems, 6 Conclusion and Future Work, References
- Referências: 27 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2560
- 10 termos mais citados: entity (78), model (45), mention (37), extraction (37), author (36), literature (28), graph (27), label (27), token (25), node (22)
- Palavras-chave (TF-IDF): entity, mention, author, graph, literature, model, edge, scientific

**Objetivo:**
- We describe a deployed scalable system for organizing published scientific literature into a heterogeneous graph to facilitate algorithmic manipulation and discovery.  _[resumo, 5 pontos]_
- We describe methods used in a scalable deployed production system for extracting structured information from scientific documents into the literature graph (see Fig. 1).  _[introducao, 5 pontos]_

**Problema:**
- Despite notable advances in scientific search engines, data mining and digital libraries (e.g., Wu et al., 2014), researchers remain unable to answer simple questions such as: What is the percentage of female subjects in depression clinical trials?  _[introducao, 7 pontos]_
- These assumptions, while useful for developing and benchmarking new methods, are unrealistic for many domains and applications.  _[introducao, 4 pontos]_

**Método:**
- We reduce literature graph construction into familiar NLP tasks (e.g., entity extraction and linking), point out research challenges due to differences from standard formulations of these tasks, and report empirical results for each task.  _[resumo, 4 pontos]_
- We reduce literature graph construction into familiar NLP tasks such as sequence labeling, entity linking and relation extraction, and address some of the impractical assumptions commonly made in the standard formulations of these tasks.  _[introducao, 4 pontos]_
- The paper also serves as an overview of the approach we adopt at www.semanticscholar.org in a step towards more intelligent academic search engines (Etzioni, 2011).  _[introducao, 4 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- Three research directions follow from this work and other similar projects, e.g., Hahn-Powell et al. (2017); Wu et al. (2014): i) improving quality and enriching content of the literature graph (e.g., ontology matching and knowledge base population). ii) aggregating domain-specific extractions across many papers to enable a better understanding of the literature as a whole (e.g., identifying demographic biases in clinical trial participants and summarizing empirical results on important tasks). iii) exploring the literature via natural language interfaces.  _[conclusao, 7 pontos]_

Artigos mais parecidos (cosseno TF-IDF): 2020.acl-main.447.pdf (0.30), 2020.acl-main.207.pdf (0.29), bunescu-acl07.pdf (0.21)

---

## Sparse Information Extraction: Unsupervised Language Models to the Rescue

- Arquivo: P07-1088.pdf | Ano: 2007 | Páginas: 8
- Seções: Abstract, 1 Introduction, 2 IE Assessment, 3 Experimental Results, 4 Related Work, 5 Conclusions, Acknowledgements, References
- Referências: 15 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2487
- 10 termos mais citados: extraction (93), relation (76), realm (61), argument (56), model (46), type (41), assess (38), hmm-t (33), corpus (32), context (31)
- Palavras-chave (TF-IDF): realm, extraction, argument, hmm-t, relation, seed, sparse, model

**Objetivo:**
- This paper shows how to assess the correctness of sparse extractions by utilizing unsupervised language models.  _[resumo, 4 pontos]_
- This paper introduces the idea that language modeling techniques such as n-gram statistics (Manning and Sch ̈utze, 1999) and HMMs (Rabiner, 1989) can be used to effectively assess sparse extractions.  _[introducao, 4 pontos]_

**Problema:**
- However, Zipf's Law governs the distribution of extractions.  _[introducao, 5 pontos]_
- This problem is particularly acute when moving beyond unary relations.  _[introducao, 5 pontos]_

**Método:**
- Because REALM pre-computes language models based on its corpus and does not require any hand-tagged seeds, it is far more scalable than approaches that learn models for each individual relation from hand-tagged data.  _[resumo, 3 pontos]_
- Second, we employ an instance of the distributional hypothesis (Harris, 1985), which can be phrased as follows: different instances of the same semantic relation tend to appear in similar textual contexts.  _[introducao, 4 pontos]_
- We assess sparse extractions by comparing the contexts in which they appear to those of more common extractions.  _[introducao, 5 pontos]_

**Contribuições:**
- The paper introduces the insight that the subfield of language modeling provides unsupervised methods that can be leveraged to assess sparse extractions.  _[introducao, 6 pontos]_
- The paper introduces an HMM-based technique for checking whether two arguments are of the proper type for a relation.  _[introducao, 6 pontos]_
- The paper introduces a relational n-gram model for the purpose of determining whether a sentence that mentions multiple arguments actually expresses a particular relationship between them.  _[introducao, 6 pontos]_
- The paper introduces a novel languagemodeling system called REALM that combines both HMM-based models and relational n-gram models, and shows that REALM reduces error by an average of 39% over previous methods, when applied to sparse extraction data.  _[introducao, 6 pontos]_

**Trabalhos futuros:**
- In future work, we plan to develop a probabilistic model of the information computed by REALM .  _[conclusao, 11 pontos]_
- We also plan to evaluate the use of non-local context for IE Assessment by integrating document-level modeling techniques (e.g., Latent Dirichlet Allocation).  _[conclusao, 5 pontos]_

Artigos mais parecidos (cosseno TF-IDF): fader11.pdf (0.31), bunescu-acl07.pdf (0.23), N18-3011.pdf (0.17)

---

## How to make words with vectors: Phrase generation in distributional semantics

- Arquivo: P14-1059.pdf | Ano: 2014 | Páginas: 10
- Seções: Abstract, 1 Introduction, 2 Related work, 3 General framework, 4 Evaluation setting, 5 Noun phrase generation, 6 Noun phrase translation, 7 Generation confidence and generation, 8 Conclusion, Acknowledgments, References
- Referências: 32 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2830
- 10 termos mais citados: vector (97), phrase (76), generation (69), word (42), function (29), composition (29), noun (28), paraphrase (27), decomposition (24), semantic (23)
- Palavras-chave (TF-IDF): vector, phrase, generation, decomposition, composition, paraphrase, noun, compose

**Objetivo:**
- We introduce the problem of generation in distributional semantics: Given a distributional vector representing some meaning, how can we generate the phrase that best expresses that meaning?  _[resumo, 5 pontos]_
- In this paper, we introduce a more direct approach to phrase generation, inspired by the work in compositional distributional semantics.  _[introducao, 5 pontos]_

**Problema:**
- However, the link between language and meaning is, obviously, bidirectional: As message recipients we are exposed to a linguistic expression and we must compute its meaning (the synthesis problem).  _[introducao, 6 pontos]_
- This is however unfeasible for larger expressions: Given n vocabulary elements, this approach requires checking nk phrases of length k.  _[introducao, 5 pontos]_

**Método:**
- We test this in a monolingual scenario (paraphrase generation) as well as in a cross-lingual setting (translation by synthesizing adjective-noun phrase vectors in English and generating the equivalent expressions in Italian).  _[resumo, 4 pontos]_
- In short, we revert the composition process and we propose a framework of data-induced, syntax-dependent functions that decompose a single vector into a vector sequence.  _[introducao, 7 pontos]_
- We proposed a simple but effective approach to reverting the composition process to obtain meaningful reformulations of phrases through a synthesis-generation process.  _[conclusao, 4 pontos]_

**Contribuições:**
- From a more theoretical point of view, our work fills an important gap in distributional semantics, making it a bidirectional theory of the connection between language and meaning.  _[conclusao, 4 pontos]_

**Trabalhos futuros:**
- In future work we will exploit the correlation between confidence and quality for the purpose of eliminating this assumption.  _[outra, 5 pontos]_
- For future work we would like to experiment with more complex models for (de-)composition in order to improve the performance on the tasks we used in this paper.  _[conclusao, 8 pontos]_
- Following this, we would like to extend the framework to handle arbitrary phrases, including making (confidencebased) choices on the syntactic structure of the phrase to be generated, which we have assumed to be given throughout this paper.  _[conclusao, 5 pontos]_

Artigos mais parecidos (cosseno TF-IDF): fader11.pdf (0.18), mooney05.pdf (0.15), dyer12.pdf (0.14)

---

## Efficient Parsing of Syntactic and Semantic Dependency Structures

- Arquivo: bohnet09.pdf | Ano: 2009 | Páginas: 6
- Seções: Abstract, 1 Introduction, 2 Parsing Algorithm, 3 Labeled Dependency Parsing, 4 Non-Projective Dependency Parsing, 5 Learning Framework, 6 Selected Parsing Features, 7 Implementation Aspects, 8 Semantic Role Labeling, 9 Conclusion, Acknowledgments, References
- Referências: 20 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2704
- 10 termos mais citados: dir (47), parse (45), feature (41), arg (38), algorithm (33), label (31), score (31), edge (27), dependency (25), tree (25)
- Palavras-chave (TF-IDF): dir, arg, parse, d-pos, h-pos, edge, feature, a-pos

**Objetivo:**
- In this paper, we describe our system for the 2009 CoNLL shared task for joint parsing of syntactic and semantic dependency structures of multiple languages.  _[resumo, 5 pontos]_

**Problema:**
- (não encontrado)

**Método:**
- Our system combines and implements efficient parsing techniques to get a high accuracy as well as very good parsing and training time.  _[resumo, 4 pontos]_
- Our system uses the first approach since we saw better chance to improve the parsing speed and additionally, the MST had so far slightly better parsing results.  _[introducao, 4 pontos]_
- For the task of semantic role labeling, we adopted a pipeline architecture where we used for each step the same learning technique (SVM) since we opted for the possibility to build a synchronous combined parser with one score function.  _[introducao, 5 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- Therefore, a possible further accuracy and parsing speed improvement would be to select different features sets for different languages or to leave out some features.  _[conclusao, 3 pontos]_

Artigos mais parecidos (cosseno TF-IDF): mooney05.pdf (0.19), dyer12.pdf (0.18), N18-3011.pdf (0.12)

---

## Learning to Extract Relations from the Web using Minimal Supervision

- Arquivo: bunescu-acl07.pdf | Ano: 2007 | Páginas: 8
- Seções: Abstract, 1 Introduction, 2 Problem Description, 3 Multiple Instance Learning, 4 Relation Extraction Kernel, 5 Two Types of Bias, 6 MIL Relation Extraction Datasets, 7 Experimental Evaluation, 8 Future Work, 9 Related Work, 10 Conclusion, Acknowledgments, References
- Referências: 16 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2595
- 10 termos mais citados: bag (55), sentence (52), relation (46), word (40), positive (34), extraction (32), pair (29), contain (29), instance (26), train (25)
- Palavras-chave (TF-IDF): bag, kernel, positive, relation, sentence, subsequence, mil, google

**Objetivo:**
- We present a new approach to relation extraction that requires only a handful of training examples.  _[resumo, 5 pontos]_
- In this paper, we introduce a supervised learning approach to RE that requires only a handful of training examples and uses the web as a corpus.  _[introducao, 5 pontos]_

**Problema:**
- Supervised learning has been shown to be effective for RE (Zelenko et al., 2003; Culotta and Sorensen, 2004; Bunescu and Mooney, 2006); however, annotating large corpora with examples of the relations to be extracted is expensive and tedious.  _[introducao, 5 pontos]_
- Although not all of the sentences for positive pairs will state the desired relationship, many of them will.  _[introducao, 4 pontos]_

**Método:**
- We extend an existing relation extraction method to handle this weaker form of supervision, and present experimental results demonstrating that our approach can reliably extract relations from web documents.  _[resumo, 4 pontos]_
- We have extended an existing approach to relation extraction using support vector machines and string kernels (Bunescu and Mooney, 2006) to handle this weaker form of MIL supervision.  _[introducao, 5 pontos]_
- We have extended an existing relation extraction kernel to learn in this setting and to resolve problems caused by the minimal supervision provided.  _[conclusao, 4 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- An interesting potential application of our approach is a web relation-extraction system similar to Google Sets, in which the user provides only a handful of pairs of entities known to exhibit or not to exhibit a particular relation, and the system is used to find other pairs of entities exhibiting the same relation.  _[conclusao, 7 pontos]_
- We are also investigating methods for reducing Type II bias, either by modifying the word weights, or by integrating an appropriate measure of word distribution across positive bags directly in the objective function for the MIL problem.  _[conclusao, 7 pontos]_

Artigos mais parecidos (cosseno TF-IDF): P07-1088.pdf (0.23), fader11.pdf (0.22), N18-3011.pdf (0.21)

---

## Joint Feature Selection in Distributed Stochastic Learning for Large-Scale Discriminative Training in SMT

- Arquivo: dyer12.pdf | Ano: 2012 | Páginas: 11
- Seções: Abstract, 1 Introduction, 2 Related Work, 3 Local Features for Synchronous CFGs, 4 Joint Feature Selection in Distributed, 5 Experiments, 6 Discussion, Acknowledgments, References
- Referências: 47 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2731
- 10 termos mais citados: feature (96), algorithm (51), train (47), rule (43), data (40), learn (29), shard (29), translation (26), weight (24), tune (20)
- Palavras-chave (TF-IDF): feature, shard, rule, algorithm, smt, train, translation, shape

**Objetivo:**
- The goal of this paper is to show that this common wisdom can also be brought to bear upon SMT.  _[resumo, 4 pontos]_
- We present experiments on learning on 1.5 million training sentences, and show significant improvements over tuning discriminative models on small development sets.  _[resumo, 5 pontos]_

**Problema:**
- Features may be lexicalized and sparse, non-local and overlapping, or be designed to generalize beyond surface statistics by incorporating part-of-speech or syntactic labels.  _[introducao, 4 pontos]_
- Another possible reason why large training data did not yet show the expected improvements in discriminative SMT is a special overfitting problem of current popular online learning techniques.  _[introducao, 6 pontos]_

**Método:**
- We deploy local features for SCFG-based SMT that can be read off from rules at runtime, and present a learning algorithm that applies l1/l2 regularization for joint feature selection over distributed stochastic learning processes.  _[resumo, 5 pontos]_
- We deploy generic features for SCFG-based SMT that can efficiently be read off from rules at runtime.  _[introducao, 5 pontos]_
- Another crucial ingredient of our approach is a combination of parallelized stochastic learning with feature selection inspired by multi-task learning.  _[introducao, 5 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- In future work, we would like to investigate more sophisticated features, better learners, and in general improve the components of our system that have been neglected in the current investigation of relative improvements by scaling the size of data and feature sets.  _[conclusao, 11 pontos]_
- Ultimately, since our algorithms are inspired by multi-task learning, we would like to apply them to scenarios where a natural definition of tasks is given.  _[conclusao, 5 pontos]_

Artigos mais parecidos (cosseno TF-IDF): roark13.pdf (0.21), bohnet09.pdf (0.18), P14-1059.pdf (0.14)

---

## Identifying Relations for Open Information Extraction

- Arquivo: fader11.pdf | Ano: 2011 | Páginas: 12
- Seções: Abstract, 1 Introduction and Motivation, 2 Previous Work, 3 Constraints on Relation Phrases, 4 REVERB, 5 Experiments, 6 Conclusions and Future Work, Acknowledgments, References
- Referências: 30 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2475
- 10 termos mais citados: relation (125), extraction (112), phrase (100), reverb (97), constraint (57), text (55), system (52), runner (51), sentence (48), precision (36)
- Palavras-chave (TF-IDF): reverb, relation, phrase, extraction, runner, woe, constraint, text

**Objetivo:**
- This paper shows that the output of state-ofthe-art Open IE systems is rife with uninformative and incoherent extractions.  _[resumo, 4 pontos]_
- To overcome these problems, we introduce two simple syntactic and lexical constraints on binary relations expressed by verbs.  _[resumo, 3 pontos]_

**Problema:**
- For example, consider the sentence "Faust made a deal with the devil." Previous Open IE systems return the uninformative (Faust, made, a deal) instead of (Faust, made a deal with, the devil).  _[introducao, 5 pontos]_
- Although the syntactic constraint significantly reduces incoherent and uninformative extractions, it allows overly-specific relation phrases such as is offering only modest greenhouse gas reduction targets at.  _[introducao, 7 pontos]_

**Método:**
- We implemented the constraints in the REVERB Open IE system, which more than doubles the area under the precision-recall curve relative to previous extractors such as TEXT RUNNER and WOE pos.  _[resumo, 5 pontos]_
- In summary, this paper articulates two simple but surprisingly powerful constraints on how binary relationships are expressed via verbs in English sentences, and implements them in the REVERB Open IE system.  _[introducao, 3 pontos]_

**Contribuições:**
- We have identified and analyzed the problems of incoherent and uninformative extractions for Open IE systems, and shown their prevalence for systems such as TEXT RUNNER and WOE.  _[conclusao, 6 pontos]_
- We articulated general, easy-to-enforce constraints on binary, verb-based relation phrases in English that ameliorate these problems and yield richer and more informative relations (see, for example, Table 2).  _[conclusao, 6 pontos]_
- Based on these constraints, we designed, implemented, and evaluated the REVERB extractor, which substantially outperforms previous Open IE systems in both recall and precision.  _[conclusao, 6 pontos]_
- We make REVERB and the data used in our experiments available to the research community.  _[conclusao, 6 pontos]_

**Trabalhos futuros:**
- In future work, we plan to explore utilizing our constraints to improve the performance of learned CRF models.  _[conclusao, 13 pontos]_
- The error analysis in Section 5.2 also suggests natural directions for future work.  _[conclusao, 7 pontos]_

Artigos mais parecidos (cosseno TF-IDF): P07-1088.pdf (0.31), bunescu-acl07.pdf (0.22), P14-1059.pdf (0.18)

---

## A Statistical Semantic Parser that Integrates Syntax and Semantics

- Arquivo: mooney05.pdf | Ano: 2005 | Páginas: 8
- Seções: Abstract, 1 Introduction, 2 Target MRL's, 3 Semantic Parsing Framework, 4 Corpus Annotation, 5 Integrated Parsing Model, 6 Experimental Evaluation, 7 Related Work, 8 Conclusion, 9 Acknowledgements, References
- Referências: 17 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2711
- 10 termos mais citados: semantic (86), syntactic (38), generate (37), label (36), player (35), parse (27), word (27), sentence (25), node (25), sapt (23)
- Palavras-chave (TF-IDF): semantic, player, sapt, scissor, syntactic, node, parse, geoquery

**Objetivo:**
- We introduce a learning semantic parser, SCISSOR , that maps natural-language sentences to a detailed, formal, meaningrepresentation language.  _[resumo, 5 pontos]_
- We present experimental results demonstrating that SCISSOR produces more accurate semantic representations than several previous approaches.  _[resumo, 5 pontos]_

**Problema:**
- (não encontrado)

**Método:**
- We evaluate the system in two domains, a natural-language database interface and an interpreter for coaching instructions in robotic soccer.  _[resumo, 4 pontos]_
- We present an approach based on a statistical parser that generates a semantically augmented parse tree (SAPT), in which each internal node includes both a syntactic and semantic label.  _[introducao, 6 pontos]_
- We augment Collins' head-driven model 2 (Collins, 1997) to incorporate a semantic label on each internal node.  _[introducao, 4 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- (não encontrado)

Artigos mais parecidos (cosseno TF-IDF): bohnet09.pdf (0.19), P14-1059.pdf (0.15), N18-3011.pdf (0.14)

---

## Discriminative Joint Modeling of Lexical Variation and Acoustic Confusion for Automated Narrative Retelling Assessment

- Arquivo: roark13.pdf | Ano: 2013 | Páginas: 10
- Seções: Abstract, 1 Introduction, 2 Wechsler Logical Memory (WLM) task, 3 Unsupervised generative automated, 4 Supervised discriminative automated, 5 Combining tagging and alignment, 6 Experimental evaluations, 7 Summary and discussion, Acknowledgments, References
- Referências: 25 (formato autor-ano)
- Perplexidade do modelo de bigramas: 2790
- 10 termos mais citados: model (120), feature (67), word (64), element (56), tag (54), story (50), retell (47), asr (44), train (43), transcript (41)
- Palavras-chave (TF-IDF): asr, model, story, transcript, element, feature, retell, tag

**Objetivo:**
- In this paper, we present and evaluate the use of word tagging models for this task, in contrast to just using automatic (unsupervised) word-alignment methods.  _[introducao, 5 pontos]_
- We present results under a range of experimental conditions, including: variously adapting the ASR models to the domain; using maximum entropy models rather than CRFs; differing tagsets (BIO versus IO); and with varying degrees of supervision.  _[introducao, 5 pontos]_

**Problema:**
- Automatically assessing the fidelity of a retelling to the original narrative - a task of growing clinical importance - is challenging, given extensive paraphrasing during retelling along with cascading automatic speech recognition (ASR) errors.  _[resumo, 4 pontos]_
- Although this presents a challenge for ASR, part of the goal of our work is to demonstrate the robustness of our methods to noisy audio.  _[resultados, 5 pontos]_

**Método:**
- We present a word tagging approach using conditional random fields (CRFs) that allows a diversity of features to be considered during inference, including some capturing acoustic confusions encoded in word confusion networks.  _[resumo, 6 pontos]_
- We evaluate the approach under several scenarios, including both supervised and unsupervised training, the latter achieved by training on the output of a baseline automatic word-alignment model.  _[resumo, 6 pontos]_
- The approach is general enough to allow tagging of word confusion networks derived from lattices, thus allowing us to explore the utility of such representations to achieve robustness.  _[introducao, 4 pontos]_

**Contribuições:**
- (não encontrado)

**Trabalhos futuros:**
- In future work, we would like to investigate two questions left open by these results.  _[conclusao, 14 pontos]_
- First, word-alignment models can be extended to process ASR lattices or word confusion networks as part of the unsupervised alignment learning algorithm, and incorporated into our approach.  _[conclusao, 5 pontos]_

Artigos mais parecidos (cosseno TF-IDF): dyer12.pdf (0.21), 2020.acl-main.207.pdf (0.16), N18-3011.pdf (0.16)
