/**
 * atlas-content.js
 * ----------------
 * Structural research-framework content for the ML × Materials Science Atlas.
 *
 * This file defines the eight-layer first-principles architecture, the eleven-branch
 * deep taxonomy, frontier growth bands, causal bottleneck chains, and the strategic
 * research agenda.  All entries are language-neutral data objects; localised UI copy
 * lives in atlas-i18n.js.
 *
 * Maintainers: edit this file when the research framework itself changes (new branches,
 * updated bottlenecks, revised architecture layers).  Do NOT put rendering logic here.
 */

"use strict";

/* =========================================================================
 * Section 1 — First-Principles Research Architecture (8 layers)
 * ========================================================================= */

var architectureSteps = [
  {
    index: "01",
    title: "Optimization Objective",
    summary:
      "Define the real utility function before touching the model stack. " +
      "Materials research is inherently multi-objective: high performance is " +
      "insufficient if the candidate is unstable, unsafe, impossible to " +
      "synthesize, too expensive, too carbon intensive, or too slow to qualify.",
    bullets: [
      "Intrinsic targets: thermodynamic, electronic, optical, magnetic, catalytic, transport, and mechanical properties",
      "Extrinsic targets: manufacturability, abundance, toxicity, regulation, cost, and lifecycle footprint",
      "Research-mode targets: information gain, falsifiability, and experimental efficiency",
    ],
    risk:
      "If this layer is weak, the rest of the pipeline optimizes a proxy " +
      "and produces elegant but strategically irrelevant results.",
  },
  {
    index: "02",
    title: "Material State Space",
    summary:
      "The field acts on a coupled state space, not on isolated formulas. " +
      "Composition, structure, defects, interfaces, processing history, " +
      "environment, and use conditions all co-determine outcome.",
    bullets: [
      "Chemistry: composition, stoichiometry, dopants, redox states",
      "Structure: crystal, local environment, disorder, topology, grain architecture",
      "History and boundary conditions: synthesis pathway, heat treatment, atmosphere, loading, cycling, aging",
    ],
    risk:
      "Ignoring hidden state variables is one of the main reasons materials " +
      "ML collapses under real-world distribution shift.",
  },
  {
    index: "03",
    title: "Evidence Acquisition",
    summary:
      "Evidence arrives through simulation, characterization, process " +
      "telemetry, literature, and expert priors. The field advances when " +
      "these streams become alignable, queryable, and governed rather than siloed.",
    bullets: [
      "Simulation: DFT, beyond-DFT, MD, phase-field, finite-element, reactor and process models",
      "Experiment: synthesis records, performance assays, spectroscopy, diffraction, microscopy, operando streams",
      "Knowledge systems: papers, patents, ELN/LIMS, ontologies, negative results, and provenance metadata",
    ],
    risk:
      "Without aligned evidence, even strong models only memorize whichever " +
      "modality is easiest to access.",
  },
  {
    index: "04",
    title: "Representation Regimes",
    summary:
      "Representations are not just encoding tricks. They determine which " +
      "physics, constraints, and invariances can be learned at all.",
    bullets: [
      "Descriptors and tabular featurizers for low-cost screening and small-data learning",
      "Atomic and crystal graphs for structure-aware property and force learning",
      "Microstructure fields, spectra encoders, time-series models, and multimodal latent spaces",
    ],
    risk:
      "Representation mismatch is the hidden reason many benchmarks look " +
      "strong while transfer to real tasks remains brittle.",
  },
  {
    index: "05",
    title: "Inference and Learning Regimes",
    summary:
      "Different research questions require different inference primitives: " +
      "discriminative prediction, generative design, scientific surrogates, " +
      "causal reasoning, or sequential decision-making.",
    bullets: [
      "Forward prediction, ranking, and uncertainty-aware screening",
      "Generative and inverse design under hard feasibility constraints",
      "Scientific ML, operator learning, causal inference, multimodal foundation models, and agents",
    ],
    risk:
      "Treating every problem as generic supervised learning erases the " +
      "structure that actually differentiates subfields.",
  },
  {
    index: "06",
    title: "Decision Loops",
    summary:
      "The value of ML appears when it drives a decision: which candidate " +
      "to test, which recipe to adjust, which tool state is abnormal, which " +
      "region of phase space to explore next.",
    bullets: [
      "Candidate prioritization, inverse design, and experiment planning",
      "Virtual metrology, process control, fault detection, and yield optimization",
      "Closed-loop laboratories, digital twins, and online adaptation",
    ],
    risk:
      "Model-centric projects that never close the decision loop rarely " +
      "survive translation into engineering practice.",
  },
  {
    index: "07",
    title: "Validation and Governance",
    summary:
      "One random split is not validation. The field needs calibration, OOD " +
      "tests, inter-lab transfer checks, prospective studies, provenance " +
      "guarantees, and safeguards against data or image manipulation.",
    bullets: [
      "Benchmark discipline: train/validation/test definitions aligned to deployment reality",
      "Trust: calibration, uncertainty, causal confounding checks, reproducibility, and traceability",
      "Governance: model cards, data cards, image integrity, auditability, and update control",
    ],
    risk:
      "Without this layer, the literature overstates discoverability and " +
      "underestimates downstream qualification burden.",
  },
  {
    index: "08",
    title: "Deployment Context",
    summary:
      "A discovery model, a process model, and a qualification model do not " +
      "live under the same constraints. Deployment defines latency, data " +
      "availability, risk tolerance, and acceptable failure modes.",
    bullets: [
      "Discovery deployment: hypothesis generation, closed-loop exploration, portfolio selection",
      "Production deployment: reliability, latency, maintenance, safe fallback, and human override",
      "Lifecycle deployment: sustainability, supply-chain resilience, recycling, qualification, and certification",
    ],
    risk:
      "When deployment context is ignored, the work remains academically " +
      "interesting but operationally fragile.",
  },
];

/* =========================================================================
 * Section 2 — Deep Taxonomy (11 branches)
 * ========================================================================= */

var taxonomyBranches = [
  {
    title: "1. Problem Formulation and Objective Systems",
    summary:
      "Every later branch depends on this one. The field should be classified " +
      "first by what it is trying to optimize and only second by which models it uses.",
    tree: [
      {
        label: "1.1 Core scientific intents",
        note: "Discovery, explanation, control, qualification, deployment",
        children: [
          { label: "1.1.1 Discover new candidates or operating windows" },
          { label: "1.1.2 Explain structure-property-process relationships" },
          { label: "1.1.3 Control synthesis or manufacturing in real time" },
          { label: "1.1.4 Qualify materials for reliability, safety, and scale-up" },
        ],
      },
      {
        label: "1.2 Objective-function layers",
        note: "Performance is only one term in the total utility function",
        children: [
          { label: "1.2.1 Intrinsic properties: electronic, ionic, optical, magnetic, catalytic, mechanical" },
          { label: "1.2.2 Feasibility constraints: synthesis accessibility, phase stability, defect tolerance, interface compatibility" },
          { label: "1.2.3 System constraints: cost, throughput, abundance, safety, carbon, regulation" },
          { label: "1.2.4 Epistemic targets: uncertainty reduction, information gain, benchmark value" },
        ],
      },
      {
        label: "1.3 Decision contexts",
        note: "Different contexts imply different acceptable failure modes",
        children: [
          { label: "1.3.1 Offline screening and ranking" },
          { label: "1.3.2 Closed-loop exploration and adaptive experimentation" },
          { label: "1.3.3 In-line monitoring and control" },
          { label: "1.3.4 Qualification, certification, and portfolio management" },
        ],
      },
    ],
    gaps: [
      "Proxy targets are often easier to label than real deployment targets, which distorts model development.",
      "Multi-objective tradeoffs are usually handled heuristically rather than through explicit decision theory.",
      "The field still lacks strong standards for combining technical performance with cost, sustainability, and qualification risk.",
    ],
  },
  {
    title: "2. Evidence and Data Substrate",
    summary:
      "Materials intelligence is bounded by what can be measured, simulated, " +
      "normalized, and traced. This branch is the data fabric underlying every other branch.",
    tree: [
      {
        label: "2.1 Native evidence streams",
        children: [
          { label: "2.1.1 First-principles and atomistic simulation: DFT, beyond-DFT, MD, MLMD" },
          { label: "2.1.2 Experimental characterization: XRD, XAS, Raman, SEM, TEM, EBSD, tomography" },
          { label: "2.1.3 Process telemetry: sensor traces, equipment state, wafer maps, reactor logs" },
          { label: "2.1.4 Knowledge corpora: papers, patents, handbooks, ELN/LIMS records, standards" },
        ],
      },
      {
        label: "2.2 Data organization layers",
        children: [
          { label: "2.2.1 Databases and repositories: Materials Project, NOMAD, OQMD, AFLOW, Polymer Genome" },
          { label: "2.2.2 Benchmark suites and leaderboards: Matbench, JARVIS-Leaderboard, domain-specific task sets" },
          { label: "2.2.3 Interoperability standards: FAIR metadata, OPTIMADE, schema mapping, ontology alignment" },
          { label: "2.2.4 Data quality control: provenance, versioning, integrity screening, failed-experiment capture" },
        ],
      },
      {
        label: "2.3 Missing evidence classes",
        children: [
          { label: "2.3.1 Negative and failed experiments" },
          { label: "2.3.2 Inter-lab variation and instrument shift" },
          { label: "2.3.3 Processing history, atmosphere, and latent environment variables" },
          { label: "2.3.4 Scale-up and downstream qualification labels" },
        ],
      },
    ],
    gaps: [
      "Metadata completeness, not raw model complexity, is often the limiting factor for generalization.",
      "Many public datasets systematically under-represent unstable, failed, rare, or highly process-sensitive regimes.",
      "Interoperability across simulation, experimental, textual, and production data remains fragmented.",
    ],
  },
  {
    title: "3. Representation Stack",
    summary:
      "Representation is where domain knowledge becomes machine-actionable. " +
      "This branch determines the invariances and couplings that the learner can capture.",
    tree: [
      {
        label: "3.1 Composition and descriptor spaces",
        children: [
          { label: "3.1.1 Handcrafted elemental statistics and domain descriptors" },
          { label: "3.1.2 Composition-only embeddings for low-cost early-stage screening" },
          { label: "3.1.3 Domain-specific descriptors for polymers, alloys, catalysts, and electrochemistry" },
        ],
      },
      {
        label: "3.2 Structure-aware representations",
        children: [
          { label: "3.2.1 Crystal graphs and periodic graph neural networks" },
          { label: "3.2.2 Local atomic environments, symmetry-aware features, point clouds" },
          { label: "3.2.3 Defect, interface, and disordered-state representations" },
        ],
      },
      {
        label: "3.3 Mesoscale and process representations",
        children: [
          { label: "3.3.1 Microstructure fields, textures, grains, pores, topology" },
          { label: "3.3.2 Spectral and diffraction encoders" },
          { label: "3.3.3 Time-series, control states, and multistep process trajectories" },
          { label: "3.3.4 Text embeddings, knowledge graphs, and multimodal latent spaces" },
        ],
      },
    ],
    gaps: [
      "Interfaces, defects, and nonequilibrium states are still much harder to encode than ideal bulk structures.",
      "Cross-scale alignment between atomic, microstructural, and process representations remains weak.",
      "Missing modalities are the norm in materials pipelines, but most representation research still assumes clean full-data settings.",
    ],
  },
  {
    title: "4. Forward Modeling",
    summary:
      "Forward models answer the question: given composition, structure, process, " +
      "or microstructure, what happens? This remains the densest and most benchmarked branch of the field.",
    tree: [
      {
        label: "4.1 Core forward tasks",
        children: [
          { label: "4.1.1 Composition \u2192 property prediction" },
          { label: "4.1.2 Structure \u2192 property prediction" },
          { label: "4.1.3 Process \u2192 property or yield prediction" },
          { label: "4.1.4 Microstructure \u2192 property or failure prediction" },
        ],
      },
      {
        label: "4.2 Property families",
        children: [
          { label: "4.2.1 Thermodynamic and stability targets" },
          { label: "4.2.2 Electronic, magnetic, optical, and transport targets" },
          { label: "4.2.3 Mechanical, fatigue, fracture, and reliability targets" },
          { label: "4.2.4 Catalytic, electrochemical, or kinetic performance targets" },
        ],
      },
      {
        label: "4.3 Deployment forms",
        children: [
          { label: "4.3.1 High-throughput screening and triage" },
          { label: "4.3.2 Property-surrogate insertion into optimization loops" },
          { label: "4.3.3 Virtual metrology and in-line prediction" },
        ],
      },
    ],
    gaps: [
      "Random splits still overestimate field performance relative to chemistry-, structure-, or process-shifted deployment.",
      "Label noise and proxy-target shortcuts are severe in small experimental datasets.",
      "True causal variables are frequently hidden by incomplete processing-history metadata.",
    ],
  },
  {
    title: "5. Inverse Design and Generative Search",
    summary:
      "Inverse design asks which candidate should exist to satisfy a target " +
      "profile. This branch is central to materials discovery but is only useful " +
      "when feasibility constraints are taken seriously.",
    tree: [
      {
        label: "5.1 Output spaces",
        children: [
          { label: "5.1.1 Composition and stoichiometry proposal" },
          { label: "5.1.2 Crystal, framework, molecule, or polymer-sequence generation" },
          { label: "5.1.3 Microstructure and architecture generation" },
          { label: "5.1.4 Process recipe and synthesis-condition generation" },
        ],
      },
      {
        label: "5.2 Search engines",
        children: [
          { label: "5.2.1 Variational autoencoders, flows, diffusion, autoregressive models" },
          { label: "5.2.2 Bayesian optimization and constrained sequential search" },
          { label: "5.2.3 Reinforcement and evolutionary search" },
          { label: "5.2.4 Hybrid generator + surrogate + feasibility filter stacks" },
        ],
      },
      {
        label: "5.3 Constraint layers",
        children: [
          { label: "5.3.1 Synthesizability and route accessibility" },
          { label: "5.3.2 Stability and defect tolerance" },
          { label: "5.3.3 Multi-objective tradeoffs and Pareto structure" },
          { label: "5.3.4 Diversity, novelty, and redundancy control" },
        ],
      },
    ],
    gaps: [
      "The inverse-design literature still generates many candidates that fail at synthesis, stability, or scale-up.",
      "Objective-conditioning is often easier than true constraint satisfaction.",
      "Evaluation remains inconsistent: novelty, diversity, feasibility, and prospective success are rarely scored together.",
    ],
  },
  {
    title: "6. Scientific ML and Multiscale Simulation",
    summary:
      "This branch does not primarily replace experiments; it replaces or " +
      "accelerates expensive simulation subroutines and propagates physical " +
      "structure into machine learning.",
    tree: [
      {
        label: "6.1 Atomistic acceleration",
        children: [
          { label: "6.1.1 Machine-learned interatomic potentials and force fields" },
          { label: "6.1.2 Active-learning loops for potential refinement" },
          { label: "6.1.3 Defect, surface, and interface sampling at expanded scale" },
        ],
      },
      {
        label: "6.2 Continuum and operator surrogates",
        children: [
          { label: "6.2.1 Phase-field and PDE surrogate learning" },
          { label: "6.2.2 Finite-element and mechanics surrogates" },
          { label: "6.2.3 Reactor, transport, and kinetics surrogates" },
        ],
      },
      {
        label: "6.3 Physics-structured hybrids",
        children: [
          { label: "6.3.1 Physics-informed losses and constraints" },
          { label: "6.3.2 Symmetry and conservation-aware architectures" },
          { label: "6.3.3 Cross-scale coupling between atomistic, mesoscale, and process models" },
        ],
      },
    ],
    gaps: [
      "Transferability beyond the training domain remains the decisive weakness of universal MLIPs.",
      "Interface-, defect-, and rare-event coverage is still poor relative to their real-world importance.",
      "Uncertainty propagation across multiscale chains remains underdeveloped.",
    ],
  },
  {
    title: "7. Characterization, Diagnostics, and Inference from Signals",
    summary:
      "This branch turns microscopy, diffraction, spectroscopy, and in situ " +
      "streams into actionable structural or process knowledge.",
    tree: [
      {
        label: "7.1 Imaging-driven characterization",
        children: [
          { label: "7.1.1 Segmentation, detection, tracking, and registration in SEM/TEM/STEM" },
          { label: "7.1.2 Grain, pore, defect, and phase-statistics extraction" },
          { label: "7.1.3 3D reconstruction and tomographic inference" },
        ],
      },
      {
        label: "7.2 Spectral and diffraction inference",
        children: [
          { label: "7.2.1 Phase identification and peak analysis in diffraction" },
          { label: "7.2.2 Raman, XAS, XPS, FTIR, and related spectroscopy interpretation" },
          { label: "7.2.3 Physics-guided signal decomposition and anomaly localization" },
        ],
      },
      {
        label: "7.3 Adaptive instrumentation",
        children: [
          { label: "7.3.1 Active acquisition and adaptive scanning" },
          { label: "7.3.2 In situ event detection and experiment steering" },
          { label: "7.3.3 Simulation-to-experiment alignment and synthetic-data transfer" },
        ],
      },
    ],
    gaps: [
      "Cross-instrument and cross-lab transfer remains much weaker than same-lab benchmark performance.",
      "Annotation cost is high and the ground truth is often physically ambiguous rather than simply missing.",
      "Multimodal fusion between imaging, spectroscopy, and process history is still immature.",
    ],
  },
  {
    title: "8. Synthesis, Process, and Manufacturing Intelligence",
    summary:
      "This branch targets the operational core of materials engineering: " +
      "recipe design, scale-up, monitoring, and control.",
    tree: [
      {
        label: "8.1 Synthesis and process design",
        children: [
          { label: "8.1.1 Recipe optimization and design of experiments" },
          { label: "8.1.2 Process-window discovery and control policy learning" },
          { label: "8.1.3 Process-aware inverse design" },
        ],
      },
      {
        label: "8.2 Industrial analytics",
        children: [
          { label: "8.2.1 Virtual metrology and soft sensing" },
          { label: "8.2.2 Fault detection, diagnosis, and predictive maintenance" },
          { label: "8.2.3 Yield analysis, wafer-map analytics, and dispatch support" },
        ],
      },
      {
        label: "8.3 Scale-up and production transfer",
        children: [
          { label: "8.3.1 Tool-to-tool and batch-to-batch transfer" },
          { label: "8.3.2 Digital twins and hybrid control architectures" },
          { label: "8.3.3 Qualification, traceability, and fallback design" },
        ],
      },
    ],
    gaps: [
      "Process data are deeply confounded by maintenance cycles, operator interventions, tool aging, and rare faults.",
      "Real deployments require low latency, safe fallback, and maintainability, which most academic work does not evaluate.",
      "Scaling from lab recipes to industrial processes remains one of the most under-modeled transformations in the field.",
    ],
  },
  {
    title: "9. Sequential Decision Systems and Self-Driving Labs",
    summary:
      "Once prediction is embedded in a real experiment loop, the problem " +
      "becomes a sequential decision system rather than a static supervised benchmark.",
    tree: [
      {
        label: "9.1 Candidate-selection policies",
        children: [
          { label: "9.1.1 Active learning for sparse labels and expensive experiments" },
          { label: "9.1.2 Bayesian optimization under hard constraints and multiple objectives" },
          { label: "9.1.3 Portfolio methods balancing exploration, exploitation, and information gain" },
        ],
      },
      {
        label: "9.2 Laboratory automation stack",
        children: [
          { label: "9.2.1 Robotics and instrument APIs" },
          { label: "9.2.2 Workflow orchestration, scheduling, and exception handling" },
          { label: "9.2.3 Online data assimilation and model updates" },
        ],
      },
      {
        label: "9.3 Safety and governance",
        children: [
          { label: "9.3.1 Safe action spaces and domain guardrails" },
          { label: "9.3.2 Human oversight and intervention design" },
          { label: "9.3.3 Benchmarking for closed-loop throughput, regret, and reproducibility" },
        ],
      },
    ],
    gaps: [
      "Closed-loop benchmark culture is much less mature than static benchmark culture.",
      "Scheduling, hardware reliability, and exception handling are major practical bottlenecks but weakly represented in papers.",
      "Safety constraints in chemical or materials experimentation remain under-formalized in autonomous pipelines.",
    ],
  },
  {
    title: "10. Trust, Evaluation, and Governance",
    summary:
      "This is the branch that determines whether the field can mature into " +
      "infrastructure rather than remain a sequence of isolated model demonstrations.",
    tree: [
      {
        label: "10.1 Evaluation hierarchy",
        children: [
          { label: "10.1.1 In-distribution retrospective benchmarks" },
          { label: "10.1.2 Chemistry-, structure-, process-, or lab-shift validation" },
          { label: "10.1.3 Prospective experimental validation" },
          { label: "10.1.4 Manufacturing or qualification deployment validation" },
        ],
      },
      {
        label: "10.2 Trust and reliability",
        children: [
          { label: "10.2.1 Uncertainty calibration and selective prediction" },
          { label: "10.2.2 OOD detection and covariate-shift response" },
          { label: "10.2.3 Causal reasoning and confounding diagnosis" },
        ],
      },
      {
        label: "10.3 Governance",
        children: [
          { label: "10.3.1 Reproducibility, lineage, and version control" },
          { label: "10.3.2 Data integrity, image authenticity, and traceable transformations" },
          { label: "10.3.3 Model cards, data cards, access control, and auditability" },
        ],
      },
    ],
    gaps: [
      "The field still overuses convenient benchmarks that do not approximate true prospective use.",
      "Calibration, not just point accuracy, becomes decisive once experiments become expensive or safety-critical.",
      "Generative AI increases the urgency of provenance and content-integrity safeguards for materials data.",
    ],
  },
  {
    title: "11. Material-System Verticals",
    summary:
      "These verticals cut across the workflow backbone. Each one emphasizes " +
      "different evidence types, constraints, and deployment end points.",
    tree: [
      {
        label: "11.1 Mainline verticals",
        children: [
          { label: "11.1.1 Inorganic crystals and functional materials" },
          { label: "11.1.2 Metals, steels, superalloys, and high-entropy alloys" },
          { label: "11.1.3 Polymers, soft matter, and macromolecular systems" },
          { label: "11.1.4 Batteries, solid electrolytes, and electrochemical materials" },
          { label: "11.1.5 Catalysis, surfaces, and interfaces" },
          { label: "11.1.6 Semiconductor materials and electronic processing" },
        ],
      },
      {
        label: "11.2 Adjacent high-value verticals",
        children: [
          { label: "11.2.1 Quantum, 2D, topological, and photonic materials" },
          { label: "11.2.2 Composite, architected, and metamaterial systems" },
          { label: "11.2.3 Biomaterials, implants, and tissue-facing materials" },
        ],
      },
      {
        label: "11.3 Under-served but strategically important verticals",
        children: [
          { label: "11.3.1 Glass, ceramics, refractories, and cementitious systems" },
          { label: "11.3.2 Corrosion, tribology, and surface degradation science" },
          { label: "11.3.3 Nuclear, geologic, and extreme-environment materials" },
          { label: "11.3.4 Recycling, scrap-aware design, and circular materials flows" },
        ],
      },
    ],
    gaps: [
      "Verticals differ more in evidence structure and deployment constraint than in preferred model family.",
      "The most strategically important branches are not always the most benchmarked or fashionable.",
      "Cross-vertical transfer remains difficult because process history and failure modes are domain-specific.",
    ],
  },
];

/* =========================================================================
 * Section 3 — Frontier Growth Bands
 * ========================================================================= */

var frontierBands = [
  {
    tone: "core",
    title: "Core High-Momentum Areas",
    summary:
      "These branches dominate current attention because they promise fast " +
      "benchmark gains or clear discovery narratives.",
    items: [
      "Foundation models and multimodal materials representation learning",
      "Universal or near-universal interatomic potentials and scientific ML surrogates",
      "Generative inorganic materials design and constrained inverse search",
      "Battery, catalyst, and polymer design pipelines with benchmark-friendly property targets",
      "Closed-loop discovery systems and self-driving laboratory infrastructure",
    ],
  },
  {
    tone: "adjacent",
    title: "Adjacent Growth Corridors",
    summary:
      "These branches close major logic gaps between academic benchmarks " +
      "and industrially credible materials intelligence.",
    items: [
      "Synthesis-aware inverse design and process-constrained search",
      "Literature mining, materials knowledge graphs, and LLM-assisted evidence synthesis",
      "Microscopy, diffraction, and spectroscopy agents for adaptive characterization",
      "Semiconductor and process-intelligence systems with deployment-grade constraints",
      "Additive-manufacturing digital twins and structure-process-property fusion",
    ],
  },
  {
    tone: "neglected",
    title: "Underrepresented Strategic Areas",
    summary:
      "These areas receive less hype but are essential for a complete field " +
      "architecture and for real economic impact.",
    items: [
      "Cement, glass, ceramics, refractories, and construction materials",
      "Corrosion, tribology, degradation, and reliability-under-service conditions",
      "Nuclear, extreme-environment, and geologic materials",
      "Recycling, scrap-aware design, and supply-constrained optimization",
      "Qualification, certification, and lifecycle evidence systems",
    ],
  },
];

/* =========================================================================
 * Section 4 — Causal Bottleneck Chains
 * ========================================================================= */

var bottlenecks = [
  {
    title: "Objective Mismatch",
    cause: "Available labels favor convenient proxies rather than the true deployment objective.",
    symptom: "Models benchmark well on retrospective targets but fail to improve actual candidate quality or process decisions.",
    consequence: "Research effort accumulates around the wrong loss function.",
    needed: "Explicit multi-objective formulations, deployment-grounded benchmarks, and decision-aware evaluation.",
  },
  {
    title: "Missing Variables and Hidden State",
    cause: "Processing history, atmosphere, defect states, interfacial condition, and instrument configuration are often missing.",
    symptom: "The same nominal material behaves differently across labs or process runs.",
    consequence: "OOD failure is interpreted as a model problem when it is often a measurement-design problem.",
    needed: "Richer metadata, inter-lab harmonization, and models that expose rather than conceal latent uncertainty.",
  },
  {
    title: "Cross-Scale Disconnection",
    cause: "Atomic structure, mesoscale microstructure, process history, and device-level performance live in different data spaces.",
    symptom: "Strong local predictors fail to extrapolate to end-use behavior.",
    consequence: "The field fragments into benchmarks that cannot compose into real engineering workflows.",
    needed: "Cross-scale representations, multimodal alignment, and hierarchical evaluation that respects scale transitions.",
  },
  {
    title: "Feasibility Blindness in Generative Design",
    cause: "Candidate generators optimize objective conditioning faster than they learn synthesis, stability, or route accessibility.",
    symptom: "Generated structures look novel but are chemically fragile or experimentally inaccessible.",
    consequence: "Inverse design pipelines over-promise while discovery throughput stays low.",
    needed: "Hard feasibility filters, synthesis-route modeling, and prospective validation loops.",
  },
  {
    title: "Weak Benchmark Realism",
    cause: "Random splits and clean public datasets dominate model comparison.",
    symptom: "Performance degrades when chemistry, structure class, instrument, or process window shifts.",
    consequence: "The literature systematically underestimates the difficulty of prospective use.",
    needed: "Shift-aware splits, inter-lab tests, prospective campaigns, and deployment-weighted metrics.",
  },
  {
    title: "Deployment Friction",
    cause: "Academic workflows optimize for novelty and accuracy, while operations require latency, maintainability, safety, and traceability.",
    symptom: "Promising models stall before integration with real instruments, fabs, pilot lines, or qualification processes.",
    consequence: "Value remains trapped at the demo stage.",
    needed: "Human-in-the-loop design, fallback policies, digital-thread integration, and lifecycle support.",
  },
];

/* =========================================================================
 * Section 5 — Strategic Research Agenda
 * ========================================================================= */

var agenda = [
  {
    title: "A. Universal Materials Data Fabric",
    goal: "Build interoperable, provenance-rich links across simulation, experiment, text, and manufacturing data.",
    modules: [
      "Shared identifiers, ontology alignment, and metadata versioning",
      "Negative-result capture and data-integrity screening",
      "Standardized interfaces for benchmark refresh and cross-platform querying",
    ],
    success: "A researcher can trace any model output back to raw evidence, transformation chain, and benchmark context.",
  },
  {
    title: "B. Cross-Scale Multimodal World Models",
    goal: "Learn materials state representations that connect chemistry, structure, defects, process, signals, and performance.",
    modules: [
      "Atomic-to-microstructure-to-process latent alignment",
      "Signal-grounded models for microscopy, diffraction, and spectroscopy",
      "Partial-modality and missing-data robustness by design",
    ],
    success: "Representations remain useful under real missing-modality conditions and transfer across labs or process windows.",
  },
  {
    title: "C. Synthesis-Aware Inverse Design",
    goal: "Move from property-conditioned generation to route-aware, stability-aware, and qualification-aware candidate design.",
    modules: [
      "Constraint-aware generation with synthesis and stability priors",
      "Route extraction from literature and historical lab records",
      "Feasibility filters coupled to process and characterization feedback",
    ],
    success: "Generated candidates survive real synthesis and qualification at materially higher rates.",
  },
  {
    title: "D. Decision Systems Under Uncertainty",
    goal: "Turn predictive models into reliable decision systems for screening, experimentation, and control.",
    modules: [
      "Calibration, selective prediction, and OOD-aware triage",
      "Sequential decision policies for active learning and autonomous labs",
      "Risk-aware portfolio optimization under limited experimental budget",
    ],
    success: "Experiment budgets produce measurably better knowledge gain and candidate yield than static baselines.",
  },
  {
    title: "E. Qualification-Grade Process Intelligence",
    goal: "Connect discovery-stage ML with manufacturing reality, qualification, and safe deployment.",
    modules: [
      "Virtual metrology, digital twins, and process-state observability",
      "Tool-to-tool transfer, drift handling, and safe fallback design",
      "Reliability, maintenance, and lifecycle-aware monitoring",
    ],
    success: "Models remain usable after deployment, not just during retrospective evaluation.",
  },
  {
    title: "F. Sustainability and Circularity Optimization",
    goal: "Integrate carbon, supply risk, recycling, and strategic-material constraints into the core field logic rather than treating them as afterthoughts.",
    modules: [
      "Critical-material substitution and supply-aware screening",
      "Recycling and scrap-aware property/process models",
      "Lifecycle metrics embedded into objective design and portfolio selection",
    ],
    success: "The field optimizes not only for technical performance but for deployable and resilient materials systems.",
  },
];
