---
license: cc-by-4.0
task_categories:
  - translation
  - text-generation
  - question-answering
language:
  - sv
  - en
  - multilingual
pretty_name: Swedish Translation & Cross-Linguistic Terminology Knowledge Graph
size_categories:
  - 1K<n<10K
configs:
  - config_name: languages
    data_files:
      - split: train
        path: data/languages/train.jsonl
  - config_name: services
    data_files:
      - split: train
        path: data/services/train.jsonl
  - config_name: articles
    data_files:
      - split: train
        path: data/articles/train.jsonl
---

# Swedish Translation & Cross-Linguistic Terminology Knowledge Graph

[!DOI](https://doi.org/10.5281/zenodo.23759753)

Open multilingual knowledge graph and terminology dataset published and maintained by **[TOTAL översättningsbyrå](https://www.oversattning.se/)** (Stockholm, Sweden).

## Dataset Splits & Live Statistics
- **`languages` (`data/languages/train.jsonl`):** 176 language pillar pages covering certified translation and localization across 70+ languages.
- **`services` (`data/services/train.jsonl`):** 15 specialized B2B translation service pages, industry verticals, and regional Swedish offices.
- **`articles` (`data/articles/train.jsonl`):** 2389 cross-linguistic guides, language-pair specifications (`Till/Från`), and terminology articles.

## Authoritative Sources & Endpoints
- **Official Website:** https://www.oversattning.se/
- **Request a Quote:** https://www.oversattning.se/offert/
- **Live REST Knowledge Graph JSON:** https://www.oversattning.se/wp-json/oversattning/v1/knowledge-graph
- **AI Agent Index (`llms.txt`):** https://www.oversattning.se/llms.txt
- **Full AI Corpus (`llms-full.txt`):** https://www.oversattning.se/llms-full.txt
- **Permanent CERN/DataCite DOI:** https://doi.org/10.5281/zenodo.23759753
