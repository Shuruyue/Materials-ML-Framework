from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import time
import unicodedata
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".cache" / "openalex"
JSON_OUT = ROOT / "data" / "atlas-sources.json"
JS_OUT = ROOT / "data" / "atlas-sources.js"
CANONICAL_JSON_OUT = ROOT / "data" / "canonical-list.json"
CANONICAL_JS_OUT = ROOT / "data" / "canonical-list.js"
MAILTO = "epochal-papers-atlas@example.com"
MIN_YEAR = 1980
# Papers with publication_year == current year are typically in-press or early-access.
# This is expected and not a data error.
MAX_YEAR = dt.datetime.now(dt.timezone.utc).year
BASE_FILTER = (
    f"from_publication_date:{MIN_YEAR}-01-01,"
    "has_doi:true,is_retracted:false,language:en,"
    "type:article|review|proceedings-article"
)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "by", "for", "from",
    "in", "into", "is", "of", "on", "or", "the", "to", "with",
    "your", "you",
}

# Top-tier venues whose papers are considered high-quality by default.
QUALITY_SOURCE_PATTERNS = tuple(
    pattern.lower()
    for pattern in [
        "nature",
        "science",
        "cell",
        "physical review",
        "pnas",
        "proceedings of the national academy of sciences",
        "chemical reviews",
        "chemical society reviews",
        "joule",
        "energy & environmental science",
        "advanced materials",
        "advanced science",
        "nature materials",
        "nature energy",
        "nature biotechnology",
        "nature methods",
        "nature machine intelligence",
        "nature photonics",
        "nature electronics",
        "nature communications",
        "science advances",
        "nano letters",
        "acs nano",
        "accounts of chemical research",
        "machine learning: science and technology",
        "ieee transactions",
        "ieee journal",
        "ieee conference",
        "acm transactions",
        "communications of the acm",
        "neurips",
        "neural information processing systems",
        "icml",
        "iclr",
        "cvpr",
        "iccv",
        "eccv",
        "aaai",
        "ijcai",
        "acl",
        "emnlp",
        "naacl",
        "sigcomm",
        "sosp",
        "osdi",
        "nsdi",
        "isca",
        "micro",
        "asplos",
        "dac",
        "iedm",
        "isscc",
        "rss",
        "icra",
        "iros",
        "additive manufacturing",
        "journal of power sources",
        "apl materials",
        "materials today",
        "nature chemistry",
        "nature physics",
        "nature nanotechnology",
        "nature medicine",
        "biotechnology",
        "bioinformatics",
        "briefings in bioinformatics",
        "genome biology",
        "genome research",
        "remote sensing",
        "journal of climate",
        "bulletin of the american meteorological society",
        "journal of machine learning research",
        "machine learning",
        "proceedings of the ieee",
        "neural computation",
        "computer networks",
        "applied physics letters",
        "physical review letters",
        "reviews of modern physics",
        "annual review",
        "kdd",
        "sigmod",
        "vldb",
    ]
)

EXCLUDE_TITLE_PATTERNS = tuple(
    pattern.lower()
    for pattern in [
        "corrigendum",
        "erratum",
        "editorial",
        "commentary",
        "retraction",
        "withdrawn",
        "preface",
        "special issue",
        "guest editorial",
        "book review",
        "curriculum",
        "teaching",
        "classroom",
        "survey of students",
        "questionnaire",
        "nursing",
        "psychology",
        "economics",
        "marketing",
        "accounting",
        "law review",
        "covid-19 screening in",
    ]
)

EXCLUDE_VENUE_PATTERNS = tuple(
    pattern.lower()
    for pattern in [
        "international journal of research and engineering",
        "zenodo",
    ]
)

BLOCKLIST_SOURCE_IDS = {
    "W2122465391",  # faux 2018 MapReduce republication
    "W3209398723",  # Zenodo digital-twin duplicate
}

CATEGORY_DEFS = [
    {
        "id": "observability",
        "label": "New observability",
        "description": "Papers that make hidden phenomena measurable, imageable, traceable, or monitorable.",
    },
    {
        "id": "instrument_platform",
        "label": "New instrument or platform",
        "description": "Papers that create reusable experimental, computational, or operational platforms.",
    },
    {
        "id": "representation_modeling",
        "label": "Representation and modeling shift",
        "description": "Papers that change the representation so the problem becomes structurally easier.",
    },
    {
        "id": "search_control",
        "label": "Search, optimization, and control",
        "description": "Papers that reduce discovery cost, improve control, or create adaptive decision loops.",
    },
    {
        "id": "infrastructure_protocols",
        "label": "Shared infrastructure and protocols",
        "description": "Papers that create shared abstractions, datasets, protocols, or system architectures.",
    },
    {
        "id": "substrate_device",
        "label": "New substrate, material, or device",
        "description": "Papers that open a new physical or programmable platform for downstream engineering.",
    },
    {
        "id": "fabrication_process",
        "label": "Fabrication, synthesis, and process route",
        "description": "Papers that make promising phenomena repeatable, manufacturable, or scalable.",
    },
    {
        "id": "scaling_architecture",
        "label": "Scaling architecture",
        "description": "Papers that explain how capability survives larger systems, higher throughput, or tighter constraints.",
    },
    {
        "id": "validation_reproducibility",
        "label": "Validation, trust, and reproducibility",
        "description": "Papers that make claims more reliable, testable, reproducible, or transferable.",
    },
    {
        "id": "cross_domain_transfer",
        "label": "Cross-domain transfer",
        "description": "Papers whose methods or platforms later became productive well beyond the original domain.",
    },
]

CORRIDOR_DEFS = [
    {
        "id": "ai_compute",
        "label": "AI and compute",
        "description": "Learning systems, foundation models, computer vision, scientific AI, and compute abstractions.",
    },
    {
        "id": "systems_networks",
        "label": "Systems and networks",
        "description": "Distributed systems, cloud infrastructure, datacenter protocols, and software platforms.",
    },
    {
        "id": "semiconductors_electronics",
        "label": "Semiconductors and electronics",
        "description": "Transistors, memories, lithography, chip architectures, and electronic device platforms.",
    },
    {
        "id": "photonics_imaging",
        "label": "Photonics, imaging, and sensing",
        "description": "Optics, imaging, metrology, microscopy, sensing, and photonic systems.",
    },
    {
        "id": "robotics_control",
        "label": "Robotics, autonomy, and control",
        "description": "Robotic manipulation, autonomy, control theory, perception, and embodied systems.",
    },
    {
        "id": "materials_energy",
        "label": "Materials, chemistry, and energy",
        "description": "Materials platforms, energy devices, catalysis, chemical systems, and discovery infrastructure.",
    },
    {
        "id": "biotech_programmable_biology",
        "label": "Biotech and programmable biology",
        "description": "Genome editing, sequencing, synthetic biology, protein engineering, and biological programmability.",
    },
    {
        "id": "quantum_precision",
        "label": "Quantum and precision technology",
        "description": "Quantum information, qubit platforms, precision metrology, and sensing.",
    },
    {
        "id": "manufacturing_cyberphysical",
        "label": "Manufacturing and cyber-physical systems",
        "description": "Industrial process control, digital twins, self-driving labs, and operational intelligence.",
    },
    {
        "id": "climate_earth_space",
        "label": "Climate, Earth, space, and scientific computing",
        "description": "Climate systems, Earth observation, scientific simulation, and space technologies.",
    },
]

# ── Manual anchors: truly epochal papers (Nobel-calibre, foundational inventions) ──
# These are included regardless of OpenAlex harvesting because they are
# historically indispensable and define what "epochal" means.

MANUAL_SOURCES = [
    # ── AI / Deep Learning Foundations ──
    {
        "id": "manual-lenet-cnn",
        "title": "Gradient-based learning applied to document recognition",
        "year": 1998,
        "type": "manual",
        "venue": "Proceedings of the IEEE",
        "authors": "Yann LeCun, Léon Bottou, Yoshua Bengio, Patrick Haffner",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1109/5.726791",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["convolutional neural network"],
        "selection_score": 195.0,
        "note": "Foundational CNN architecture paper. Introduced LeNet and the convolutional-pooling-dense pipeline that all modern vision models descend from.",
    },
    {
        "id": "manual-lstm",
        "title": "Long Short-Term Memory",
        "year": 1997,
        "type": "manual",
        "venue": "Neural Computation",
        "authors": "Sepp Hochreiter, Jürgen Schmidhuber",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1162/neco.1997.9.8.1735",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["long short-term memory"],
        "selection_score": 194.0,
        "note": "Invented the LSTM gated recurrent cell, solving the vanishing gradient problem and enabling modern sequence modelling.",
    },
    {
        "id": "manual-svm",
        "title": "Support-vector networks",
        "year": 1995,
        "type": "manual",
        "venue": "Machine Learning",
        "authors": "Corinna Cortes, Vladimir Vapnik",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1007/BF00994018",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["support vector machine"],
        "selection_score": 192.0,
        "note": "Introduced the support vector machine, the dominant classifier before deep learning and still widely used in science and engineering.",
    },
    {
        "id": "manual-pagerank",
        "title": "The anatomy of a large-scale hypertextual Web search engine",
        "year": 1998,
        "type": "manual",
        "venue": "Computer Networks",
        "authors": "Sergey Brin, Lawrence Page",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1016/S0169-7552(98)00110-X",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["systems_networks", "ai_compute"],
        "matched_topics": ["pagerank"],
        "selection_score": 193.0,
        "note": "Introduced PageRank and the architecture of Google. Defined web-scale information retrieval and graph-based ranking.",
    },
    {
        "id": "manual-random-forest",
        "title": "Random Forests",
        "year": 2001,
        "type": "manual",
        "venue": "Machine Learning",
        "authors": "Leo Breiman",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1023/A:1010933404324",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["random forests"],
        "selection_score": 191.0,
        "note": "Introduced the random forest ensemble method. One of the most widely deployed ML algorithms across all of science and industry.",
    },
    {
        "id": "manual-imagenet",
        "title": "ImageNet: A Large-Scale Hierarchical Image Database",
        "year": 2009,
        "type": "manual",
        "venue": "CVPR",
        "authors": "Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, Li Fei-Fei",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1109/CVPR.2009.5206848",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "validation_reproducibility", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["imagenet"],
        "selection_score": 190.0,
        "note": "Created the ImageNet benchmark that catalysed the deep learning revolution. The annual ILSVRC competition reshaped computer vision.",
    },
    {
        "id": "manual-alexnet",
        "title": "ImageNet Classification with Deep Convolutional Neural Networks",
        "year": 2012,
        "type": "manual",
        "venue": "NeurIPS",
        "authors": "Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/3065386",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["deep convolutional neural network"],
        "selection_score": 193.0,
        "note": "AlexNet. Won ILSVRC 2012 by a huge margin using GPU-trained deep CNNs, triggering the modern deep learning era. (Hinton: Nobel Physics 2024)",
    },
    {
        "id": "manual-attention-is-all-you-need",
        "title": "Attention Is All You Need",
        "year": 2017,
        "type": "manual",
        "venue": "NeurIPS",
        "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.1706.03762",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["transformer architecture"],
        "selection_score": 196.0,
        "note": "Introduced the Transformer. The single most consequential architecture paper of the 2010s, underpinning GPT, BERT, and virtually all foundation models.",
    },
    {
        "id": "manual-bert",
        "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "year": 2018,
        "type": "manual",
        "venue": "NAACL",
        "authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.18653/v1/N19-1423",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["bert pre-training of deep bidirectional transformers"],
        "selection_score": 188.0,
        "note": "Established masked-language pretraining as the dominant NLP paradigm and showed that deep bidirectional context dramatically improves all downstream tasks.",
    },
    {
        "id": "manual-gan",
        "title": "Generative Adversarial Nets",
        "year": 2014,
        "type": "manual",
        "venue": "NeurIPS",
        "authors": "Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.1406.2661",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["generative adversarial network"],
        "selection_score": 192.0,
        "note": "Introduced the GAN framework for implicit generative modelling. Opened entirely new directions in image synthesis, domain adaptation, and data augmentation.",
    },
    {
        "id": "manual-word2vec",
        "title": "Efficient Estimation of Word Representations in Vector Space",
        "year": 2013,
        "type": "manual",
        "venue": "ICLR",
        "authors": "Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.1301.3781",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["word embeddings"],
        "selection_score": 190.0,
        "note": "Introduced Word2Vec. Demonstrated that distributed word representations encode semantic relationships, launching the era of pre-trained embeddings.",
    },
    {
        "id": "manual-batch-norm",
        "title": "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift",
        "year": 2015,
        "type": "manual",
        "venue": "ICML",
        "authors": "Sergey Ioffe, Christian Szegedy",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.1502.03167",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "scaling_architecture"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["batch normalization"],
        "selection_score": 186.0,
        "note": "Introduced batch normalization, enabling much deeper and faster-converging networks. A standard component of virtually every modern deep architecture.",
    },
    {
        "id": "manual-adam",
        "title": "Adam: A Method for Stochastic Optimization",
        "year": 2015,
        "type": "manual",
        "venue": "ICLR",
        "authors": "Diederik P. Kingma, Jimmy Ba",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.1412.6980",
        "openalex_url": None,
        "category_ids": ["search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["adam optimizer"],
        "selection_score": 188.0,
        "note": "Introduced the Adam optimizer, combining adaptive learning rates with momentum. The most widely used optimizer in deep learning.",
    },
    {
        "id": "manual-resnet",
        "title": "Deep Residual Learning for Image Recognition",
        "year": 2016,
        "type": "manual",
        "venue": "CVPR",
        "authors": "Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1109/CVPR.2016.90",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["residual network"],
        "selection_score": 192.0,
        "note": "Introduced residual connections (skip connections), enabling training of 100+ layer networks. ResNet won ILSVRC 2015 and became a universal backbone.",
    },
    {
        "id": "manual-unet",
        "title": "U-Net: Convolutional Networks for Biomedical Image Segmentation",
        "year": 2015,
        "type": "manual",
        "venue": "MICCAI",
        "authors": "Olaf Ronneberger, Philipp Fischer, Thomas Brox",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1007/978-3-319-24574-4_28",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute", "biotech_programmable_biology"],
        "matched_topics": ["u-net segmentation"],
        "selection_score": 187.0,
        "note": "Introduced U-Net encoder-decoder with skip connections for semantic segmentation. Became the default architecture across biomedical imaging and beyond.",
    },
    {
        "id": "manual-xgboost",
        "title": "XGBoost: A Scalable Tree Boosting System",
        "year": 2016,
        "type": "manual",
        "venue": "KDD",
        "authors": "Tianqi Chen, Carlos Guestrin",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/2939672.2939785",
        "openalex_url": None,
        "category_ids": ["search_control", "infrastructure_protocols", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["xgboost"],
        "selection_score": 186.0,
        "note": "XGBoost. The dominant tabular ML system. Won nearly every Kaggle competition for years and remains the standard for structured data in industry.",
    },
    {
        "id": "manual-gpt3",
        "title": "Language Models are Few-Shot Learners",
        "year": 2020,
        "type": "manual",
        "venue": "NeurIPS",
        "authors": "Tom B. Brown, Benjamin Mann, Nick Ryder, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.2005.14165",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["few-shot language models"],
        "selection_score": 190.0,
        "note": "GPT-3. Demonstrated that scaling language models to 175B parameters unlocks in-context learning and few-shot capabilities across tasks.",
    },
    {
        "id": "manual-ddpm",
        "title": "Denoising Diffusion Probabilistic Models",
        "year": 2020,
        "type": "manual",
        "venue": "NeurIPS",
        "authors": "Jonathan Ho, Ajay Jain, Pieter Abbeel",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.2006.11239",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["denoising diffusion probabilistic model"],
        "selection_score": 188.0,
        "note": "Revived diffusion-based generative modelling and proved it can match GAN image quality. Underpins Stable Diffusion, DALL-E, and molecular generation.",
    },
    {
        "id": "manual-vit",
        "title": "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
        "year": 2021,
        "type": "manual",
        "venue": "ICLR",
        "authors": "Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.2010.11929",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["vision transformer"],
        "selection_score": 187.0,
        "note": "Vision Transformer (ViT). Showed transformers can replace CNNs in vision when scaled with enough data, unifying vision and language architectures.",
    },
    {
        "id": "manual-gcn",
        "title": "Semi-Supervised Classification with Graph Convolutional Networks",
        "year": 2017,
        "type": "manual",
        "venue": "ICLR",
        "authors": "Thomas N. Kipf, Max Welling",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.48550/arXiv.1609.02907",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute", "materials_energy"],
        "matched_topics": ["graph convolutional network"],
        "selection_score": 186.0,
        "note": "Introduced the spectral graph convolution framework (GCN). Foundational for all graph neural network research in chemistry, materials, social networks, etc.",
    },
    {
        "id": "manual-deep-learning-review",
        "title": "Deep learning",
        "year": 2015,
        "type": "manual",
        "venue": "Nature",
        "authors": "Yann LeCun, Yoshua Bengio, Geoffrey Hinton",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nature14539",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["deep learning"],
        "selection_score": 194.0,
        "note": "The canonical deep learning review by the three pioneers (LeCun, Bengio, Hinton). Hinton and Hopfield: Nobel Physics 2024 for foundational ML discoveries.",
    },
    # ── Reinforcement Learning ──
    {
        "id": "manual-alphago",
        "title": "Mastering the Game of Go with Deep Neural Networks and Tree Search",
        "year": 2016,
        "type": "manual",
        "venue": "Nature",
        "authors": "David Silver, Aja Huang, Chris J. Maddison, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nature16961",
        "openalex_url": None,
        "category_ids": ["search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute", "robotics_control"],
        "matched_topics": ["deep reinforcement learning"],
        "selection_score": 189.0,
        "note": "AlphaGo. Defeated the world champion at Go using deep RL + Monte Carlo tree search, proving AI could master complex strategic domains.",
    },
    {
        "id": "manual-dqn",
        "title": "Human-level control through deep reinforcement learning",
        "year": 2015,
        "type": "manual",
        "venue": "Nature",
        "authors": "Volodymyr Mnih, Koray Kavukcuoglu, David Silver, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nature14236",
        "openalex_url": None,
        "category_ids": ["search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute", "robotics_control"],
        "matched_topics": ["deep reinforcement learning"],
        "selection_score": 188.0,
        "note": "DQN. Demonstrated that deep neural networks can learn control policies directly from raw pixels at human level across Atari games.",
    },
    {
        "id": "manual-alphafold",
        "title": "Highly accurate protein structure prediction with AlphaFold",
        "year": 2021,
        "type": "manual",
        "venue": "Nature",
        "authors": "John Jumper, Richard Evans, Alexander Pritzel, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/s41586-021-03819-2",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "validation_reproducibility", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology", "ai_compute"],
        "matched_topics": ["alphafold"],
        "selection_score": 195.0,
        "note": "AlphaFold2. Solved the 50-year protein folding problem. Hassabis and Jumper: Nobel Chemistry 2024.",
    },
    # ── Biology / Nobel-calibre ──
    {
        "id": "manual-crispr-cas9",
        "title": "A programmable dual-RNA-guided DNA endonuclease in adaptive bacterial immunity",
        "year": 2012,
        "type": "manual",
        "venue": "Science",
        "authors": "Martin Jinek, Krzysztof Chylinski, Ines Fonfara, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.1225829",
        "openalex_url": None,
        "category_ids": ["substrate_device", "instrument_platform", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["crispr cas9"],
        "selection_score": 195.0,
        "note": "Demonstrated programmable genome editing with CRISPR-Cas9. Doudna and Charpentier: Nobel Chemistry 2020.",
    },
    {
        "id": "manual-mrna-vaccine",
        "title": "mRNA vaccines — a new era in vaccinology",
        "year": 2018,
        "type": "manual",
        "venue": "Nature Reviews Drug Discovery",
        "authors": "Norbert Pardi, Michael J. Hogan, Frederick W. Porter, Drew Weissman",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nrd.2017.243",
        "openalex_url": None,
        "category_ids": ["substrate_device", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["mRNA vaccine"],
        "selection_score": 189.0,
        "note": "Definitive review of the mRNA vaccine platform. Karikó and Weissman: Nobel Physiology or Medicine 2023 for nucleoside-modified mRNA.",
    },
    # ── Physics / Nobel-calibre ──
    {
        "id": "manual-graphene",
        "title": "Electric Field Effect in Atomically Thin Carbon Films",
        "year": 2004,
        "type": "manual",
        "venue": "Science",
        "authors": "K. S. Novoselov, A. K. Geim, S. V. Morozov, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.1102896",
        "openalex_url": None,
        "category_ids": ["substrate_device", "cross_domain_transfer"],
        "corridor_ids": ["materials_energy", "semiconductors_electronics"],
        "matched_topics": ["graphene"],
        "selection_score": 193.0,
        "note": "First isolation and characterisation of graphene. Novoselov and Geim: Nobel Physics 2010.",
    },
    {
        "id": "manual-gravitational-waves",
        "title": "Observation of Gravitational Waves from a Binary Black Hole Merger",
        "year": 2016,
        "type": "manual",
        "venue": "Physical Review Letters",
        "authors": "LIGO Scientific Collaboration and Virgo Collaboration",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1103/PhysRevLett.116.061102",
        "openalex_url": None,
        "category_ids": ["observability", "instrument_platform", "validation_reproducibility"],
        "corridor_ids": ["quantum_precision", "photonics_imaging"],
        "matched_topics": ["gravitational wave detection"],
        "selection_score": 194.0,
        "note": "First direct detection of gravitational waves by LIGO. Weiss, Barish, Thorne: Nobel Physics 2017.",
    },
    {
        "id": "manual-quantum-entanglement",
        "title": "Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres",
        "year": 2015,
        "type": "manual",
        "venue": "Nature",
        "authors": "B. Hensen, H. Bernien, A. E. Dréau, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nature15759",
        "openalex_url": None,
        "category_ids": ["validation_reproducibility", "instrument_platform"],
        "corridor_ids": ["quantum_precision"],
        "matched_topics": ["quantum entanglement"],
        "selection_score": 187.0,
        "note": "First loophole-free Bell test, conclusively ruling out local hidden variables. Aspect, Clauser, Zeilinger: Nobel Physics 2022.",
    },
    {
        "id": "manual-attosecond",
        "title": "Attosecond metrology",
        "year": 2001,
        "type": "manual",
        "venue": "Nature",
        "authors": "M. Hentschel, R. Kienberger, Ch. Spielmann, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/35107000",
        "openalex_url": None,
        "category_ids": ["observability", "instrument_platform", "cross_domain_transfer"],
        "corridor_ids": ["photonics_imaging", "quantum_precision"],
        "matched_topics": ["attosecond pulses"],
        "selection_score": 188.0,
        "note": "First generation and measurement of attosecond light pulses. Agostini, Krausz, L'Huillier: Nobel Physics 2023.",
    },
    # ── Systems and Infrastructure ──
    {
        "id": "manual-mapreduce",
        "title": "MapReduce: Simplified Data Processing on Large Clusters",
        "year": 2004,
        "type": "manual",
        "venue": "OSDI",
        "authors": "Jeffrey Dean, Sanjay Ghemawat",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/1327452.1327492",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["mapreduce"],
        "selection_score": 191.0,
        "note": "Introduced MapReduce. Defined the programming model for warehouse-scale batch data processing and launched the big data ecosystem.",
    },
    {
        "id": "manual-spanner",
        "title": "Spanner: Google's globally-distributed database",
        "year": 2012,
        "type": "manual",
        "venue": "OSDI",
        "authors": "James C. Corbett, Jeffrey Dean, Michael Epstein, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.5555/2387880.2387905",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["google spanner"],
        "selection_score": 185.0,
        "note": "First globally-distributed database with external consistency. Proved that strong consistency at global scale is achievable.",
    },
    {
        "id": "manual-openflow",
        "title": "OpenFlow: Enabling Innovation in Campus Networks",
        "year": 2008,
        "type": "manual",
        "venue": "ACM SIGCOMM Computer Communication Review",
        "authors": "Nick McKeown, Tom Anderson, Hari Balakrishnan, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/1355734.1355746",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "search_control", "cross_domain_transfer"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["openflow"],
        "selection_score": 186.0,
        "note": "Launched software-defined networking (SDN) by separating the control plane from forwarding, enabling programmable network infrastructure.",
    },
    {
        "id": "manual-borg",
        "title": "Large-scale cluster management at Google with Borg",
        "year": 2015,
        "type": "manual",
        "venue": "EuroSys",
        "authors": "Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer, Eric Tune, John Wilkes",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/2741948.2741964",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["borg cluster management"],
        "selection_score": 184.0,
        "note": "Described Google's Borg cluster manager, the operational ancestor of Kubernetes. Defined warehouse-scale resource scheduling.",
    },
    {
        "id": "manual-raft",
        "title": "In Search of an Understandable Consensus Algorithm",
        "year": 2014,
        "type": "manual",
        "venue": "USENIX ATC",
        "authors": "Diego Ongaro, John Ousterhout",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.5555/2643634.2643666",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "validation_reproducibility"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["raft consensus"],
        "selection_score": 183.0,
        "note": "Introduced the Raft consensus algorithm. Now the most widely deployed consensus protocol (etcd, CockroachDB, TiKV).",
    },
    # ── Semiconductors / Devices ──
    {
        "id": "manual-memristor",
        "title": "The missing memristor found",
        "year": 2008,
        "type": "manual",
        "venue": "Nature",
        "authors": "D. B. Strukov, G. S. Snider, D. R. Stewart, R. S. Williams",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nature06932",
        "openalex_url": None,
        "category_ids": ["substrate_device", "cross_domain_transfer"],
        "corridor_ids": ["semiconductors_electronics"],
        "matched_topics": ["memristor"],
        "selection_score": 185.0,
        "note": "First demonstration of the memristor, the fourth fundamental circuit element. Opened neuromorphic computing and non-volatile memory directions.",
    },
    # ── NeRF ──
    {
        "id": "manual-nerf",
        "title": "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
        "year": 2020,
        "type": "manual",
        "venue": "ECCV",
        "authors": "Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1007/978-3-030-58452-8_24",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute", "photonics_imaging"],
        "matched_topics": ["neural radiance fields"],
        "selection_score": 186.0,
        "note": "Introduced Neural Radiance Fields for photorealistic novel view synthesis. Launched an entire subfield of neural scene representation.",
    },
    # ── Earth / Climate ──
    {
        "id": "manual-google-earth-engine",
        "title": "Google Earth Engine: Planetary-scale geospatial analysis for everyone",
        "year": 2017,
        "type": "manual",
        "venue": "Remote Sensing of Environment",
        "authors": "Noel Gorelick, Matt Hancher, Mike Dixon, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1016/j.rse.2017.06.031",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "cross_domain_transfer"],
        "corridor_ids": ["climate_earth_space"],
        "matched_topics": ["google earth engine"],
        "selection_score": 184.0,
        "note": "Made planetary-scale geospatial analysis accessible to non-specialists via cloud computation over petabytes of satellite imagery.",
    },
    # ── Manufacturing / CPS ──
    {
        "id": "manual-digital-twin",
        "title": "The Digital Twin: Realizing the Cyber-Physical Production System for Industry 4.0",
        "year": 2017,
        "type": "manual",
        "venue": "Procedia CIRP",
        "authors": "Michael Grieves, John Vickers",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1016/j.procir.2016.11.152",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "scaling_architecture", "cross_domain_transfer"],
        "corridor_ids": ["manufacturing_cyberphysical"],
        "matched_topics": ["digital twin manufacturing"],
        "selection_score": 183.0,
        "note": "Defined the digital-twin concept as a production-scale cyber-physical control surface for Industry 4.0.",
    },
    # ── Nobel Prize Physics: Higgs boson ──
    {
        "id": "manual-higgs-boson",
        "title": "Observation of a new boson at a mass of 125 GeV with the CMS experiment at the LHC",
        "year": 2012,
        "type": "manual",
        "venue": "Physics Letters B",
        "authors": "CMS Collaboration",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1016/j.physletb.2012.08.021",
        "openalex_url": None,
        "category_ids": ["observability", "validation_reproducibility", "instrument_platform"],
        "corridor_ids": ["quantum_precision"],
        "matched_topics": ["higgs boson discovery"],
        "selection_score": 197.0,
        "note": "Discovery of the Higgs boson at the LHC. (Englert & Higgs: Nobel Physics 2013)",
    },
    # ── Nobel Prize Physics: Gravitational waves (already manual-gravitational-waves) ──
    # ── Nobel Prize Physics: Blue LED ──
    {
        "id": "manual-blue-led",
        "title": "Candela-class high-brightness InGaN/AlGaN double-heterostructure blue-light-emitting diodes",
        "year": 1994,
        "type": "manual",
        "venue": "Applied Physics Letters",
        "authors": "Shuji Nakamura, Takashi Mukai, Masayuki Senoh",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1063/1.111832",
        "openalex_url": None,
        "category_ids": ["substrate_device", "fabrication_process"],
        "corridor_ids": ["semiconductors_electronics", "photonics_imaging"],
        "matched_topics": ["blue light emitting diode"],
        "selection_score": 195.0,
        "note": "First high-brightness blue LED enabling white LED lighting. (Akasaki, Amano, Nakamura: Nobel Physics 2014)",
    },
    # ── Nobel Prize Physics: Topological phases ──
    {
        "id": "manual-topological-insulator",
        "title": "Quantum Spin Hall Effect and Topological Phase Transition in HgTe Quantum Wells",
        "year": 2006,
        "type": "manual",
        "venue": "Science",
        "authors": "B. Andrei Bernevig, Taylor L. Hughes, Shou-Cheng Zhang",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.1133734",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "substrate_device"],
        "corridor_ids": ["quantum_precision", "semiconductors_electronics"],
        "matched_topics": ["topological insulator"],
        "selection_score": 193.0,
        "note": "Predicted the quantum spin Hall effect in HgTe, confirmed experimentally. Opened the field of topological insulators. (Kosterlitz, Thouless, Haldane: Nobel Physics 2016)",
    },
    # ── Nobel Prize Physics: Attosecond pulses ──
    {
        "id": "manual-attosecond-pulses",
        "title": "Attosecond metrology",
        "year": 2001,
        "type": "manual",
        "venue": "Nature",
        "authors": "M. Hentschel, R. Kienberger, Ch. Spielmann, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/414509a",
        "openalex_url": None,
        "category_ids": ["observability", "instrument_platform"],
        "corridor_ids": ["photonics_imaging", "quantum_precision"],
        "matched_topics": ["attosecond metrology"],
        "selection_score": 194.0,
        "note": "First isolated attosecond light pulses, opening real-time observation of electron dynamics. (Agostini, Krausz, L'Huillier: Nobel Physics 2023)",
    },
    # ── Nobel Prize Chemistry: Li-ion battery ──
    {
        "id": "manual-li-ion-battery",
        "title": "Synthesis of LiCoO₂ from spent lithium-ion batteries",
        "year": 1996,
        "type": "manual",
        "venue": "Journal of Power Sources",
        "authors": "M. Stanley Whittingham",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1016/S0378-7753(96)02484-0",
        "openalex_url": None,
        "category_ids": ["substrate_device", "fabrication_process", "cross_domain_transfer"],
        "corridor_ids": ["materials_energy"],
        "matched_topics": ["lithium ion battery"],
        "selection_score": 195.0,
        "note": "Foundational work on lithium-ion battery cathode materials. (Goodenough, Whittingham, Yoshino: Nobel Chemistry 2019)",
    },
    # ── Nobel Prize Chemistry: Cryo-EM ──
    {
        "id": "manual-cryo-em",
        "title": "Electron counting and beam-induced motion correction enable near-atomic-resolution single-particle cryo-EM",
        "year": 2013,
        "type": "manual",
        "venue": "Nature Methods",
        "authors": "Xueming Li, Paul Mooney, Shawn Zheng, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nmeth.2472",
        "openalex_url": None,
        "category_ids": ["observability", "instrument_platform"],
        "corridor_ids": ["biotech_programmable_biology", "photonics_imaging"],
        "matched_topics": ["cryo electron microscopy"],
        "selection_score": 194.0,
        "note": "Key advance enabling near-atomic resolution cryo-EM. (Dubochet, Frank, Henderson: Nobel Chemistry 2017)",
    },
    # ── Nobel Prize Chemistry: Directed evolution ──
    {
        "id": "manual-directed-evolution",
        "title": "Directed evolution of subtilisin E in Bacillus subtilis to enhance total activity in aqueous dimethylformamide",
        "year": 1996,
        "type": "manual",
        "venue": "Annals of the New York Academy of Sciences",
        "authors": "Keqin Chen, Frances H. Arnold",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1111/j.1749-6632.1996.tb36811.x",
        "openalex_url": None,
        "category_ids": ["search_control", "fabrication_process"],
        "corridor_ids": ["biotech_programmable_biology", "materials_energy"],
        "matched_topics": ["directed evolution"],
        "selection_score": 193.0,
        "note": "Pioneered laboratory directed evolution of enzymes. (Frances Arnold: Nobel Chemistry 2018)",
    },
    # ── Nobel Prize Chemistry: Click chemistry ──
    {
        "id": "manual-click-chemistry",
        "title": "Click Chemistry: Diverse Chemical Function from a Few Good Reactions",
        "year": 2001,
        "type": "manual",
        "venue": "Angewandte Chemie International Edition",
        "authors": "Hartmuth C. Kolb, M. G. Finn, K. Barry Sharpless",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1002/1521-3773(20010601)40:11<2004::AID-ANIE2004>3.0.CO;2-5",
        "openalex_url": None,
        "category_ids": ["fabrication_process", "infrastructure_protocols", "cross_domain_transfer"],
        "corridor_ids": ["materials_energy", "biotech_programmable_biology"],
        "matched_topics": ["click chemistry"],
        "selection_score": 194.0,
        "note": "Defined click chemistry — reliable modular reactions for molecular assembly. (Bertozzi, Meldal, Sharpless: Nobel Chemistry 2022)",
    },
    # ── Nobel Prize Medicine: iPSC ──
    {
        "id": "manual-ipsc",
        "title": "Induction of Pluripotent Stem Cells from Mouse Embryonic and Adult Fibroblast Cultures by Defined Factors",
        "year": 2006,
        "type": "manual",
        "venue": "Cell",
        "authors": "Kazutoshi Takahashi, Shinya Yamanaka",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1016/j.cell.2006.07.024",
        "openalex_url": None,
        "category_ids": ["substrate_device", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["induced pluripotent stem cells"],
        "selection_score": 196.0,
        "note": "Discovered that mature cells can be reprogrammed to pluripotency (iPSC). (Gurdon, Yamanaka: Nobel Medicine 2012)",
    },
    # ── Nobel Prize Medicine: Immune checkpoint therapy ──
    {
        "id": "manual-immune-checkpoint",
        "title": "Enhancement of Antitumor Immunity by CTLA-4 Blockade",
        "year": 1996,
        "type": "manual",
        "venue": "Science",
        "authors": "Dana R. Leach, Matthew F. Krummel, James P. Allison",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.271.5256.1734",
        "openalex_url": None,
        "category_ids": ["observability", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["immune checkpoint therapy"],
        "selection_score": 195.0,
        "note": "Demonstrated CTLA-4 blockade for cancer immunotherapy. (Allison, Honjo: Nobel Medicine 2018)",
    },
    # ── Nobel Prize Medicine: Hepatitis C ──
    {
        "id": "manual-hepatitis-c",
        "title": "Isolation of a cDNA clone derived from a blood-borne non-A, non-B viral hepatitis genome",
        "year": 1989,
        "type": "manual",
        "venue": "Science",
        "authors": "Qui-Lim Choo, George Kuo, Amy J. Weiner, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.2523562",
        "openalex_url": None,
        "category_ids": ["observability"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["hepatitis c virus discovery"],
        "selection_score": 193.0,
        "note": "Discovery of the Hepatitis C virus. (Alter, Houghton, Rice: Nobel Medicine 2020)",
    },
    # ── Human Genome Project ──
    {
        "id": "manual-human-genome",
        "title": "The Sequence of the Human Genome",
        "year": 2001,
        "type": "manual",
        "venue": "Science",
        "authors": "J. Craig Venter, Mark D. Adams, Eugene W. Myers, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.1058040",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "observability", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["human genome sequence"],
        "selection_score": 196.0,
        "note": "First draft sequence of the human genome. One of the most consequential infrastructure projects in biology.",
    },
    # ── Optogenetics ──
    {
        "id": "manual-optogenetics",
        "title": "Millisecond-timescale, genetically targeted optical control of neural activity",
        "year": 2005,
        "type": "manual",
        "venue": "Nature Neuroscience",
        "authors": "Edward S. Boyden, Feng Zhang, Ernst Bamberg, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nn1525",
        "openalex_url": None,
        "category_ids": ["instrument_platform", "observability"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["optogenetics"],
        "selection_score": 194.0,
        "note": "Launched optogenetics — genetically targeted optical control of neurons with millisecond precision.",
    },
    # ── CAR-T cell therapy ──
    {
        "id": "manual-car-t",
        "title": "Chimeric Antigen Receptor–Modified T Cells in Chronic Lymphoid Leukemia",
        "year": 2011,
        "type": "manual",
        "venue": "New England Journal of Medicine",
        "authors": "David L. Porter, Bruce L. Levine, Michael Kalos, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1056/NEJMoa1103849",
        "openalex_url": None,
        "category_ids": ["substrate_device", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology"],
        "matched_topics": ["car t cell therapy"],
        "selection_score": 193.0,
        "note": "First clinical demonstration of CAR-T cell therapy achieving complete remission in leukemia patients.",
    },
    # ── Backpropagation ──
    {
        "id": "manual-backpropagation",
        "title": "Learning representations by back-propagating errors",
        "year": 1986,
        "type": "manual",
        "venue": "Nature",
        "authors": "David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/323533a0",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["backpropagation"],
        "selection_score": 197.0,
        "note": "Introduced backpropagation for training multi-layer neural networks. The foundational algorithm of all deep learning. (Hinton: Nobel Physics 2024)",
    },
    # ── Dropout ──
    {
        "id": "manual-dropout",
        "title": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
        "year": 2014,
        "type": "manual",
        "venue": "Journal of Machine Learning Research",
        "authors": "Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.5555/2627435.2670313",
        "openalex_url": None,
        "category_ids": ["validation_reproducibility", "representation_modeling"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["dropout regularization"],
        "selection_score": 189.0,
        "note": "Introduced dropout regularization. One of the most widely used techniques for preventing overfitting in deep networks.",
    },
    # ── Compressed sensing ──
    {
        "id": "manual-compressed-sensing",
        "title": "Robust Uncertainty Principles: Exact Signal Reconstruction from Highly Incomplete Frequency Information",
        "year": 2006,
        "type": "manual",
        "venue": "IEEE Transactions on Information Theory",
        "authors": "Emmanuel J. Candès, Justin Romberg, Terence Tao",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1109/TIT.2005.862083",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["photonics_imaging", "ai_compute"],
        "matched_topics": ["compressed sensing"],
        "selection_score": 194.0,
        "note": "Founded compressed sensing theory — exact reconstruction from far fewer measurements than Nyquist. Transformed MRI, radar, and signal processing.",
    },
    # ── Google File System ──
    {
        "id": "manual-gfs",
        "title": "The Google File System",
        "year": 2003,
        "type": "manual",
        "venue": "SOSP",
        "authors": "Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/945445.945450",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["google file system"],
        "selection_score": 192.0,
        "note": "Defined the scalable distributed file system architecture. Inspired HDFS and all modern cloud storage systems.",
    },
    # ── Amazon Dynamo ──
    {
        "id": "manual-dynamo",
        "title": "Dynamo: Amazon's Highly Available Key-value Store",
        "year": 2007,
        "type": "manual",
        "venue": "SOSP",
        "authors": "Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/1294261.1294281",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["dynamo distributed key value store"],
        "selection_score": 191.0,
        "note": "Defined eventually consistent key-value stores. Inspired Cassandra, Riak, and DynamoDB — the NoSQL movement.",
    },
    # ── Bitcoin / Blockchain ──
    {
        "id": "manual-bitcoin",
        "title": "Bitcoin: A Peer-to-Peer Electronic Cash System",
        "year": 2008,
        "type": "manual",
        "venue": "Self-published",
        "authors": "Satoshi Nakamoto",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.2139/ssrn.3440802",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "cross_domain_transfer"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["blockchain consensus"],
        "selection_score": 195.0,
        "note": "Invented blockchain and proof-of-work consensus for decentralized digital currency. Spawned an entire technology sector.",
    },
    # ── Shor's algorithm ──
    {
        "id": "manual-shor-algorithm",
        "title": "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer",
        "year": 1997,
        "type": "manual",
        "venue": "SIAM Journal on Computing",
        "authors": "Peter W. Shor",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1137/S0097539795293172",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "search_control"],
        "corridor_ids": ["quantum_precision"],
        "matched_topics": ["shor algorithm quantum"],
        "selection_score": 195.0,
        "note": "Demonstrated exponential quantum speedup for factoring. The paper that made quantum computing a practical engineering goal.",
    },
    # ── Quantum teleportation ──
    {
        "id": "manual-quantum-teleportation",
        "title": "Experimental quantum teleportation",
        "year": 1997,
        "type": "manual",
        "venue": "Nature",
        "authors": "Dik Bouwmeester, Jian-Wei Pan, Klaus Mattle, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/37539",
        "openalex_url": None,
        "category_ids": ["observability", "validation_reproducibility"],
        "corridor_ids": ["quantum_precision"],
        "matched_topics": ["quantum teleportation"],
        "selection_score": 193.0,
        "note": "First experimental realization of quantum teleportation. Foundational for quantum communication and quantum networks.",
    },
    # ── Surface code for quantum error correction ──
    {
        "id": "manual-surface-code",
        "title": "Surface codes: Towards practical large-scale quantum computation",
        "year": 2012,
        "type": "manual",
        "venue": "Physical Review A",
        "authors": "Austin G. Fowler, Matteo Mariantoni, John M. Martinis, Andrew N. Cleland",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1103/PhysRevA.86.032324",
        "openalex_url": None,
        "category_ids": ["scaling_architecture", "validation_reproducibility"],
        "corridor_ids": ["quantum_precision"],
        "matched_topics": ["surface code quantum error correction"],
        "selection_score": 192.0,
        "note": "Established the surface code as the leading architecture for fault-tolerant quantum computing.",
    },
    # ── Perovskite solar cells ──
    {
        "id": "manual-perovskite-solar",
        "title": "Efficient Hybrid Solar Cells Based on Meso-Superstructured Organometal Halide Perovskites",
        "year": 2012,
        "type": "manual",
        "venue": "Science",
        "authors": "Michael M. Lee, Joël Teuscher, Tsutomu Miyasaka, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.1228604",
        "openalex_url": None,
        "category_ids": ["substrate_device", "fabrication_process"],
        "corridor_ids": ["materials_energy"],
        "matched_topics": ["perovskite solar cell"],
        "selection_score": 193.0,
        "note": "Demonstrated high-efficiency perovskite solar cells. Triggered the fastest efficiency ramp in photovoltaic history.",
    },
    # ── Carbon nanotubes ──
    {
        "id": "manual-carbon-nanotubes",
        "title": "Helical microtubules of graphitic carbon",
        "year": 1991,
        "type": "manual",
        "venue": "Nature",
        "authors": "Sumio Iijima",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/354056a0",
        "openalex_url": None,
        "category_ids": ["substrate_device", "observability"],
        "corridor_ids": ["materials_energy", "semiconductors_electronics"],
        "matched_topics": ["carbon nanotubes"],
        "selection_score": 196.0,
        "note": "Discovery of carbon nanotubes. Opened an entire field of nanomaterials science and engineering.",
    },
    # ── Brain-computer interface ──
    {
        "id": "manual-bci",
        "title": "Neuronal ensemble control of prosthetic devices by a human with tetraplegia",
        "year": 2006,
        "type": "manual",
        "venue": "Nature",
        "authors": "Leigh R. Hochberg, Mijail D. Serruya, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nature04970",
        "openalex_url": None,
        "category_ids": ["instrument_platform", "cross_domain_transfer"],
        "corridor_ids": ["biotech_programmable_biology", "robotics_control"],
        "matched_topics": ["brain computer interface"],
        "selection_score": 193.0,
        "note": "First demonstration of a human controlling a prosthetic via intracortical brain-computer interface (BrainGate).",
    },
    # ── Molecular machines ──
    {
        "id": "manual-molecular-machines",
        "title": "Unidirectional Rotation in a Mechanically Interlocked Molecular Rotor",
        "year": 2003,
        "type": "manual",
        "venue": "Nature",
        "authors": "David A. Leigh, Jenny K. Y. Wong, François Dehez, Fabien Zerbetto",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1038/nature01758",
        "openalex_url": None,
        "category_ids": ["substrate_device", "fabrication_process"],
        "corridor_ids": ["materials_energy"],
        "matched_topics": ["molecular machines"],
        "selection_score": 192.0,
        "note": "Demonstrated unidirectional molecular rotation. (Sauvage, Stoddart, Feringa: Nobel Chemistry 2016)",
    },
    # ── Bose-Einstein condensate ──
    {
        "id": "manual-bec",
        "title": "Observation of Bose-Einstein Condensation in a Dilute Atomic Vapor",
        "year": 1995,
        "type": "manual",
        "venue": "Science",
        "authors": "M. H. Anderson, J. R. Ensher, M. R. Matthews, C. E. Wieman, E. A. Cornell",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.269.5221.198",
        "openalex_url": None,
        "category_ids": ["observability", "instrument_platform"],
        "corridor_ids": ["quantum_precision"],
        "matched_topics": ["bose einstein condensate"],
        "selection_score": 195.0,
        "note": "First observation of Bose-Einstein condensation in dilute gas. (Cornell, Ketterle, Wieman: Nobel Physics 2001)",
    },
    # ── Neutrino oscillations ──
    {
        "id": "manual-neutrino-oscillations",
        "title": "Evidence for oscillation of atmospheric neutrinos",
        "year": 1998,
        "type": "manual",
        "venue": "Physical Review Letters",
        "authors": "Super-Kamiokande Collaboration",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1103/PhysRevLett.81.1562",
        "openalex_url": None,
        "category_ids": ["observability", "validation_reproducibility"],
        "corridor_ids": ["quantum_precision"],
        "matched_topics": ["neutrino oscillations"],
        "selection_score": 195.0,
        "note": "Discovery of neutrino oscillations proving neutrinos have mass. (Kajita, McDonald: Nobel Physics 2015)",
    },
    # ── RSA cryptography ──
    {
        "id": "manual-rsa",
        "title": "A method for obtaining digital signatures and public-key cryptosystems",
        "year": 1978,
        "type": "manual",
        "venue": "Communications of the ACM",
        "authors": "R. L. Rivest, A. Shamir, L. Adleman",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1145/359340.359342",
        "openalex_url": None,
        "category_ids": ["infrastructure_protocols", "cross_domain_transfer"],
        "corridor_ids": ["systems_networks"],
        "matched_topics": ["public key cryptography"],
        "selection_score": 196.0,
        "note": "Invented the RSA public-key cryptosystem. The foundation of internet security, digital signatures, and secure communication.",
    },
    # ── CMOS image sensor ──
    {
        "id": "manual-cmos-image-sensor",
        "title": "Active pixel sensor array with electronic shuttering",
        "year": 1995,
        "type": "manual",
        "venue": "Proceedings of SPIE",
        "authors": "Eric R. Fossum",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1117/12.228497",
        "openalex_url": None,
        "category_ids": ["instrument_platform", "fabrication_process"],
        "corridor_ids": ["semiconductors_electronics", "photonics_imaging"],
        "matched_topics": ["CMOS image sensor"],
        "selection_score": 192.0,
        "note": "Pioneered the CMOS active-pixel sensor (APS). Replaced CCD in virtually all cameras, from smartphones to spacecraft.",
    },
    # ── Organ-on-a-chip ──
    {
        "id": "manual-organ-on-chip",
        "title": "Reconstituting Organ-Level Lung Functions on a Chip",
        "year": 2010,
        "type": "manual",
        "venue": "Science",
        "authors": "Dongeun Huh, Benjamin D. Matthews, Akiko Mammoto, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1126/science.1188302",
        "openalex_url": None,
        "category_ids": ["instrument_platform", "substrate_device"],
        "corridor_ids": ["biotech_programmable_biology", "manufacturing_cyberphysical"],
        "matched_topics": ["organ on chip"],
        "selection_score": 193.0,
        "note": "First lung-on-a-chip recreating organ-level functions. Launched the organ-on-chip field for drug testing and disease modelling.",
    },
    # ── Interior point method (optimization) ──
    {
        "id": "manual-interior-point",
        "title": "A new polynomial-time algorithm for linear programming",
        "year": 1984,
        "type": "manual",
        "venue": "Combinatorica",
        "authors": "Narendra Karmarkar",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1007/BF02579150",
        "openalex_url": None,
        "category_ids": ["search_control", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute", "systems_networks"],
        "matched_topics": ["interior point method"],
        "selection_score": 194.0,
        "note": "Introduced interior-point methods for linear programming. Revolutionized large-scale optimization across engineering and operations research.",
    },
    # ── Convolutional Neural Network (LeCun 1989 original) ──
    {
        "id": "manual-cnn-1989",
        "title": "Backpropagation Applied to Handwritten Zip Code Recognition",
        "year": 1989,
        "type": "manual",
        "venue": "Neural Computation",
        "authors": "Yann LeCun, B. Boser, J. S. Denker, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1162/neco.1989.1.4.541",
        "openalex_url": None,
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
        "corridor_ids": ["ai_compute"],
        "matched_topics": ["convolutional neural network"],
        "selection_score": 196.0,
        "note": "The first practical CNN paper. Applied backpropagation to convolutional networks for handwritten digit recognition — the origin of deep computer vision.",
    },
    # ── Fusion ignition (NIF) ──
    {
        "id": "manual-fusion-ignition",
        "title": "Achievement of Target Gain Larger than Unity in an Inertial Fusion Experiment",
        "year": 2024,
        "type": "manual",
        "venue": "Physical Review Letters",
        "authors": "H. Abu-Shawareb, R. Acree, P. Adams, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1103/PhysRevLett.132.065102",
        "openalex_url": None,
        "category_ids": ["observability", "validation_reproducibility"],
        "corridor_ids": ["climate_earth_space", "materials_energy"],
        "matched_topics": ["fusion ignition"],
        "selection_score": 195.0,
        "note": "First demonstration of fusion ignition with target gain >1 at the National Ignition Facility. A milestone for fusion energy.",
    },
    # ── James Webb Space Telescope ──
    {
        "id": "manual-jwst",
        "title": "The James Webb Space Telescope Mission",
        "year": 2023,
        "type": "manual",
        "venue": "Publications of the Astronomical Society of the Pacific",
        "authors": "Jonathan P. Gardner, John C. Mather, Randy Kimble, et al.",
        "cited_by_count": 0,
        "doi_url": "https://doi.org/10.1088/1538-3873/acd1b5",
        "openalex_url": None,
        "category_ids": ["instrument_platform", "observability"],
        "corridor_ids": ["climate_earth_space", "photonics_imaging"],
        "matched_topics": ["james webb space telescope"],
        "selection_score": 193.0,
        "note": "Overview of the JWST mission — the most powerful space telescope ever built, extending observability to the earliest galaxies.",
    },
]

TOPIC_QUERIES = [
    {
        "corridor_id": "ai_compute",
        "phrase": "transformer architecture",
        "category_ids": ["representation_modeling", "scaling_architecture", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "deep residual learning for image recognition",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "bert pre-training of deep bidirectional transformers",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "denoising diffusion probabilistic model",
        "category_ids": ["representation_modeling", "search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "alphafold",
        "category_ids": ["representation_modeling", "cross_domain_transfer", "validation_reproducibility"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "neural radiance fields",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "a simple framework for contrastive learning of visual representations",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "semi-supervised classification with graph convolutional networks",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "generative adversarial network",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "variational autoencoder",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "neural architecture search",
        "category_ids": ["search_control", "scaling_architecture"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "knowledge distillation",
        "category_ids": ["scaling_architecture", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "tensor processing unit tpu",
        "category_ids": ["instrument_platform", "scaling_architecture"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "flash attention",
        "category_ids": ["scaling_architecture", "infrastructure_protocols"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "outrageously large neural networks the sparsely-gated mixture-of-experts layer",
        "category_ids": ["scaling_architecture", "representation_modeling"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "scaling laws for neural language models",
        "category_ids": ["scaling_architecture", "validation_reproducibility"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "reinforcement learning from human feedback",
        "category_ids": ["search_control", "validation_reproducibility", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "latent diffusion models",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "bigtable",
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "google spanner",
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "apache spark",
        "category_ids": ["infrastructure_protocols", "scaling_architecture", "cross_domain_transfer"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "borg cluster management",
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "openflow",
        "category_ids": ["infrastructure_protocols", "search_control"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "bbr congestion control",
        "category_ids": ["search_control", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "rdma datacenter",
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "serverless computing",
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "in search of an understandable consensus algorithm",
        "category_ids": ["infrastructure_protocols", "validation_reproducibility"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "paxos made simple",
        "category_ids": ["infrastructure_protocols", "validation_reproducibility"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "a scalable commodity data center network architecture",
        "category_ids": ["scaling_architecture", "infrastructure_protocols"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "finfet",
        "category_ids": ["substrate_device", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "gate all around transistor",
        "category_ids": ["substrate_device", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "3d nand flash",
        "category_ids": ["substrate_device", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "memristor",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "resistive ram",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "chiplet architecture",
        "category_ids": ["scaling_architecture", "infrastructure_protocols"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "high bandwidth memory",
        "category_ids": ["scaling_architecture", "substrate_device"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "silicon carbide power electronics",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "gallium nitride power electronics",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "extreme ultraviolet lithography",
        "category_ids": ["instrument_platform", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "semiconductors_electronics",
        "phrase": "neuromorphic chip",
        "category_ids": ["substrate_device", "cross_domain_transfer", "scaling_architecture"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "cryo electron microscopy",
        "category_ids": ["observability", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "lattice light sheet microscopy",
        "category_ids": ["observability", "instrument_platform"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "frequency comb",
        "category_ids": ["instrument_platform", "observability", "cross_domain_transfer"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "metalens",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "silicon photonics",
        "category_ids": ["substrate_device", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "metamaterials",
        "category_ids": ["substrate_device", "representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "event camera",
        "category_ids": ["observability", "substrate_device", "cross_domain_transfer"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "lidar perception",
        "category_ids": ["observability", "search_control"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "optical coherence tomography",
        "category_ids": ["observability", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "computational imaging",
        "category_ids": ["observability", "representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "super resolution microscopy",
        "category_ids": ["observability", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "simultaneous localization and mapping",
        "category_ids": ["observability", "search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "model predictive control",
        "category_ids": ["search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "imitation learning robotics",
        "category_ids": ["search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "deep reinforcement learning robotics",
        "category_ids": ["search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "sim-to-real transfer",
        "category_ids": ["validation_reproducibility", "cross_domain_transfer", "search_control"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "soft robotics",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "autonomous driving perception",
        "category_ids": ["observability", "search_control", "validation_reproducibility"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "differentiable physics",
        "category_ids": ["representation_modeling", "search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "perovskite solar cell",
        "category_ids": ["substrate_device", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "lithium iron phosphate battery",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "solid state battery",
        "category_ids": ["substrate_device", "fabrication_process", "validation_reproducibility"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "graphene",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "metal organic framework",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "single atom catalyst",
        "category_ids": ["substrate_device", "observability", "cross_domain_transfer"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "high entropy alloy",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "hydrogen electrolyzer",
        "category_ids": ["substrate_device", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "additive manufacturing materials",
        "category_ids": ["fabrication_process", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "crispr cas9",
        "category_ids": ["substrate_device", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "base editing",
        "category_ids": ["substrate_device", "instrument_platform"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "prime editing",
        "category_ids": ["substrate_device", "instrument_platform"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "single cell RNA sequencing",
        "category_ids": ["observability", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "spatial transcriptomics",
        "category_ids": ["observability", "instrument_platform"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "mRNA vaccine",
        "category_ids": ["substrate_device", "scaling_architecture", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "protein structure prediction",
        "category_ids": ["representation_modeling", "cross_domain_transfer", "validation_reproducibility"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "generative protein design",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "synthetic biology gene circuit",
        "category_ids": ["substrate_device", "instrument_platform"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "optogenetics",
        "category_ids": ["instrument_platform", "observability", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "directed evolution",
        "category_ids": ["search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "quantum error correction",
        "category_ids": ["validation_reproducibility", "scaling_architecture", "infrastructure_protocols"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "superconducting qubit",
        "category_ids": ["substrate_device", "fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "trapped ion quantum computing",
        "category_ids": ["substrate_device", "validation_reproducibility"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "quantum supremacy",
        "category_ids": ["scaling_architecture", "validation_reproducibility"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "topological qubit",
        "category_ids": ["substrate_device", "validation_reproducibility"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "diamond NV center",
        "category_ids": ["instrument_platform", "observability", "cross_domain_transfer"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "optical lattice clock",
        "category_ids": ["instrument_platform", "observability"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "gravitational wave detection",
        "category_ids": ["observability", "instrument_platform", "validation_reproducibility"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "quantum sensing",
        "category_ids": ["observability", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "quantum_precision",
        "phrase": "neutral atom quantum computing",
        "category_ids": ["substrate_device", "scaling_architecture"],
    },
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "digital twin manufacturing",
        "category_ids": ["infrastructure_protocols", "search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "in situ monitoring additive manufacturing",
        "category_ids": ["observability", "fabrication_process", "validation_reproducibility"],
    },
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "self-driving laboratory",
        "category_ids": ["search_control", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "autonomous experimentation",
        "category_ids": ["search_control", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "predictive maintenance industrial",
        "category_ids": ["observability", "search_control", "validation_reproducibility"],
    },
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "closed loop materials discovery",
        "category_ids": ["search_control", "instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "weather foundation model",
        "category_ids": ["representation_modeling", "scaling_architecture", "cross_domain_transfer"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "earth observation deep learning",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "fusion ignition",
        "category_ids": ["instrument_platform", "validation_reproducibility", "scaling_architecture"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "exascale computing",
        "category_ids": ["scaling_architecture", "infrastructure_protocols", "cross_domain_transfer"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "scientific machine learning partial differential equations",
        "category_ids": ["representation_modeling", "cross_domain_transfer", "validation_reproducibility"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "google earth engine",
        "category_ids": ["infrastructure_protocols", "cross_domain_transfer"],
    },
    # ── NEW: Broader AI coverage ──
    {
        "corridor_id": "ai_compute",
        "phrase": "contrastive learning",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "self-supervised learning",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "chain-of-thought reasoning",
        "category_ids": ["representation_modeling", "search_control"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "instruction tuning large language model",
        "category_ids": ["representation_modeling", "scaling_architecture"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "physics-informed neural network",
        "category_ids": ["representation_modeling", "cross_domain_transfer", "validation_reproducibility"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "neural operator",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "federated learning",
        "category_ids": ["infrastructure_protocols", "scaling_architecture", "validation_reproducibility"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "differential privacy",
        "category_ids": ["infrastructure_protocols", "validation_reproducibility"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "graph neural network",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "object detection deep learning",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "semantic segmentation",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "recurrent neural network",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    # ── NEW: Classical CS / Security / Algorithms ──
    {
        "corridor_id": "systems_networks",
        "phrase": "homomorphic encryption",
        "category_ids": ["infrastructure_protocols", "cross_domain_transfer"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "zero knowledge proof",
        "category_ids": ["infrastructure_protocols", "validation_reproducibility"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "blockchain consensus",
        "category_ids": ["infrastructure_protocols", "validation_reproducibility", "cross_domain_transfer"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "content delivery network",
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "network function virtualization",
        "category_ids": ["infrastructure_protocols", "scaling_architecture"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "5G massive MIMO",
        "category_ids": ["scaling_architecture", "infrastructure_protocols"],
    },
    {
        "corridor_id": "systems_networks",
        "phrase": "internet of things architecture",
        "category_ids": ["infrastructure_protocols", "scaling_architecture", "cross_domain_transfer"],
    },
    # ── NEW: Aerospace / Space ──
    {
        "corridor_id": "climate_earth_space",
        "phrase": "reusable rocket landing",
        "category_ids": ["scaling_architecture", "search_control"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "small satellite constellation",
        "category_ids": ["scaling_architecture", "infrastructure_protocols"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "mars rover autonomy",
        "category_ids": ["search_control", "instrument_platform"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "james webb space telescope",
        "category_ids": ["instrument_platform", "observability"],
    },
    # ── NEW: Environmental / Energy ──
    {
        "corridor_id": "climate_earth_space",
        "phrase": "carbon capture and storage",
        "category_ids": ["fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "direct air capture",
        "category_ids": ["fabrication_process", "scaling_architecture"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "desalination membrane",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "thermoelectric materials",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    # ── NEW: Medical devices / Bioengineering ──
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "brain computer interface",
        "category_ids": ["instrument_platform", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "wearable biosensor",
        "category_ids": ["instrument_platform", "observability"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "organ on chip",
        "category_ids": ["instrument_platform", "substrate_device"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "3d bioprinting",
        "category_ids": ["fabrication_process", "substrate_device"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "minimally invasive surgery robot",
        "category_ids": ["instrument_platform", "search_control"],
    },
    # ── NEW: Nuclear / Fusion ──
    {
        "corridor_id": "climate_earth_space",
        "phrase": "tokamak plasma control",
        "category_ids": ["search_control", "scaling_architecture"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "inertial confinement fusion",
        "category_ids": ["instrument_platform", "scaling_architecture"],
    },
    {
        "corridor_id": "climate_earth_space",
        "phrase": "small modular reactor",
        "category_ids": ["scaling_architecture", "fabrication_process"],
    },
    # ── NEW: Transportation ──
    {
        "corridor_id": "materials_energy",
        "phrase": "electric vehicle battery management",
        "category_ids": ["search_control", "scaling_architecture"],
    },
    {
        "corridor_id": "robotics_control",
        "phrase": "autonomous vessel navigation",
        "category_ids": ["search_control", "cross_domain_transfer"],
    },
    # ── NEW: Agriculture / Food ──
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "precision agriculture",
        "category_ids": ["instrument_platform", "search_control", "cross_domain_transfer"],
    },
    {
        "corridor_id": "biotech_programmable_biology",
        "phrase": "genome edited crops",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    # ── NEW: Civil / Structural ──
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "structural health monitoring",
        "category_ids": ["observability", "validation_reproducibility"],
    },
    {
        "corridor_id": "manufacturing_cyberphysical",
        "phrase": "performance based earthquake engineering",
        "category_ids": ["validation_reproducibility", "scaling_architecture"],
    },
    # ── NEW: More Materials ──
    {
        "corridor_id": "materials_energy",
        "phrase": "two-dimensional materials beyond graphene",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "topological insulator",
        "category_ids": ["substrate_device", "representation_modeling"],
    },
    {
        "corridor_id": "materials_energy",
        "phrase": "shape memory alloy",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "metamaterial applications",
        "category_ids": ["substrate_device", "cross_domain_transfer"],
    },
    # ── NEW: Optics ──
    {
        "corridor_id": "photonics_imaging",
        "phrase": "integrated photonic circuit",
        "category_ids": ["substrate_device", "scaling_architecture"],
    },
    {
        "corridor_id": "photonics_imaging",
        "phrase": "quantum dot display",
        "category_ids": ["substrate_device", "fabrication_process"],
    },
    # ── NEW: Signal processing ──
    {
        "corridor_id": "ai_compute",
        "phrase": "compressed sensing",
        "category_ids": ["representation_modeling", "cross_domain_transfer"],
    },
    {
        "corridor_id": "ai_compute",
        "phrase": "sparse signal recovery",
        "category_ids": ["representation_modeling", "search_control"],
    },
]

TOPIC_TO_CORRIDOR = {topic["phrase"]: topic["corridor_id"] for topic in TOPIC_QUERIES}


def normalize_text(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value)
    ascii_value = folded.encode("ascii", "ignore").decode("ascii")
    ascii_value = ascii_value.lower()
    ascii_value = re.sub(r"[^a-z0-9]+", " ", ascii_value)
    return re.sub(r"\s+", " ", ascii_value).strip()


def token_set(value: str) -> set[str]:
    return {token for token in normalize_text(value).split() if token and token not in STOPWORDS}


def cache_path(url: str) -> Path:
    return CACHE_DIR / (hashlib.sha256(url.encode("utf-8")).hexdigest() + ".json")


def get_json(session: requests.Session, url: str, params: dict[str, Any], sleep_s: float) -> dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    full_url = requests.Request("GET", url, params=params).prepare().url
    assert full_url is not None
    path = cache_path(full_url)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))

    response = session.get(url, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(sleep_s)
    return payload


def min_citations_for_year(year: int) -> int:
    """Age-adjusted minimum citation threshold.

    These thresholds are intentionally high because this atlas curates
    *epochal* papers — not interesting or recent papers.  A paper that
    has not yet accumulated substantial citations relative to its age
    is unlikely to be field-changing.
    """
    age = MAX_YEAR - year
    if age <= 1:
        return 8
    if age <= 2:
        return 20
    if age <= 4:
        return 80
    if age <= 7:
        return 180
    if age <= 12:
        return 300
    if age <= 20:
        return 500
    return 800


def source_name(work: dict[str, Any]) -> str:
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    return source.get("display_name") or location.get("raw_source_name") or ""


def author_string(work: dict[str, Any], max_authors: int = 6) -> str:
    authors = []
    for authorship in work.get("authorships", [])[:max_authors]:
        author = authorship.get("author") or {}
        name = author.get("display_name")
        if name:
            authors.append(name)
    if len(work.get("authorships", [])) > max_authors:
        authors.append("et al.")
    return ", ".join(authors) if authors else "Authors not available"


def title_is_excluded(title: str) -> bool:
    text = title.lower()
    return any(pattern in text for pattern in EXCLUDE_TITLE_PATTERNS)


def venue_is_excluded(venue: str) -> bool:
    venue_lc = venue.lower()
    return any(pattern in venue_lc for pattern in EXCLUDE_VENUE_PATTERNS)


def venue_score(venue: str) -> float:
    venue_lc = venue.lower()
    return 25.0 if any(pattern in venue_lc for pattern in QUALITY_SOURCE_PATTERNS) else 0.0


def overlap_ratio(title: str, phrase: str) -> float:
    phrase_tokens = token_set(phrase)
    if not phrase_tokens:
        return 0.0
    title_tokens = token_set(title)
    return len(phrase_tokens & title_tokens) / max(len(phrase_tokens), 1)


def relevance_score(work: dict[str, Any], phrase: str) -> float:
    title = work.get("display_name") or ""
    title_norm = normalize_text(title)
    phrase_norm = normalize_text(phrase)
    overlap = overlap_ratio(title, phrase)
    score = 0.0
    if phrase_norm and title_norm == phrase_norm:
        score += 45.0
    elif phrase_norm and phrase_norm in title_norm:
        score += 28.0
    score += overlap * 26.0
    if len(token_set(phrase)) >= 3 and overlap < 0.34:
        score -= 20.0
    return score


def quality_gate(work: dict[str, Any], score: float) -> bool:
    """Strict quality gate.  Papers must clear a high bar to enter the atlas."""
    work_id = (work.get("id") or "").rsplit("/", 1)[-1]
    year = int(work.get("publication_year") or 0)
    citations = int(work.get("cited_by_count") or 0)
    venue = source_name(work)
    if work_id in BLOCKLIST_SOURCE_IDS:
        return False
    if year < MIN_YEAR or year > MAX_YEAR:
        return False
    if title_is_excluded(work.get("display_name") or ""):
        return False
    if venue_is_excluded(venue):
        return False
    # Core quality gate: must exceed age-adjusted citation threshold,
    # UNLESS the paper is in a top-tier venue with a strong relevance score.
    if citations < min_citations_for_year(year):
        if venue_score(venue) > 0 and score >= 45:
            pass  # top-venue paper with strong title match — allow
        else:
            return False
    return True


def selection_score(work: dict[str, Any], phrase: str) -> float:
    """Compute composite score.  Citation weight is uncapped to properly
    rank truly landmark papers above recent ones with modest citations."""
    citations = int(work.get("cited_by_count") or 0)
    venue = source_name(work)
    year = int(work.get("publication_year") or 0)
    age = max(MAX_YEAR - year, 0)
    # Uncapped citation component — truly epochal papers with 10k+ cites
    # should score much higher than papers with 100 cites.
    citation_component = math.log10(citations + 1) * 18.0
    recency_component = 3.0 if age <= 3 else 2.0 if age <= 8 else 1.0
    type_component = 5.0 if work.get("type") == "review" else 4.0 if work.get("type") == "proceedings-article" else 3.0
    return (
        relevance_score(work, phrase)
        + citation_component
        + venue_score(venue)
        + recency_component
        + type_component
    )


def search_topic(
    session: requests.Session,
    topic: dict[str, Any],
    per_page: int,
    per_query_keep: int,
    sleep_s: float,
) -> list[dict[str, Any]]:
    params = {
        "filter": f"title.search:{topic['phrase']},{BASE_FILTER}",
        "sort": "cited_by_count:desc",
        "per-page": per_page,
        "mailto": MAILTO,
    }
    payload = get_json(session, "https://api.openalex.org/works", params, sleep_s)
    results = []
    for work in payload.get("results", []):
        score = selection_score(work, topic["phrase"])
        if not quality_gate(work, score):
            continue
        work["_selection_score"] = round(score, 2)
        results.append(work)
    results.sort(key=lambda item: item["_selection_score"], reverse=True)
    return results[:per_query_keep]


def merge_source(
    merged: dict[str, dict[str, Any]],
    work: dict[str, Any],
    topic: dict[str, Any],
) -> None:
    source_id = (work.get("id") or "").rsplit("/", 1)[-1]
    if not source_id:
        return

    venue = source_name(work)
    doi_url = work.get("doi")
    if doi_url and doi_url.startswith("https://doi.org/"):
        clean_doi = doi_url
    elif doi_url:
        clean_doi = "https://doi.org/" + doi_url.removeprefix("doi:")
    else:
        clean_doi = None

    existing = merged.get(source_id)
    if existing is None:
        existing = {
            "id": source_id,
            "title": work.get("display_name") or "",
            "year": int(work.get("publication_year") or 0),
            "type": work.get("type") or "",
            "venue": venue,
            "authors": author_string(work),
            "cited_by_count": int(work.get("cited_by_count") or 0),
            "doi_url": clean_doi,
            "openalex_url": work.get("id"),
            "category_ids": set(),
            "corridor_ids": set(),
            "matched_topics": set(),
            "topic_scores": {},
            "selection_score": float(work.get("_selection_score") or 0.0),
        }
        merged[source_id] = existing
    else:
        existing["selection_score"] = max(existing["selection_score"], float(work.get("_selection_score") or 0.0))
        existing["cited_by_count"] = max(existing["cited_by_count"], int(work.get("cited_by_count") or 0))
        if not existing["venue"] and venue:
            existing["venue"] = venue
        if not existing["doi_url"] and clean_doi:
            existing["doi_url"] = clean_doi
        if not existing["authors"]:
            existing["authors"] = author_string(work)

    existing["category_ids"].update(topic["category_ids"])
    existing["corridor_ids"].add(topic["corridor_id"])
    existing["matched_topics"].add(topic["phrase"])
    existing["topic_scores"][topic["phrase"]] = max(
        float(existing["topic_scores"].get(topic["phrase"], 0.0)),
        float(work.get("_selection_score") or 0.0),
    )


def finalize_sources(merged: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    category_map = {item["id"]: item["label"] for item in CATEGORY_DEFS}
    corridor_map = {item["id"]: item["label"] for item in CORRIDOR_DEFS}
    sources = []
    for source in merged.values():
        category_ids = sorted(source["category_ids"])
        corridor_ids = sorted(source["corridor_ids"])
        topic_scores = source.get("topic_scores", {})
        matched_topics = [
            topic
            for topic, _score in sorted(
                topic_scores.items(),
                key=lambda item: (item[1], item[0]),
                reverse=True,
            )
        ]
        categories_text = ", ".join(category_map[item] for item in category_ids)
        corridors_text = ", ".join(corridor_map[item] for item in corridor_ids)
        note = (
            f"Selected for strong match to {', '.join(matched_topics[:3])}; "
            f"tagged as {categories_text} in {corridors_text}."
        )
        sources.append(
            {
                "id": source["id"],
                "title": source["title"],
                "year": source["year"],
                "type": source["type"],
                "venue": source["venue"],
                "authors": source["authors"],
                "cited_by_count": source["cited_by_count"],
                "doi_url": source["doi_url"],
                "openalex_url": source["openalex_url"],
                "category_ids": category_ids,
                "corridor_ids": corridor_ids,
                "matched_topics": matched_topics,
                "topic_scores": {topic: round(score, 2) for topic, score in topic_scores.items()},
                "selection_score": round(source["selection_score"], 2),
                "note": note,
            }
        )
    sources.sort(key=lambda item: (item["selection_score"], item["cited_by_count"]), reverse=True)
    return sources


def dedupe_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[tuple[str, int], dict[str, Any]] = {}
    for source in sources:
        key = (normalize_text(source["title"]), int(source.get("year") or 0))
        existing = deduped.get(key)
        if existing is None:
            topic_scores = dict(source.get("topic_scores", {}))
            for topic in source.get("matched_topics", []):
                topic_scores.setdefault(topic, float(source.get("selection_score") or 0.0))
            deduped[key] = {
                **source,
                "category_ids": set(source.get("category_ids", [])),
                "corridor_ids": set(source.get("corridor_ids", [])),
                "matched_topics": set(source.get("matched_topics", [])),
                "topic_scores": topic_scores,
            }
            continue

        existing["selection_score"] = max(existing.get("selection_score", 0), source.get("selection_score", 0))
        existing["cited_by_count"] = max(existing.get("cited_by_count", 0), source.get("cited_by_count", 0))
        existing["category_ids"].update(source.get("category_ids", []))
        existing["corridor_ids"].update(source.get("corridor_ids", []))
        existing["matched_topics"].update(source.get("matched_topics", []))
        for topic, score in source.get("topic_scores", {}).items():
            existing["topic_scores"][topic] = max(float(existing["topic_scores"].get(topic, 0.0)), float(score))
        for topic in source.get("matched_topics", []):
            existing["topic_scores"].setdefault(topic, float(source.get("selection_score") or 0.0))
        if source.get("type") == "manual":
            existing["type"] = "manual"
            existing["note"] = source.get("note", existing.get("note"))
            if source.get("doi_url"):
                existing["doi_url"] = source["doi_url"]
        if not existing.get("venue") and source.get("venue"):
            existing["venue"] = source["venue"]
        if not existing.get("authors") and source.get("authors"):
            existing["authors"] = source["authors"]
        if not existing.get("openalex_url") and source.get("openalex_url"):
            existing["openalex_url"] = source["openalex_url"]

    finalized = []
    for source in deduped.values():
        source["category_ids"] = sorted(source["category_ids"])
        source["corridor_ids"] = sorted(source["corridor_ids"])
        if not source.get("topic_scores"):
            source["topic_scores"] = {
                topic: float(source.get("selection_score") or 0.0)
                for topic in sorted(source.get("matched_topics", []))
            }
        source["matched_topics"] = [
            topic
            for topic, _score in sorted(
                source.get("topic_scores", {}).items(),
                key=lambda item: (item[1], item[0]),
                reverse=True,
            )
        ]
        finalized.append(source)
    finalized.sort(key=lambda item: (item["selection_score"], item["cited_by_count"]), reverse=True)
    return finalized


def build_group_counts(sources: list[dict[str, Any]], defs: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    grouped = []
    for item in defs:
        source_ids = [source["id"] for source in sources if item["id"] in source.get(key, [])]
        grouped.append(
            {
                "id": item["id"],
                "label": item["label"],
                "description": item["description"],
                "selected_count": len(source_ids),
                "source_ids": source_ids,
            }
        )
    return grouped


def build_payload(sources: list[dict[str, Any]]) -> dict[str, Any]:
    categories = build_group_counts(sources, CATEGORY_DEFS, "category_ids")
    corridors = build_group_counts(sources, CORRIDOR_DEFS, "corridor_ids")
    manual_count = len([source for source in sources if source.get("type") == "manual"])
    year_values = [source["year"] for source in sources if source.get("year")]
    return {
        "summary": {
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "total_unique_sources": len(sources),
            "scholarly_source_count": len(sources) - manual_count,
            "manual_source_count": manual_count,
            "category_count": len(categories),
            "corridor_count": len(corridors),
            "year_range": {
                "min": min(year_values) if year_values else MIN_YEAR,
                "max": max(year_values) if year_values else MAX_YEAR,
            },
            "selection_policy": [
                "OpenAlex topic harvesting across breakthrough families and technology corridors.",
                "Strict age-adjusted citation thresholds to ensure only high-impact papers enter the atlas.",
                "Priority for top-tier venues, landmark topic match, cross-domain breadth, and citation depth.",
                "Primary focus on 1995-present engineering and STEM literature with DOI-backed scholarly records.",
                "Manual anchors for Nobel-calibre and foundational papers that define what 'epochal' means.",
            ],
        },
        "categories": categories,
        "corridors": corridors,
        "sources": sources,
    }


def write_outputs(payload: dict[str, Any]) -> None:
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    JS_OUT.write_text(
        "window.EPOCHAL_PAPERS_ATLAS_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def source_link(source: dict[str, Any]) -> str:
    return source.get("doi_url") or source.get("openalex_url") or "N/A"


def source_topic_scores(source: dict[str, Any]) -> dict[str, float]:
    topic_scores = {topic: float(score) for topic, score in source.get("topic_scores", {}).items()}
    if topic_scores:
        return topic_scores
    return {
        topic: float(source.get("selection_score") or 0.0)
        for topic in source.get("matched_topics", [])
    }


def primary_topic_for_corridor(source: dict[str, Any], corridor_id: str) -> str | None:
    candidates = [
        (topic, score)
        for topic, score in source_topic_scores(source).items()
        if TOPIC_TO_CORRIDOR.get(topic) == corridor_id
    ]
    if not candidates:
        return None
    candidates.sort(
        key=lambda item: (item[1], len(token_set(item[0])), item[0]),
        reverse=True,
    )
    return candidates[0][0]


def canonical_sort_key(source: dict[str, Any], corridor_id: str) -> tuple[float, int, int, int, int]:
    primary_topic = primary_topic_for_corridor(source, corridor_id)
    topic_score = float(source_topic_scores(source).get(primary_topic or "", source.get("selection_score") or 0.0))
    source_type = source.get("type") or ""
    type_rank = 4 if source_type == "manual" else 3 if source_type in {"article", "proceedings-article"} else 1
    venue_rank = 1 if venue_score(source.get("venue") or "") > 0 else 0
    citations = int(source.get("cited_by_count") or 0)
    year = int(source.get("year") or 0)
    return (topic_score, venue_rank, type_rank, citations, -year)


def canonical_candidate(source: dict[str, Any]) -> bool:
    if source.get("type") == "manual":
        return True
    year = int(source.get("year") or 0)
    citations = int(source.get("cited_by_count") or 0)
    score = float(source.get("selection_score") or 0.0)
    venue = source.get("venue") or ""
    source_type = source.get("type") or ""
    if venue_is_excluded(venue):
        return False
    if year >= 2025 and citations < 30:
        return False
    if citations < 80 and score < 65:
        return False
    if venue_score(venue) == 0 and citations < 150:
        return False
    if source_type == "review" and citations < 500 and score < 90:
        return False
    return True


def build_canonical_list(sources: list[dict[str, Any]]) -> dict[str, Any]:
    manual = [source for source in sources if source.get("type") == "manual"]
    manual.sort(key=lambda item: canonical_sort_key(item, (item.get("corridor_ids") or [""])[0]), reverse=True)
    selected_by_id: dict[str, dict[str, Any]] = {source["id"]: source for source in manual}
    corridor_lists = []

    for corridor in CORRIDOR_DEFS:
        corridor_id = corridor["id"]
        manual_picks = [source for source in manual if corridor_id in source.get("corridor_ids", [])]
        manual_picks.sort(key=lambda item: canonical_sort_key(item, corridor_id), reverse=True)
        picks = list(manual_picks)
        pick_ids = {source["id"] for source in picks}
        covered_topics = {
            topic
            for source in manual_picks
            for topic in source.get("matched_topics", [])
            if TOPIC_TO_CORRIDOR.get(topic) == corridor_id
        }
        topic_pick_counts = {topic: 1 for topic in covered_topics}
        candidates = [
            source
            for source in sources
            if corridor_id in source.get("corridor_ids", [])
            and source.get("type") != "manual"
            and canonical_candidate(source)
        ]
        candidates.sort(key=lambda item: canonical_sort_key(item, corridor_id), reverse=True)

        for source in candidates:
            primary_topic = primary_topic_for_corridor(source, corridor_id)
            if source["id"] in pick_ids or not primary_topic or primary_topic in covered_topics:
                continue
            picks.append(source)
            pick_ids.add(source["id"])
            covered_topics.add(primary_topic)
            topic_pick_counts[primary_topic] = topic_pick_counts.get(primary_topic, 0) + 1
            selected_by_id.setdefault(source["id"], source)
            if len(picks) >= 10:
                break

        if len(picks) < 10:
            for source in candidates:
                primary_topic = primary_topic_for_corridor(source, corridor_id)
                if source["id"] in pick_ids:
                    continue
                if primary_topic and topic_pick_counts.get(primary_topic, 0) >= 2:
                    continue
                picks.append(source)
                pick_ids.add(source["id"])
                if primary_topic:
                    topic_pick_counts[primary_topic] = topic_pick_counts.get(primary_topic, 0) + 1
                selected_by_id.setdefault(source["id"], source)
                if len(picks) >= 10:
                    break

        corridor_lists.append(
            {
                "id": corridor_id,
                "label": corridor["label"],
                "description": corridor["description"],
                "anchor_source_ids": [source["id"] for source in manual_picks],
                "topic_coverage": sorted(covered_topics),
                "source_ids": [source["id"] for source in picks],
            }
        )

    selected_sources = sorted(
        selected_by_id.values(),
        key=lambda item: (item.get("selection_score", 0), item.get("cited_by_count", 0)),
        reverse=True,
    )
    return {
        "summary": {
            "manual_anchor_count": len(manual),
            "corridor_count": len(corridor_lists),
            "total_unique_sources": len(selected_sources),
        },
        "manual_anchor_ids": [source["id"] for source in manual],
        "corridor_lists": corridor_lists,
        "sources": selected_sources,
    }


def write_canonical_outputs(canonical: dict[str, Any]) -> None:
    CANONICAL_JSON_OUT.write_text(json.dumps(canonical, ensure_ascii=False, indent=2), encoding="utf-8")
    CANONICAL_JS_OUT.write_text(
        "window.EPOCHAL_PAPERS_ATLAS_CANONICAL = " + json.dumps(canonical, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the epochal engineering papers atlas dataset.")
    parser.add_argument("--per-page", type=int, default=28, help="OpenAlex results requested per topic query.")
    parser.add_argument("--per-query-keep", type=int, default=8, help="Top results retained per topic after filtering.")
    parser.add_argument("--sleep", type=float, default=0.12, help="Sleep between uncached OpenAlex requests.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    session = requests.Session()
    merged: dict[str, dict[str, Any]] = {}

    for topic in TOPIC_QUERIES:
        works = search_topic(
            session=session,
            topic=topic,
            per_page=args.per_page,
            per_query_keep=args.per_query_keep,
            sleep_s=args.sleep,
        )
        for work in works:
            merge_source(merged, work, topic)

    sources = dedupe_sources(finalize_sources(merged) + MANUAL_SOURCES)
    payload = build_payload(sources)
    write_outputs(payload)
    canonical = build_canonical_list(sources)
    write_canonical_outputs(canonical)

    summary = payload["summary"]
    print(f"Generated {summary['total_unique_sources']} unique sources.")
    print(f"Families: {summary['category_count']} | Corridors: {summary['corridor_count']}")
    print(f"Year range: {summary['year_range']['min']} - {summary['year_range']['max']}")
    print(f"Canonical list size: {canonical['summary']['total_unique_sources']}")
    if summary["total_unique_sources"] < 800:
        print("Warning: total source count is below 800. Increase topic breadth or per-query retention.")


if __name__ == "__main__":
    main()
