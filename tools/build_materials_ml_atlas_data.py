from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import time
import unicodedata
import urllib.parse
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".cache" / "openalex"
JSON_OUT = ROOT / "data" / "atlas-sources.json"
JS_OUT = ROOT / "data" / "atlas-sources.js"
MAILTO = "materials-ml-atlas@example.com"

BASE_FILTER = "type:article|review,has_doi:true,is_retracted:false,language:en"
MIN_YEAR = 2010

QUALITY_SOURCE_PATTERNS = tuple(
    pattern.lower()
    for pattern in [
        "nature",
        "science",
        "cell",
        "npj computational materials",
        "computational materials science",
        "physical review",
        "advanced materials",
        "advanced science",
        "advanced functional materials",
        "advanced energy materials",
        "advanced optical materials",
        "chemical reviews",
        "chemical society reviews",
        "chemistry of materials",
        "acs catalysis",
        "acs energy letters",
        "materials horizons",
        "journal of materials chemistry",
        "journal of chemical physics",
        "acta materialia",
        "scripta materialia",
        "progress in materials science",
        "current opinion in solid state and materials science",
        "journal of physics: materials",
        "apl materials",
        "digital discovery",
        "infomat",
        "matter",
        "nano letters",
        "small",
        "small methods",
        "microscopy and microanalysis",
        "ultramicroscopy",
        "nanoscale horizons",
        "applied physics reviews",
        "machine learning: science and technology",
        "communications materials",
        "nature communications",
        "nature machine intelligence",
        "nature materials",
        "nature reviews materials",
        "nature reviews chemistry",
        "nature computational science",
        "joule",
        "energy & environmental science",
        "journal of power sources",
        "journal of energy chemistry",
        "materials & design",
        "metallurgical and materials transactions",
        "journal of materials informatics",
        "mrs bulletin",
        "ieee transactions on semiconductor manufacturing",
        "ieee transactions on automation science and engineering",
        "journal of manufacturing processes",
        "additive manufacturing",
        "surface science reports",
        "accounts of chemical research",
        "national science review",
        "acs applied materials",
        "journal of membrane science",
        "materials today",
        "battery energy",
        "energy storage materials",
        "journal of alloys and compounds",
        "ceramics international",
        "cement and concrete research",
        "corrosion science",
    ]
)

EXCLUDE_TITLE_PATTERNS = tuple(
    pattern.lower()
    for pattern in [
        "corrigendum",
        "correction:",
        "erratum",
        "editorial",
        "preface",
        "special issue",
        "supplemental material",
        "diabetes",
        "cognition",
        "cognitive",
        "psychology",
        "psychopathology",
        "urine",
        "phylogenetic",
        "breast cancer",
        "lung tumor",
        "logistic regression",
        "speech recognition",
        "drug formulation",
        "soil science",
        "protein fitness landscape",
        "social media",
        "covid",
        "mouse",
        "neuroscience",
        "eggshell",
        "biomedical science & research",
    ]
)

COMMON_SIGNAL_TERMS = [
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data-driven",
    "informatics",
    "neural network",
    "graph neural",
    "language model",
    "word embeddings",
    "bayesian optimization",
    "active learning",
    "generative",
    "diffusion",
    "self-driving",
    "virtual metrology",
]

CATEGORIES: list[dict[str, Any]] = [
    {
        "id": "field_overviews",
        "label": "Field Overviews and Strategic Framing",
        "description": "High-level reviews, position papers, and strategic syntheses defining the scope of ML-driven materials science.",
        "target": 26,
        "title_pages": 2,
        "title_phrases": [
            "materials informatics",
            "machine learning materials",
            "data-driven materials",
            "artificial intelligence materials science",
            "foundation models materials",
        ],
        "fallback_queries": [
            "materials informatics machine learning review",
            "artificial intelligence materials science review",
        ],
        "required_groups": [
            ["material"],
            ["machine learning", "informatics", "artificial intelligence", "data-driven", "foundation model"],
        ],
        "priority_terms": ["materials informatics", "machine learning materials", "review", "foundation models"],
        "min_cites": 8,
    },
    {
        "id": "data_infrastructure",
        "label": "Data Infrastructure, Databases, and Benchmarks",
        "description": "Evidence bases, open databases, FAIR systems, and benchmark papers that define reusable data infrastructure.",
        "target": 24,
        "title_pages": 2,
        "title_phrases": [
            "materials project",
            "matbench",
            "jarvis leaderboard",
            "nomad",
            "open quantum materials database",
            "aflow",
            "polymer genome",
        ],
        "fallback_queries": [
            "materials benchmark machine learning",
            "materials database machine learning benchmark",
        ],
        "required_groups": [
            ["materials", "matbench", "jarvis", "nomad", "oqmd", "aflow", "polymer"],
            ["benchmark", "database", "dataset", "leaderboard", "platform", "genome", "fair", "repository"],
        ],
        "signal_terms": ["materials project", "matbench", "jarvis", "nomad", "open quantum materials database", "aflow", "polymer genome", "benchmark", "leaderboard", "database", "dataset", "fair"],
        "priority_terms": ["matbench", "materials project", "jarvis", "nomad", "benchmark", "leaderboard"],
        "min_cites": 6,
    },
    {
        "id": "crystal_prediction",
        "label": "Composition, Crystal, and Property Prediction",
        "description": "Forward models mapping composition or structure to thermodynamic, electronic, or mechanical properties.",
        "target": 28,
        "title_pages": 2,
        "title_phrases": [
            "crystal graph",
            "materials property prediction",
            "band gap prediction",
            "formation energy prediction",
            "graph neural network materials",
            "composition-based machine learning",
        ],
        "fallback_queries": [
            "crystal property prediction materials machine learning",
            "band gap formation energy machine learning materials",
        ],
        "required_groups": [
            ["material", "crystal", "composition", "band gap", "formation energy"],
            ["prediction", "property", "graph", "neural network", "machine learning"],
        ],
        "priority_terms": ["crystal graph", "band gap", "formation energy", "property prediction"],
        "min_cites": 10,
    },
    {
        "id": "inverse_design",
        "label": "Inverse Design and Generative Discovery",
        "description": "Target-to-structure, target-to-composition, and target-to-process generation for candidate discovery.",
        "target": 24,
        "title_pages": 2,
        "title_phrases": [
            "inverse design materials",
            "inverse molecular design",
            "generative models for materials",
            "materials discovery generative",
            "diffusion model materials",
        ],
        "fallback_queries": [
            "inverse design generative model materials",
            "materials discovery generative model",
        ],
        "required_groups": [
            ["inverse", "generative", "diffusion", "design"],
            ["material", "molecular", "microstructure", "crystal", "reticular", "discovery"],
        ],
        "signal_terms": ["inverse design", "generative", "diffusion", "machine learning", "data-driven", "reinforcement", "bayesian optimization"],
        "priority_terms": ["inverse design", "generative", "diffusion", "materials discovery"],
        "min_cites": 6,
    },
    {
        "id": "scientific_ml",
        "label": "Scientific ML and Interatomic Potentials",
        "description": "Machine-learned interatomic potentials, force fields, operator learning, and simulation surrogates.",
        "target": 28,
        "title_pages": 2,
        "title_phrases": [
            "interatomic potential",
            "machine learning potentials",
            "force field materials",
            "neural network potential",
            "atomistic simulation machine learning",
            "universal interatomic potential",
        ],
        "fallback_queries": [
            "machine learning interatomic potential materials review",
            "scientific machine learning materials simulation",
        ],
        "required_groups": [
            ["interatomic", "potential", "force field", "atomistic", "simulation", "operator"],
            ["material", "alloy", "periodic", "molecule", "chemistry"],
        ],
        "signal_terms": ["machine learning", "machine-learned", "neural network", "deep potential", "gaussian process", "graph neural", "universal interatomic potential", "scientific machine learning"],
        "priority_terms": ["interatomic potential", "force field", "atomistic simulation", "universal"],
        "min_cites": 8,
    },
    {
        "id": "trust_uq",
        "label": "Uncertainty, OOD Robustness, and Reproducibility",
        "description": "Calibration, model reliability, distribution shift, prospective testing, and methodological rigor.",
        "target": 20,
        "title_pages": 2,
        "title_phrases": [
            "uncertainty quantification materials",
            "out-of-distribution materials",
            "robust materials machine learning",
            "trustworthy materials ai",
            "crystal stability predictions",
        ],
        "fallback_queries": [
            "uncertainty quantification machine learning materials",
            "out-of-distribution materials machine learning",
        ],
        "required_groups": [
            ["uncertainty", "out-of-distribution", "ood", "robust", "trust", "stability"],
            ["material", "machine learning", "model", "prediction"],
        ],
        "priority_terms": ["uncertainty", "out-of-distribution", "trustworthy", "stability predictions"],
        "min_cites": 5,
    },
    {
        "id": "autonomous_labs",
        "label": "Active Learning and Self-Driving Laboratories",
        "description": "Closed-loop discovery, autonomous experimentation, and machine-guided experiment selection.",
        "target": 22,
        "title_pages": 2,
        "title_phrases": [
            "self-driving laboratories",
            "autonomous materials discovery",
            "closed-loop materials discovery",
            "active learning materials discovery",
            "robotic materials",
        ],
        "fallback_queries": [
            "self-driving laboratory materials science review",
            "autonomous materials discovery active learning",
        ],
        "required_groups": [
            ["self-driving", "autonomous", "closed-loop", "active learning", "bayesian", "robotic"],
            ["materials", "chemistry", "discovery", "synthesis", "laboratory", "electrolyte", "catalysis", "polymer"],
        ],
        "signal_terms": ["self-driving", "autonomous", "closed-loop", "active learning", "bayesian optimization", "robotic"],
        "priority_terms": ["self-driving", "autonomous", "closed-loop", "active learning"],
        "min_cites": 5,
    },
    {
        "id": "microscopy_characterization",
        "label": "Microscopy, Imaging, and Characterization",
        "description": "Electron microscopy, image-based microstructure learning, segmentation, and nanoscale characterization.",
        "target": 26,
        "title_pages": 2,
        "title_phrases": [
            "electron microscopy machine learning",
            "machine learning in scanning transmission electron microscopy",
            "microstructure segmentation materials",
            "microstructure machine learning",
            "defect detection materials",
            "nanocharacterization machine learning",
        ],
        "fallback_queries": [
            "machine learning microscopy materials characterization review",
            "deep learning microstructure image materials review",
        ],
        "required_groups": [
            ["microscopy", "microstructure", "tem", "sem", "stem", "micrograph", "nanocharacterization", "defect"],
            ["machine learning", "deep learning", "segmentation", "characterization", "analysis"],
        ],
        "priority_terms": ["electron microscopy", "microstructure", "segmentation", "nanocharacterization"],
        "min_cites": 5,
    },
    {
        "id": "spectroscopy_diffraction",
        "label": "Spectroscopy, Diffraction, and Scattering",
        "description": "XRD, Raman, XAS, and related data-driven analysis methods for structural and chemical inference.",
        "target": 22,
        "title_pages": 2,
        "title_phrases": [
            "raman spectroscopy machine learning",
            "x-ray diffraction machine learning",
            "materials spectroscopy machine learning",
            "diffraction machine learning materials",
            "xas machine learning",
            "spectroscopy machine learning materials",
        ],
        "fallback_queries": [
            "machine learning spectroscopy materials review",
            "machine learning diffraction materials review",
        ],
        "required_groups": [
            ["spectroscopy", "raman", "x-ray diffraction", "xrd", "diffraction", "xas", "ftir", "xps"],
            ["machine learning", "deep learning", "analysis", "materials"],
        ],
        "priority_terms": ["raman", "x-ray diffraction", "spectroscopy", "xas"],
        "min_cites": 4,
    },
    {
        "id": "manufacturing_semiconductor",
        "label": "Manufacturing, Semiconductor, and Process Control",
        "description": "Virtual metrology, yield learning, fault detection, and process monitoring in industrial settings.",
        "target": 22,
        "title_pages": 2,
        "title_phrases": [
            "semiconductor manufacturing machine learning",
            "virtual metrology",
            "wafer map",
            "fault detection semiconductor",
            "process monitoring semiconductor",
            "optical metrology ai",
        ],
        "fallback_queries": [
            "machine learning semiconductor manufacturing review",
            "virtual metrology semiconductor machine learning",
        ],
        "required_groups": [
            ["semiconductor", "virtual metrology", "wafer", "yield", "process monitoring", "fault detection", "manufacturing", "optical metrology"],
            ["machine learning", "deep learning", "ai", "prediction", "metrology"],
        ],
        "priority_terms": ["virtual metrology", "semiconductor", "wafer", "fault detection", "yield"],
        "min_cites": 4,
    },
    {
        "id": "additive_manufacturing",
        "label": "Additive Manufacturing and Process-Structure Learning",
        "description": "Powder-bed, melt-pool, and build-process modeling for quality, microstructure, and property control.",
        "target": 22,
        "title_pages": 2,
        "title_phrases": [
            "additive manufacturing machine learning",
            "powder bed fusion machine learning",
            "laser powder bed fusion machine learning",
            "3d printing machine learning materials",
            "data-driven additive manufacturing",
        ],
        "fallback_queries": [
            "machine learning additive manufacturing materials review",
            "artificial intelligence additive manufacturing metals review",
        ],
        "required_groups": [
            ["additive manufacturing", "powder bed", "laser powder", "3d printing", "directed energy deposition"],
            ["machine learning", "deep learning", "data-driven", "microstructure", "materials"],
        ],
        "priority_terms": ["additive manufacturing", "powder bed fusion", "laser powder bed fusion"],
        "min_cites": 4,
    },
    {
        "id": "polymers",
        "label": "Polymers, Soft Matter, and Macromolecular Design",
        "description": "Polymer informatics, sequence-to-property modeling, and soft-material design workflows.",
        "target": 26,
        "title_pages": 2,
        "title_phrases": [
            "polymer informatics",
            "machine learning polymers",
            "polymer design machine learning",
            "polymer genome",
            "soft materials machine learning",
        ],
        "fallback_queries": [
            "machine learning polymers materials review",
            "polymer informatics review",
        ],
        "required_groups": [
            ["polymer", "polymers", "polymeric", "soft material", "macromolecular"],
            ["informatics", "machine learning", "design", "property", "materials"],
        ],
        "priority_terms": ["polymer informatics", "polymer genome", "machine learning polymers"],
        "min_cites": 5,
    },
    {
        "id": "batteries",
        "label": "Batteries, Electrolytes, and Electrochemistry",
        "description": "Battery materials discovery, electrolyte screening, degradation modeling, and electrochemical optimization.",
        "target": 26,
        "title_pages": 2,
        "title_phrases": [
            "battery materials machine learning",
            "solid electrolyte machine learning",
            "battery informatics",
            "electrochemistry machine learning materials",
            "ionic conductivity machine learning",
            "lithium battery machine learning",
        ],
        "fallback_queries": [
            "machine learning battery materials review",
            "battery materials discovery machine learning",
        ],
        "required_groups": [
            ["battery", "electrolyte", "electrochem", "lithium", "ionic conductivity", "solid-state"],
            ["machine learning", "informatics", "discovery", "materials", "prediction"],
        ],
        "priority_terms": ["battery materials", "solid electrolyte", "battery informatics", "ionic conductivity"],
        "min_cites": 5,
    },
    {
        "id": "catalysis",
        "label": "Catalysis, Surfaces, and Interfaces",
        "description": "Catalyst design, adsorption modeling, electrocatalysis, and surface chemistry with ML support.",
        "target": 24,
        "title_pages": 2,
        "title_phrases": [
            "machine learning catalysis",
            "heterogeneous catalysis machine learning",
            "electrocatalyst machine learning",
            "photocatalyst machine learning",
            "surface science machine learning",
        ],
        "fallback_queries": [
            "machine learning catalysis materials review",
            "machine learning heterogeneous catalysis review",
        ],
        "required_groups": [
            ["catalysis", "catalyst", "electrocatalyst", "photocatalyst", "adsorption", "surface"],
            ["machine learning", "informatics", "design", "prediction"],
        ],
        "priority_terms": ["catalysis", "electrocatalyst", "heterogeneous catalysis", "surface science"],
        "min_cites": 5,
    },
    {
        "id": "alloys_metallurgy",
        "label": "Alloys, Metallurgy, and Phase-Space Exploration",
        "description": "High-entropy alloys, steels, superalloys, phase prediction, and metallurgy-aware materials informatics.",
        "target": 24,
        "title_pages": 2,
        "title_phrases": [
            "machine learning for alloys",
            "high entropy alloys machine learning",
            "materials informatics metallurgy",
            "phase prediction alloys machine learning",
            "steel machine learning materials",
        ],
        "fallback_queries": [
            "machine learning alloys materials review",
            "high entropy alloys machine learning review",
        ],
        "required_groups": [
            ["alloy", "alloys", "high entropy", "metallurgy", "steel", "superalloy", "phase"],
            ["machine learning", "informatics", "prediction", "design", "materials"],
        ],
        "priority_terms": ["alloys", "high entropy", "metallurgy", "phase prediction"],
        "min_cites": 5,
    },
    {
        "id": "microstructure_mechanics",
        "label": "Microstructure, Mechanics, Defects, and Reliability",
        "description": "Microstructure-property links, defect-aware learning, fracture, fatigue, and reliability prediction.",
        "target": 24,
        "title_pages": 2,
        "title_phrases": [
            "microstructure property machine learning",
            "fatigue machine learning materials",
            "fracture machine learning materials",
            "grain structure machine learning",
            "defect prediction materials",
        ],
        "fallback_queries": [
            "machine learning microstructure materials review",
            "materials mechanics machine learning review",
        ],
        "required_groups": [
            ["microstructure", "grain", "defect", "mechanical", "fracture", "fatigue", "reliability"],
            ["machine learning", "deep learning", "prediction", "property"],
        ],
        "priority_terms": ["microstructure", "fracture", "fatigue", "defect prediction"],
        "min_cites": 4,
    },
    {
        "id": "literature_kg",
        "label": "Literature Mining, Knowledge Graphs, and LLMs",
        "description": "Text extraction, knowledge graph induction, synthesis-route mining, and literature-based reasoning.",
        "target": 22,
        "title_pages": 2,
        "title_phrases": [
            "materials science literature",
            "materials knowledge graph",
            "materials text mining",
            "language models materials science",
            "word embeddings materials science",
        ],
        "fallback_queries": [
            "materials science literature mining machine learning",
            "materials knowledge graph machine learning review",
        ],
        "required_groups": [
            ["literature", "text mining", "knowledge graph", "information extraction", "language model", "word embeddings"],
            ["materials", "science", "synthesis", "property", "materials science"],
        ],
        "priority_terms": ["knowledge graph", "language models", "word embeddings", "literature"],
        "min_cites": 4,
    },
    {
        "id": "quantum_2d",
        "label": "Electronic, Quantum, 2D, and Photonic Materials",
        "description": "Quantum materials, semiconducting crystals, 2D systems, and photonic structures with ML-assisted discovery.",
        "target": 22,
        "title_pages": 2,
        "title_phrases": [
            "quantum materials machine learning",
            "2d materials machine learning",
            "topological materials machine learning",
            "photonic materials machine learning",
            "semiconductor materials machine learning",
        ],
        "fallback_queries": [
            "machine learning quantum materials review",
            "2D materials machine learning review",
        ],
        "required_groups": [
            ["quantum", "2d", "two-dimensional", "topological", "photonic", "semiconductor"],
            ["machine learning", "materials", "discovery", "prediction", "design"],
        ],
        "priority_terms": ["quantum materials", "2d materials", "topological", "photonic"],
        "min_cites": 4,
    },
    {
        "id": "biomaterials",
        "label": "Biomaterials and Bioinspired Materials",
        "description": "Implants, bioceramics, tissue-facing materials, and bioinspired design with ML-guided optimization.",
        "target": 18,
        "title_pages": 2,
        "title_phrases": [
            "biomaterials machine learning",
            "bioinspired materials machine learning",
            "implant materials machine learning",
            "tissue engineering materials machine learning",
            "bioceramic machine learning",
        ],
        "fallback_queries": [
            "machine learning biomaterials review",
            "bioinspired materials machine learning review",
        ],
        "required_groups": [
            ["biomaterial", "bioinspired", "implant", "tissue engineering", "bioceramic", "biomedical"],
            ["machine learning", "materials", "design", "prediction", "informatics"],
        ],
        "priority_terms": ["biomaterials", "bioinspired", "implant", "tissue engineering"],
        "min_cites": 3,
    },
    {
        "id": "nonhot_materials",
        "label": "Less-Discussed Branches: Ceramics, Glass, Cement, Corrosion, Tribology, Nuclear",
        "description": "Important but less-hyped materials branches that remain underrepresented in mainstream ML narratives.",
        "target": 24,
        "title_pages": 2,
        "title_phrases": [
            "ceramics informatics",
            "glass materials machine learning",
            "cement materials machine learning",
            "corrosion machine learning materials",
            "tribology machine learning materials",
            "nuclear materials machine learning",
        ],
        "fallback_queries": [
            "machine learning ceramics materials review",
            "machine learning corrosion materials review",
        ],
        "required_groups": [
            ["ceramic", "glass", "cement", "corrosion", "tribology", "nuclear material", "refractory", "geologic"],
            ["machine learning", "data-driven", "materials", "prediction", "informatics"],
        ],
        "priority_terms": ["ceramics", "glass", "cement", "corrosion", "tribology", "nuclear materials"],
        "min_cites": 2,
    },
    {
        "id": "sustainability",
        "label": "Sustainability, Critical Materials, and Lifecycle Constraints",
        "description": "Carbon, supply risk, recycling, and sustainability-aware optimization of materials discovery pipelines.",
        "target": 16,
        "title_pages": 2,
        "title_phrases": [
            "sustainable materials machine learning",
            "carbon footprint materials",
            "critical materials machine learning",
            "recycling materials machine learning",
            "green materials informatics",
        ],
        "fallback_queries": [
            "sustainable materials discovery machine learning review",
            "critical materials supply machine learning review",
        ],
        "required_groups": [
            ["sustainable", "carbon", "critical material", "recycling", "life cycle", "green"],
            ["materials", "machine learning", "discovery", "informatics", "optimization"],
        ],
        "priority_terms": ["sustainable materials", "carbon", "critical materials", "recycling"],
        "min_cites": 3,
    },
    {
        "id": "composites_metamaterials",
        "label": "Composites, Metamaterials, and Architected Matter",
        "description": "Composite informatics, metamaterial inverse design, and architected-structure optimization.",
        "target": 22,
        "title_pages": 2,
        "title_phrases": [
            "composite materials machine learning",
            "metamaterials inverse design",
            "architected materials machine learning",
            "lattice materials machine learning",
            "composite informatics",
        ],
        "fallback_queries": [
            "machine learning composites materials review",
            "metamaterials inverse design machine learning review",
        ],
        "required_groups": [
            ["composite", "metamaterial", "architected", "lattice", "mechanical metamaterial"],
            ["machine learning", "inverse design", "materials", "prediction", "informatics"],
        ],
        "priority_terms": ["metamaterials", "inverse design", "composite", "architected"],
        "min_cites": 3,
    },
]

MANUAL_SOURCES: list[dict[str, Any]] = [
    {
        "id": "manual-materials-project-docs",
        "title": "Materials Project: ML and AI applications documentation",
        "year": 2026,
        "venue": "Materials Project",
        "type": "official-resource",
        "category_ids": ["data_infrastructure"],
        "url": "https://docs.materialsproject.org/services/ml-and-ai-applications",
        "note": "Official documentation accessed on March 16, 2026.",
    },
    {
        "id": "manual-matbench-docs",
        "title": "Matbench documentation",
        "year": 2026,
        "venue": "Materials Project",
        "type": "official-resource",
        "category_ids": ["data_infrastructure", "trust_uq"],
        "url": "https://docs.materialsproject.org/services/ml-and-ai-applications/matbench",
        "note": "Official benchmark documentation accessed on March 16, 2026.",
    },
    {
        "id": "manual-jarvis-leaderboard",
        "title": "JARVIS-Leaderboard official site",
        "year": 2026,
        "venue": "NIST JARVIS",
        "type": "official-resource",
        "category_ids": ["data_infrastructure", "trust_uq"],
        "url": "https://pages.nist.gov/jarvis_leaderboard/",
        "note": "Official benchmark leaderboard accessed on March 16, 2026.",
    },
    {
        "id": "manual-nomad",
        "title": "NOMAD Laboratory and FAIR materials data infrastructure",
        "year": 2026,
        "venue": "NOMAD",
        "type": "official-resource",
        "category_ids": ["data_infrastructure"],
        "url": "https://nomad-lab.eu/nomad-lab/",
        "note": "Official platform page accessed on March 16, 2026.",
    },
    {
        "id": "manual-openalex",
        "title": "OpenAlex API",
        "year": 2026,
        "venue": "OpenAlex",
        "type": "official-resource",
        "category_ids": ["field_overviews"],
        "url": "https://api.openalex.org/",
        "note": "Used only as metadata infrastructure for bibliography assembly.",
    },
    {
        "id": "manual-oqmd",
        "title": "Open Quantum Materials Database",
        "year": 2026,
        "venue": "OQMD",
        "type": "official-resource",
        "category_ids": ["data_infrastructure"],
        "url": "https://oqmd.org/",
        "note": "Official platform page accessed on March 16, 2026.",
    },
    {
        "id": "manual-aflow",
        "title": "AFLOW and AFLOWlib materials data infrastructure",
        "year": 2026,
        "venue": "AFLOW",
        "type": "official-resource",
        "category_ids": ["data_infrastructure"],
        "url": "https://aflowlib.org/",
        "note": "Official platform page accessed on March 16, 2026.",
    },
    {
        "id": "manual-materials-cloud",
        "title": "Materials Cloud platform",
        "year": 2026,
        "venue": "Materials Cloud",
        "type": "official-resource",
        "category_ids": ["data_infrastructure"],
        "url": "https://www.materialscloud.org/",
        "note": "Official platform page accessed on March 16, 2026.",
    },
    {
        "id": "manual-optimade",
        "title": "OPTIMADE specification",
        "year": 2026,
        "venue": "OPTIMADE",
        "type": "official-resource",
        "category_ids": ["data_infrastructure"],
        "url": "https://www.optimade.org/",
        "note": "Official interoperability specification accessed on March 16, 2026.",
    },
    {
        "id": "manual-matminer",
        "title": "matminer documentation",
        "year": 2026,
        "venue": "matminer",
        "type": "official-resource",
        "category_ids": ["data_infrastructure", "field_overviews"],
        "url": "https://hackingmaterials.lbl.gov/matminer/",
        "note": "Official toolkit documentation accessed on March 16, 2026.",
    },
    {
        "id": "manual-mdf",
        "title": "Materials Data Facility",
        "year": 2026,
        "venue": "Materials Data Facility",
        "type": "official-resource",
        "category_ids": ["data_infrastructure"],
        "url": "https://materialsdatafacility.org/",
        "note": "Official platform page accessed on March 16, 2026.",
    },
]


def clean_text(value: str | None) -> str:
    return unicodedata.normalize("NFKC", value or "").strip()


def slugify_url(url: str) -> Path:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{digest}.json"


def cached_json(url: str, refresh: bool = False) -> dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = slugify_url(url)
    if cache_file.exists() and not refresh:
        return json.loads(cache_file.read_text(encoding="utf-8"))

    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            payload = response.json()
            cache_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            time.sleep(0.1)
            return payload
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.2 * (attempt + 1))

    if last_error is not None:
        raise last_error
    raise RuntimeError("OpenAlex request failed without an explicit exception.")


def api_filter(filter_expr: str, per_page: int, page: int) -> str:
    encoded = urllib.parse.quote(f"{BASE_FILTER},{filter_expr}", safe=":,|")
    mailto = urllib.parse.quote(MAILTO)
    return f"https://api.openalex.org/works?filter={encoded}&per-page={per_page}&page={page}&mailto={mailto}"


def query_openalex(filter_expr: str, pages: int, refresh: bool) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for page in range(1, pages + 1):
        url = api_filter(filter_expr, per_page=25, page=page)
        try:
            payload = cached_json(url, refresh=refresh)
        except Exception:  # noqa: BLE001
            continue
        results.extend(payload.get("results", []))
    return results


def source_name(work: dict[str, Any]) -> str:
    source = ((work.get("primary_location") or {}).get("source") or {}).get("display_name")
    return clean_text(source)


def title_text(work: dict[str, Any]) -> str:
    return clean_text(work.get("title"))


def title_ok(title: str, category: dict[str, Any]) -> bool:
    lowered = title.lower()
    if any(blocked in lowered for blocked in EXCLUDE_TITLE_PATTERNS):
        return False
    if not all(any(term in lowered for term in group) for group in category["required_groups"]):
        return False

    signal_terms = category.get("signal_terms") or COMMON_SIGNAL_TERMS
    return any(term in lowered for term in signal_terms)


def quality_score(work: dict[str, Any], category: dict[str, Any]) -> int:
    title = title_text(work).lower()
    venue = source_name(work).lower()
    score = 0

    if any(pattern in venue for pattern in QUALITY_SOURCE_PATTERNS):
        score += 4
    if work.get("type") == "review":
        score += 3

    cited_by = int(work.get("cited_by_count") or 0)
    if cited_by >= 500:
        score += 4
    elif cited_by >= 200:
        score += 3
    elif cited_by >= 75:
        score += 2
    elif cited_by >= category["min_cites"]:
        score += 1

    for term in category["priority_terms"]:
        if term in title:
            score += 2

    if "review" in title:
        score += 1

    publication_year = int(work.get("publication_year") or 0)
    if publication_year >= 2024:
        score += 2
    elif publication_year >= 2020:
        score += 1

    return score


def format_authors(work: dict[str, Any]) -> str:
    names = [clean_text((entry.get("author") or {}).get("display_name")) for entry in work.get("authorships", [])]
    names = [name for name in names if name]
    if not names:
        return ""
    if len(names) <= 3:
        return ", ".join(names)
    return ", ".join(names[:3]) + ", et al."


def openalex_id(work: dict[str, Any]) -> str:
    return clean_text(work.get("id")).rstrip("/").split("/")[-1]


def doi_url(work: dict[str, Any]) -> str:
    return clean_text(work.get("doi"))


def should_keep(work: dict[str, Any], category: dict[str, Any]) -> bool:
    title = title_text(work)
    if not title:
        return False
    if not title_ok(title, category):
        return False
    if int(work.get("publication_year") or 0) < MIN_YEAR:
        return False

    venue = source_name(work)
    if not venue:
        return False

    venue_lower = venue.lower()
    cited_by = int(work.get("cited_by_count") or 0)
    publication_year = int(work.get("publication_year") or 0)
    is_review = work.get("type") == "review"
    has_quality_venue = any(pattern in venue_lower for pattern in QUALITY_SOURCE_PATTERNS)

    # Reject papers older than 2 years with fewer than 3 citations
    if publication_year <= 2023 and cited_by < 3:
        return False

    return has_quality_venue or is_review or cited_by >= category["min_cites"]


def upsert_work(
    work: dict[str, Any],
    category: dict[str, Any],
    works_by_id: dict[str, dict[str, Any]],
    category_members: dict[str, dict[str, int]],
) -> None:
    if not should_keep(work, category):
        return

    identifier = openalex_id(work)
    score = quality_score(work, category)

    if identifier not in works_by_id:
        works_by_id[identifier] = {
            "id": identifier,
            "title": title_text(work),
            "year": int(work.get("publication_year") or 0),
            "venue": source_name(work),
            "type": clean_text(work.get("type")) or "article",
            "authors": format_authors(work),
            "doi_url": doi_url(work),
            "openalex_url": clean_text(work.get("id")),
            "cited_by_count": int(work.get("cited_by_count") or 0),
            "category_ids": [],
        }

    record = works_by_id[identifier]
    if category["id"] not in record["category_ids"]:
        record["category_ids"].append(category["id"])

    previous_score = category_members[category["id"]].get(identifier, -1)
    if score > previous_score:
        category_members[category["id"]][identifier] = score


def gather_sources(refresh: bool = False) -> dict[str, Any]:
    works_by_id: dict[str, dict[str, Any]] = {}
    category_members: dict[str, dict[str, int]] = {category["id"]: {} for category in CATEGORIES}

    for category in CATEGORIES:
        for phrase in category["title_phrases"]:
            works = query_openalex(f"title.search:{phrase}", pages=category["title_pages"], refresh=refresh)
            for work in works:
                upsert_work(work, category, works_by_id, category_members)

        if len(category_members[category["id"]]) < category["target"]:
            for query in category["fallback_queries"]:
                works = query_openalex(f"title_and_abstract.search:{query}", pages=1, refresh=refresh)
                for work in works:
                    upsert_work(work, category, works_by_id, category_members)
                if len(category_members[category["id"]]) >= category["target"]:
                    break

    category_output: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    for category in CATEGORIES:
        scored = category_members[category["id"]]
        ordered_ids = sorted(
            scored,
            key=lambda identifier: (
                scored[identifier],
                works_by_id[identifier]["cited_by_count"],
                works_by_id[identifier]["year"],
                works_by_id[identifier]["title"],
            ),
            reverse=True,
        )[: category["target"]]

        selected_ids.update(ordered_ids)
        category_output.append(
            {
                "id": category["id"],
                "label": category["label"],
                "description": category["description"],
                "target": category["target"],
                "source_ids": ordered_ids,
                "selected_count": len(ordered_ids),
            }
        )

    sources = [
        works_by_id[identifier]
        for identifier in sorted(
            selected_ids,
            key=lambda item: (
                works_by_id[item]["year"],
                works_by_id[item]["cited_by_count"],
                works_by_id[item]["title"],
            ),
            reverse=True,
        )
    ]
    sources.extend(MANUAL_SOURCES)

    numeric_years = [source["year"] for source in sources if isinstance(source.get("year"), int)]
    summary = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "total_unique_sources": len(sources),
        "scholarly_source_count": len(selected_ids),
        "manual_source_count": len(MANUAL_SOURCES),
        "category_count": len(CATEGORIES),
        "year_range": {
            "min": min(numeric_years) if numeric_years else None,
            "max": max(numeric_years) if numeric_years else None,
        },
        "selection_policy": [
            "Peer-reviewed articles and reviews from title-focused OpenAlex harvesting.",
            "Priority for benchmark papers, review papers, high-impact venues, and recent 2024-2026 syntheses.",
            "Manual additions reserved for official data-platform resources and benchmark documentation.",
        ],
    }

    return {
        "summary": summary,
        "categories": category_output,
        "sources": sources,
    }


def write_outputs(payload: dict[str, Any]) -> None:
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    JS_OUT.write_text(
        "window.MATERIALS_ML_ATLAS_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build structured bibliography data for the ML x Materials Science research atlas.")
    parser.add_argument("--refresh", action="store_true", help="Ignore cached OpenAlex responses and refetch.")
    args = parser.parse_args()

    payload = gather_sources(refresh=args.refresh)
    write_outputs(payload)

    summary = payload["summary"]
    print(
        json.dumps(
            {
                "total_unique_sources": summary["total_unique_sources"],
                "scholarly_source_count": summary["scholarly_source_count"],
                "manual_source_count": summary["manual_source_count"],
                "category_count": summary["category_count"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
