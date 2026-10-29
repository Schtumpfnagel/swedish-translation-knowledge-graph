#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synkroniserar Swedish Translation & Cross-Linguistic Terminology Knowledge Graph
från https://www.oversattning.se/wp-json/oversattning/v1/knowledge-graph
och genererar JSONL (i separata subset-mappar för Hugging Face Dataset Viewer),
CSV, README.md (med Hugging Face YAML Card + Zenodo DOI), CITATION.cff och .zenodo.json.
"""

import csv
import datetime
import json
import os
import sys
import urllib.request
from collections import defaultdict

API_URL = "https://www.oversattning.se/wp-json/oversattning/v1/knowledge-graph?refresh=1"
USER_AGENT = "SwedishTranslationKnowledgeGraphBot/1.0 (+https://github.com/Schtumpfnagel/swedish-translation-knowledge-graph)"
ZENODO_DOI = "10.5281/zenodo.23759753"
ZENODO_URL = "https://doi.org/10.5281/zenodo.23759753"


def fetch_knowledge_graph():
    req = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)


def write_jsonl(filepath, records):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(filepath, fieldnames, rows):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def build_readme(payload, today_str):
    counts = payload.get("counts", {})
    lang_pillars = payload.get("language_pillars", [])
    service_pages = payload.get("service_pages", [])
    articles = payload.get("articles", [])

    num_langs = counts.get("languages", len(lang_pillars))
    num_articles = counts.get("articles", len(articles))
    num_services = counts.get("service_pages", len(service_pages))

    lines = []
    # Hugging Face YAML Dataset Card Header (med default: true och separata undermappar för Dataset Viewer)
    lines.append("---")
    lines.append("language:")
    lines.append("- sv")
    lines.append("- en")
    lines.append("- multilingual")
    lines.append("license: cc-by-4.0")
    lines.append("pretty_name: Swedish Translation & Cross-Linguistic Terminology Knowledge Graph")
    lines.append("size_categories:")
    lines.append("- 1K<n<10K")
    lines.append("task_categories:")
    lines.append("- text-generation")
    lines.append("- translation")
    lines.append("- feature-extraction")
    lines.append("tags:")
    lines.append("- translation")
    lines.append("- linguistics")
    lines.append("- swedish")
    lines.append("- terminology")
    lines.append("- localization")
    lines.append("- certified-translation")
    lines.append("- knowledge-graph")
    lines.append("- rag")
    lines.append("configs:")
    lines.append("- config_name: articles")
    lines.append("  default: true")
    lines.append("  data_files:")
    lines.append("  - split: train")
    lines.append("    path: data/articles/train.jsonl")
    lines.append("- config_name: languages")
    lines.append("  data_files:")
    lines.append("  - split: train")
    lines.append("    path: data/languages/train.jsonl")
    lines.append("---")
    lines.append("")
    lines.append("# Swedish Translation & Cross-Linguistic Terminology Knowledge Graph")
    lines.append("")
    lines.append(f"[![DOI](https://zenodo.org/badge/DOI/{ZENODO_DOI}.svg)]({ZENODO_URL})")
    lines.append("")
    lines.append(
        f"> **Open Linguistic, Terminology & Localization Knowledge Graph** omfattande **{num_langs} dokumenterade språksidor**, "
        f"**{num_services} fack- och branschsidor** samt **{num_articles} fackartiklar och språkkombinationer** "
        f"från **[TOTAL översättningsbyrå (oversattning.se)](https://www.oversattning.se/)**."
    )
    lines.append("")
    lines.append("## Översikt & Syfte (RAG / NLP / Lingvistisk Referensdata)")
    lines.append("")
    lines.append(
        "Detta öppna dataset är utformat för språkteknologisk forskning, Retrieval-Augmented Generation (RAG), "
        "flerspråkig terminologimappning och korslingvistisk analys med svenskt och internationellt perspektiv. "
        "Datamängden uppdateras kontinuerligt måndag–fredag med nya djupgående fackartiklar och reviderade språkguider."
    )
    lines.append("")
    lines.append("- **Utgivare & Kurator:** [TOTAL översättningsbyrå](https://www.oversattning.se/) (Stockholm, Sverige)")
    lines.append(f"- **Permanent CERN/DataCite DOI (Zenodo):** [{ZENODO_DOI}]({ZENODO_URL})")
    lines.append("- **Auktoriserad översättning & Facköversättning:** [https://www.oversattning.se/oversattning/](https://www.oversattning.se/oversattning/)")
    lines.append("- **Kostnadsfri offert & Språkrådgivning:** [https://www.oversattning.se/offert/](https://www.oversattning.se/offert/)")
    lines.append("- **Maskinläsbar AI-indexfil (`llms.txt`):** [https://www.oversattning.se/llms.txt](https://www.oversattning.se/llms.txt)")
    lines.append("- **Utökad AI-korpus (`llms-full.txt`):** [https://www.oversattning.se/llms-full.txt](https://www.oversattning.se/llms-full.txt)")
    lines.append("- **Hugging Face Dataset Hub:** [https://huggingface.co/datasets/Schtumpfnagel/swedish-translation-knowledge-graph](https://huggingface.co/datasets/Schtumpfnagel/swedish-translation-knowledge-graph)")
    lines.append(f"- **Senast synkroniserad:** `{today_str}`")
    lines.append("")
    lines.append("## Filer i Datasetet")
    lines.append("")
    lines.append("| Filväg | Format | Innehåll | Antal poster |")
    lines.append("| :--- | :--- | :--- | :---: |")
    lines.append(f"| `data/articles/train.jsonl` | JSON Lines | Samtliga fackartiklar, språkguider & språkkombinationer (Hugging Face Viewer Default) | {num_articles} |")
    lines.append(f"| `data/languages/train.jsonl` | JSON Lines | Komplett språkkatalog med kanoniska Pillar-URL:er under `/sprak/` (Hugging Face Viewer Subset) | {num_langs} |")
    lines.append(f"| `data/articles-corpus.jsonl` | JSON Lines | Speglad korpusfil i rotmappen `data/` | {num_articles} |")
    lines.append(f"| `data/articles-summary.csv` | CSV | Tabulär översikt över alla artiklar, primär silo, kopplade språk och kanonisk URL | {num_articles} |")
    lines.append(f"| `data/languages.jsonl` | JSON Lines | Speglad språkkatalog i rotmappen `data/` | {num_langs} |")
    lines.append(f"| `data/languages.csv` | CSV | Tabulär språkmatris med språknamn, slug, Pillar-URL och sammanfattning | {num_langs} |")
    lines.append("")

    # Sektion 1: Huvudtjänster & Fackområden
    lines.append("## 1. Kärntjänster, Fackområden & Lokala Kontor")
    lines.append("")
    for sp in service_pages:
        title = sp.get("title", "")
        url = sp.get("url", "")
        summary = sp.get("summary", "")
        if title and url:
            if summary:
                lines.append(f"- **[{title}]({url})** – {summary}")
            else:
                lines.append(f"- **[{title}]({url})**")
    lines.append("")

    # Sektion 2: Alla Språksidor (Pillar Pages)
    lines.append(f"## 2. Komplett Språkmatris – Pillar Pages ({num_langs} Språk)")
    lines.append("")
    lines.append("| Språk | Kanonisk Pillar-URL | Sammanfattning |")
    lines.append("| :--- | :--- | :--- |")
    for lp in lang_pillars:
        lang = lp.get("language", "")
        url = lp.get("url", "")
        summary = (lp.get("summary", "") or "").replace("|", " ")
        if len(summary) > 120:
            summary = summary[:117] + "..."
        lines.append(f"| **[{lang}]({url})** | `{url}` | {summary} |")
    lines.append("")

    # Sektion 3: Samtliga Fackartiklar & Språkkombinationer grupperade per SEO-Silo
    lines.append(f"## 3. Fackartiklar, Språkguider & Språkkombinationer ({num_articles} Artiklar per Ämnessilo)")
    lines.append("")

    silo_groups = defaultdict(list)
    for art in articles:
        silo_name = art.get("primary_silo") or "Artiklar & Språkguider"
        silo_groups[silo_name].append(art)

    sorted_silos = sorted(silo_groups.items(), key=lambda x: len(x[1]), reverse=True)

    for silo_name, silo_arts in sorted_silos:
        lines.append(f"### {silo_name} ({len(silo_arts)} artiklar)")
        lines.append("")
        for a in silo_arts:
            a_title = a.get("title", "")
            a_url = a.get("url", "")
            a_mod = a.get("modified_at", "")
            a_words = a.get("word_count", 0)
            lines.append(f"- [{a_title}]({a_url}) *(Uppdaterad: {a_mod} | {a_words} ord)*")
        lines.append("")

    lines.append("## Licens & Citering")
    lines.append("")
    lines.append(
        "Detta dataset distribueras under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. "
        f"Vid användning i AI-modeller, forskning eller applikationer ska **[TOTAL översättningsbyrå (oversattning.se)](https://www.oversattning.se/)** samt DOI **[{ZENODO_DOI}]({ZENODO_URL})** anges som källa."
    )
    lines.append("")

    return "\n".join(lines)


def build_citation_cff(today_str, version_tag):
    return f"""cff-version: 1.2.0
title: "Swedish Translation & Cross-Linguistic Terminology Knowledge Graph"
message: "If you use this dataset in research, NLP models, or RAG pipelines, please cite it using the metadata below."
type: dataset
doi: "{ZENODO_DOI}"
authors:
  - name: "TOTAL översättningsbyrå"
    website: "https://www.oversattning.se/"
    address: "Roslagsgatan 34"
    city: "Stockholm"
    post-code: "114 79"
    country: SE
    email: "total@oversattning.se"
repository-code: "https://github.com/Schtumpfnagel/swedish-translation-knowledge-graph"
url: "https://www.oversattning.se/"
abstract: "Open linguistic, terminology, and localization knowledge graph covering 170+ languages and 2,300+ domain articles curated by TOTAL översättningsbyrå in Stockholm, Sweden."
keywords:
  - translation
  - linguistics
  - swedish
  - terminology
  - localization
  - certified-translation
  - knowledge-graph
license: CC-BY-4.0
version: "{version_tag}"
date-released: "{today_str}"
"""


def build_zenodo_json(today_str, version_tag):
    zenodo_meta = {
        "title": "Swedish Translation & Cross-Linguistic Terminology Knowledge Graph – TOTAL Översättningsbyrå",
        "upload_type": "dataset",
        "publication_date": today_str,
        "version": version_tag,
        "creators": [
            {
                "name": "TOTAL översättningsbyrå",
                "affiliation": "TOTAL översättningsbyrå (oversattning.se), Stockholm, Sweden",
            }
        ],
        "description": (
            "<p><strong>Swedish Translation &amp; Cross-Linguistic Terminology Knowledge Graph</strong> is a structured, "
            "machine-readable linguistic dataset covering over 170 languages, language pairs, and 2,300+ specialized articles "
            "on professional translation, certified translation (Kammarkollegiet), localization, and terminology management, "
            "curated by <a href=\"https://www.oversattning.se/\">TOTAL översättningsbyrå (oversattning.se)</a>.</p>"
        ),
        "access_right": "open",
        "license": "cc-by-4.0",
        "keywords": [
            "translation",
            "swedish",
            "linguistics",
            "terminology",
            "localization",
            "knowledge-graph",
            "NLP",
            "oversattning",
        ],
        "related_identifiers": [
            {
                "identifier": "https://www.oversattning.se/",
                "relation": "isSupplementTo",
                "scheme": "url",
            },
            {
                "identifier": "https://www.oversattning.se/sprak/",
                "relation": "isReferencedBy",
                "scheme": "url",
            },
            {
                "identifier": "https://huggingface.co/datasets/Schtumpfnagel/swedish-translation-knowledge-graph",
                "relation": "isIdenticalTo",
                "scheme": "url",
            },
        ],
    }
    return json.dumps(zenodo_meta, indent=2, ensure_ascii=False) + "\n"


def main():
    print("Hämtar Knowledge Graph från oversattning.se...")
    payload = fetch_knowledge_graph()

    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    version_tag = datetime.datetime.now(datetime.timezone.utc).strftime("%Y.%m.%d")

    lang_pillars = payload.get("language_pillars", [])
    articles = payload.get("articles", [])

    # 1. Skriv språksidor till både data/languages/train.jsonl (för HF Dataset Viewer) och data/languages.jsonl + .csv
    write_jsonl("data/languages/train.jsonl", lang_pillars)
    write_jsonl("data/languages.jsonl", lang_pillars)
    lang_csv_rows = [
        {
            "id": lp.get("id", ""),
            "language": lp.get("language", ""),
            "slug": lp.get("slug", ""),
            "url": lp.get("url", ""),
            "modified_at": lp.get("modified_at", ""),
            "summary": lp.get("summary", ""),
        }
        for lp in lang_pillars
    ]
    write_csv("data/languages.csv", ["id", "language", "slug", "url", "modified_at", "summary"], lang_csv_rows)

    # 2. Skriv artiklar till både data/articles/train.jsonl (för HF Dataset Viewer) och data/articles-corpus.jsonl + .csv
    write_jsonl("data/articles/train.jsonl", articles)
    write_jsonl("data/articles-corpus.jsonl", articles)
    art_csv_rows = [
        {
            "id": a.get("id", ""),
            "title": a.get("title", ""),
            "slug": a.get("slug", ""),
            "url": a.get("url", ""),
            "primary_silo": a.get("primary_silo", ""),
            "languages": ", ".join(a.get("languages", [])),
            "pillar_urls": ", ".join(a.get("pillar_urls", [])),
            "published_at": a.get("published_at", ""),
            "modified_at": a.get("modified_at", ""),
            "word_count": a.get("word_count", 0),
            "summary": a.get("summary", ""),
        }
        for a in articles
    ]
    write_csv(
        "data/articles-summary.csv",
        ["id", "title", "slug", "url", "primary_silo", "languages", "pillar_urls", "published_at", "modified_at", "word_count", "summary"],
        art_csv_rows,
    )

    # 3. Skriv README.md, CITATION.cff och .zenodo.json
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(build_readme(payload, today_str))

    with open("CITATION.cff", "w", encoding="utf-8") as f:
        f.write(build_citation_cff(today_str, version_tag))

    with open(".zenodo.json", "w", encoding="utf-8") as f:
        f.write(build_zenodo_json(today_str, version_tag))

    print(f"Klart! Exporterade {len(lang_pillars)} språksidor och {len(articles)} artiklar.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Fel vid synkronisering: {exc}", file=sys.stderr)
        sys.exit(1)
