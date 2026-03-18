"use strict";

var anatomySteps = [
  {
    index: "01",
    title: "Bottleneck reframing",
    title_zh: "重新定義瓶頸",
    summary:
      "Epochal papers usually redefine the real constraint. They stop optimizing the visible proxy and expose the deeper variable that actually limits progress.",
    summary_zh:
      "劃時代論文的第一步，通常是重新定義真正的瓶頸在哪裡——不再糾結於表面指標，而是找出真正卡住進展的深層變數。",
    bullets: [
      "Turn a vague challenge into a constrained engineering objective",
      "Expose the hidden variable that downstream work has been ignoring",
      "Convert narrative intuition into a manipulable problem statement"
    ],
    bullets_zh: [
      "把模糊的挑戰轉化為有明確限制條件的工程目標",
      "找出下游研究一直忽視的隱藏變數",
      "把直覺式的判斷轉化成可操作的問題陳述"
    ],
    risk:
      "Without correct bottleneck identification, later work optimizes the wrong thing and produces local novelty rather than irreversible progress.",
    risk_zh:
      "如果瓶頸判斷錯了，後續研究就會在錯的方向上做最佳化，只產出局部的新意，無法帶來不可逆的進步。"
  },
  {
    index: "02",
    title: "Observability gain",
    title_zh: "觀測能力的突破",
    summary:
      "Many technology leaps begin when a paper makes an invisible process visible, measurable, or traceable at the right resolution.",
    summary_zh:
      "許多技術飛躍的起點，是某篇論文讓原本看不見的過程變得可觀測、可量化，或者能在對的解析度下被追蹤。",
    bullets: [
      "Higher-resolution sensing, imaging, sequencing, or logging",
      "New signal channels or multi-modal evidence alignment",
      "Cleaner mapping from hidden state to observed data"
    ],
    bullets_zh: [
      "更高解析度的感測、成像、定序或紀錄",
      "開闢新的訊號通道，或對齊多種模態的觀測證據",
      "讓隱藏狀態與觀測數據之間的對應更加清晰"
    ],
    risk:
      "If the state of the system remains weakly observed, control, prediction, and explanation all inherit a hard ceiling.",
    risk_zh:
      "如果系統狀態始終觀測不清，控制、預測和解釋就全都有一道跨不過去的天花板。"
  },
  {
    index: "03",
    title: "Representation shift",
    title_zh: "表徵方式的轉換",
    summary:
      "Landmark papers often replace an awkward representation with one that aligns better with symmetry, structure, sparsity, hierarchy, or invariance.",
    summary_zh:
      "里程碑論文常做的一件事，是用更貼合對稱性、結構、稀疏性或不變性的表徵方式，取代原本彆扭的描述框架。",
    bullets: [
      "Better encodings for structure, time, geometry, or sequence",
      "Lower friction between theory and computation",
      "Improved transfer across tasks, scales, or domains"
    ],
    bullets_zh: [
      "為結構、時間、幾何或序列找到更好的編碼方式",
      "拉近理論與計算之間的距離",
      "讓方法更容易跨任務、跨尺度、跨領域遷移"
    ],
    risk:
      "A poor representation can make a fundamentally solvable problem appear computationally intractable.",
    risk_zh:
      "不好的表徵方式，足以讓一個本來可以解的問題看起來完全沒辦法算。"
  },
  {
    index: "04",
    title: "Search and control tractability",
    title_zh: "讓搜尋與控制變得可行",
    summary:
      "Breakthrough work often compresses an impossible search space into a feasible decision loop through optimization, learning, control, or heuristic design.",
    summary_zh:
      "突破性研究經常做的事，是透過最佳化、學習、控制或啟發式設計，把原本大到不可能窮舉的搜尋空間壓縮成可行的決策迴圈。",
    bullets: [
      "Reduction in experimental or computational search cost",
      "Active decision policies instead of passive batch processing",
      "New control surfaces for high-dimensional systems"
    ],
    bullets_zh: [
      "大幅降低實驗或計算上的搜尋成本",
      "用主動決策取代被動的批次處理",
      "替高維系統找到新的可控維度"
    ],
    risk:
      "If the search space remains combinatorial and unguided, promising ideas die before translation.",
    risk_zh:
      "如果搜尋空間仍然是組合爆炸又缺乏引導，再有潛力的想法也會在落地之前就夭折。"
  },
  {
    index: "05",
    title: "Platform creation",
    title_zh: "打造平台",
    summary:
      "Some papers matter because they do not solve one task. They create a reusable substrate, toolchain, architecture, or material platform that makes many tasks easier.",
    summary_zh:
      "有些論文的價值不在於解決某個特定問題，而在於打造出一套可重複使用的基底、工具鏈、架構或材料平台，讓後面的許多任務都變得更容易。",
    bullets: [
      "General-purpose devices, protocols, datasets, or programming abstractions",
      "Reusable building blocks rather than one-off demonstrations",
      "Compounding downstream returns from one initial conceptual move"
    ],
    bullets_zh: [
      "通用性的裝置、協議、資料集或程式抽象層",
      "可重複使用的基礎模組，而不只是一次性的展示",
      "一次觀念上的突破，帶來持續累積的下游回報"
    ],
    risk:
      "Without platformization, the field fragments into isolated demonstrations that do not compound.",
    risk_zh:
      "沒有平台化，整個領域就會散成一座座孤立的展示，無法產生複利效應。"
  },
  {
    index: "06",
    title: "Scaling pathway",
    title_zh: "找到規模化的路徑",
    summary:
      "A scientific effect becomes a technology only when someone shows how it scales in throughput, reliability, cost, latency, or manufacturing compatibility.",
    summary_zh:
      "一個科學效應要真正變成技術，前提是有人示範了它怎麼在吞吐量、可靠性、成本、延遲或製造相容性上放大規模。",
    bullets: [
      "Scaling laws, systems architectures, or process routes",
      "Compatibility with existing tools, supply chains, or fabs",
      "Operational performance under realistic resource constraints"
    ],
    bullets_zh: [
      "規模定律、系統架構或製程路線",
      "能跟現有工具、供應鏈或晶圓廠接軌",
      "在實際資源限制下仍有可用的效能"
    ],
    risk:
      "Many papers are scientifically valid but architecturally dead because no credible scaling route exists.",
    risk_zh:
      "很多論文科學上站得住腳，架構上卻是死路——因為根本找不到可信的放大途徑。"
  },
  {
    index: "07",
    title: "Validation regime",
    title_zh: "驗證機制與可信度",
    summary:
      "Irreversible progress depends on evaluation that matches deployment reality, not just benchmark convenience.",
    summary_zh:
      "真正不可逆的進步，靠的是貼近實際部署情境的驗證，而不只是跑基準測試拿個好分數。",
    bullets: [
      "Prospective validation, transfer tests, robustness checks",
      "Inter-lab, inter-site, or out-of-distribution reliability",
      "Traceability from raw evidence to final claim"
    ],
    bullets_zh: [
      "前瞻性驗證、遷移測試、穩健性檢驗",
      "跨實驗室、跨場域，以及分佈外情境的可靠度",
      "從原始數據到最終結論的完整可追溯性"
    ],
    risk:
      "Weak validation lets an attractive result spread before the community understands its real boundary conditions.",
    risk_zh:
      "驗證不夠扎實，漂亮的結果就會在大家搞清楚它的真正適用範圍之前擴散開來。"
  },
  {
    index: "08",
    title: "Translation chain",
    title_zh: "從理論到落地的完整鏈條",
    summary:
      "The most important papers either start or reshape a chain from theory to infrastructure to deployed systems and finally to industry impact.",
    summary_zh:
      "最重要的論文，不是開啟就是重塑了一條從理論到基礎設施、再到部署系統、最終影響產業的完整鏈條。",
    bullets: [
      "Enable an ecosystem of follow-on papers, tools, and products",
      "Reshape what counts as feasible in adjacent domains",
      "Persist even after later methods supersede the original implementation"
    ],
    bullets_zh: [
      "帶動後續的論文、工具和產品，形成完整的生態系",
      "改寫相鄰領域對「什麼是可行的」的認知",
      "即使後來的方法超越了原始做法，影響力依然持續"
    ],
    risk:
      "If no translation chain forms, the work may remain elegant but historically isolated.",
    risk_zh:
      "如果形不成轉化鏈條，研究再漂亮，在歷史上也只是一座孤島。"
  }
];

var breakthroughFamilies = [
  {
    title: "1. New observability",
    title_zh: "1. 讓隱藏的東西被看見",
    summary:
      "Papers that open a previously hidden state variable to measurement, imaging, sequencing, logging, or monitoring.",
    summary_zh:
      "把原本隱藏的狀態變數打開，讓它能被量測、成像、定序、記錄或監控。",
    tree: [
      { label: "1.1 Higher-resolution measurement", label_zh: "1.1 更高解析度的量測" },
      { label: "1.2 New sensing modality or contrast mechanism", label_zh: "1.2 新的感測模態或對比機制" },
      { label: "1.3 Real-time or in situ observation", label_zh: "1.3 即時或原位觀測" },
      { label: "1.4 Multi-modal alignment of evidence streams", label_zh: "1.4 多模態觀測證據的對齊" }
    ],
    gaps: [
      "Measurement papers are often undervalued compared with model papers even when they have stronger downstream leverage.",
      "Fields still lack consistent ways to compare observability gains against raw prediction improvements."
    ],
    gaps_zh: [
      "量測類論文就算下游影響力更大，評價上還是常常不如模型論文。",
      "到目前為止，各領域仍缺少一套一致的方法來比較「觀測能力的提升」和「預測準確度的改進」。"
    ]
  },
  {
    title: "2. New instrument or experimental platform",
    title_zh: "2. 新儀器或實驗平台",
    summary:
      "Papers that introduce hardware or workflow platforms which become reusable engines for later discovery.",
    summary_zh:
      "提出新的硬體或工作流程平台，後來成為推動一連串新發現的可重複使用引擎。",
    tree: [
      { label: "2.1 Instrument architecture", label_zh: "2.1 儀器架構" },
      { label: "2.2 Workflow automation or throughput gain", label_zh: "2.2 工作流程自動化與吞吐量提升" },
      { label: "2.3 Miniaturization or access expansion", label_zh: "2.3 微型化或取得門檻降低" },
      { label: "2.4 Precision and stability improvement", label_zh: "2.4 精度與穩定性提升" }
    ],
    gaps: [
      "Platform papers can have slow citation ramps even when their real technology impact is enormous.",
      "Tool-building work is still structurally undercounted in paper-centric evaluation cultures."
    ],
    gaps_zh: [
      "平台類論文的引用數成長往往很慢，就算它的實際技術影響力非常大。",
      "在以論文為中心的評價體系裡，做工具的人始終被低估。"
    ]
  },
  {
    title: "3. Representation and modeling shift",
    title_zh: "3. 表徵與建模方式的轉變",
    summary:
      "Papers that make the problem easier by changing the representation itself rather than only changing the optimizer.",
    summary_zh:
      "不是去調最佳化器，而是直接換掉描述問題的方式，讓問題本身變得更好解。",
    tree: [
      { label: "3.1 Structure-aware or symmetry-aware representations", label_zh: "3.1 感知結構或對稱性的表徵" },
      { label: "3.2 Sparse, factorized, or latent representations", label_zh: "3.2 稀疏、分解式或隱空間表徵" },
      { label: "3.3 Cross-modal or multi-scale representations", label_zh: "3.3 跨模態或多尺度表徵" },
      { label: "3.4 Pretrained representations for reuse", label_zh: "3.4 可複用的預訓練表徵" }
    ],
    gaps: [
      "Many fields still overfocus on model size while under-theorizing representation adequacy.",
      "Transferability is often claimed before the structural invariances are properly tested."
    ],
    gaps_zh: [
      "很多領域還是一味追求模型規模，卻很少認真探討表徵本身夠不夠好。",
      "可遷移性常常還沒經過結構不變性的嚴格測試就被宣稱了。"
    ]
  },
  {
    title: "4. Search, optimization, and control",
    title_zh: "4. 搜尋、最佳化與控制",
    summary:
      "Papers that reduce decision cost, make discovery loops adaptive, or create practical control surfaces in complex systems.",
    summary_zh:
      "降低決策成本、讓探索迴圈能自我調適，或在複雜系統中開出實際可用的控制維度。",
    tree: [
      { label: "4.1 Active search and experiment design", label_zh: "4.1 主動搜尋與實驗設計" },
      { label: "4.2 Reinforcement learning and sequential control", label_zh: "4.2 強化學習與序貫控制" },
      { label: "4.3 Surrogate-based optimization", label_zh: "4.3 代理模型最佳化" },
      { label: "4.4 Closed-loop adaptive systems", label_zh: "4.4 閉迴路自適應系統" }
    ],
    gaps: [
      "Search papers are often benchmarked on toy settings that do not capture operational constraints.",
      "Closed-loop credibility usually depends more on instrumentation and latency than on raw model novelty."
    ],
    gaps_zh: [
      "搜尋類論文經常在過於簡化的場景上做評比，反映不了實際操作的限制。",
      "閉迴路系統能不能信任，更多取決於儀器和延遲，而不是模型有多新穎。"
    ]
  },
  {
    title: "5. Shared infrastructure and protocols",
    title_zh: "5. 共享基礎設施與協議",
    summary:
      "Papers that create datasets, abstractions, protocols, compilers, architectures, or standards on which whole ecosystems later rely.",
    summary_zh:
      "建立資料集、抽象層、協議、編譯器、架構或標準——後來整個生態系都長在這些東西上面。",
    tree: [
      { label: "5.1 Benchmarks and shared corpora", label_zh: "5.1 基準測試與共享語料庫" },
      { label: "5.2 System architectures and distributed primitives", label_zh: "5.2 系統架構與分散式基本元件" },
      { label: "5.3 Interoperability and interface standards", label_zh: "5.3 互通性與介面標準" },
      { label: "5.4 Shared software or hardware platforms", label_zh: "5.4 共享的軟體或硬體平台" }
    ],
    gaps: [
      "Infrastructure papers often look less glamorous than capability demos but have larger compounding effects.",
      "Modern literature still lacks good metrics for ecosystem formation and protocol lock-in."
    ],
    gaps_zh: [
      "基礎設施論文看起來沒有能力展示那麼亮眼，但累積起來的影響力其實更大。",
      "學術界至今缺少好的指標，來衡量一個生態系是怎麼形成的、一套協議又是怎麼被鎖定的。"
    ]
  },
  {
    title: "6. New substrate, material, or device platform",
    title_zh: "6. 新基底、新材料或新元件平台",
    summary:
      "Papers that open a fresh physical substrate or programmable platform for later engineering.",
    summary_zh:
      "打開一個全新的物理基底或可程式化平台，讓後面的工程研發有新東西可以做。",
    tree: [
      { label: "6.1 Semiconductor and memory platform shifts", label_zh: "6.1 半導體與記憶體平台革新" },
      { label: "6.2 Materials, catalysts, and energy platform shifts", label_zh: "6.2 材料、催化與能源平台革新" },
      { label: "6.3 Photonic and quantum device platforms", label_zh: "6.3 光子與量子元件平台" },
      { label: "6.4 Biological programmability platforms", label_zh: "6.4 生物可程式化平台" }
    ],
    gaps: [
      "The first successful substrate paper is often followed by years of reliability and process bottlenecks that citation counts do not reveal.",
      "Fields routinely underestimate the time from first demonstration to manufacturing-grade maturity."
    ],
    gaps_zh: [
      "第一篇成功的基底論文之後，通常要再花好幾年解決可靠性和製程瓶頸——引用次數看不出這些。",
      "各領域普遍低估了從首次展示到真正能量產之間需要多少時間。"
    ]
  },
  {
    title: "7. Fabrication, synthesis, and process route",
    title_zh: "7. 製造、合成與製程路線",
    summary:
      "Papers that matter because they make a promising phenomenon repeatable, manufacturable, or economically reachable.",
    summary_zh:
      "價值在於讓一項有潛力的現象變得可重複、可量產，或者在經濟上做得到。",
    tree: [
      { label: "7.1 Synthesis route simplification", label_zh: "7.1 合成路線簡化" },
      { label: "7.2 Process window expansion", label_zh: "7.2 製程窗口拓寬" },
      { label: "7.3 Throughput and reproducibility gain", label_zh: "7.3 吞吐量與可重複性提升" },
      { label: "7.4 Compatibility with industrial process stacks", label_zh: "7.4 能接入現有工業製程" }
    ],
    gaps: [
      "Process-route papers remain underappreciated despite often determining whether a technology survives outside the lab.",
      "Scale-up evidence is still too fragmented across academia and industry."
    ],
    gaps_zh: [
      "製程路線論文始終不受重視，但它們往往決定了一項技術能不能走出實驗室。",
      "規模化的證據分散在學術界和產業界之間，拼不起來。"
    ]
  },
  {
    title: "8. Scaling architecture",
    title_zh: "8. 規模化架構",
    summary:
      "Papers that explain how to maintain or improve capability when the system becomes larger, faster, or more operationally constrained.",
    summary_zh:
      "解決的核心問題是：當系統變大、變快、限制條件變嚴格的時候，怎麼讓能力不掉下來甚至更好。",
    tree: [
      { label: "8.1 Compute and memory scaling", label_zh: "8.1 算力與記憶體的擴展" },
      { label: "8.2 Throughput, latency, and reliability scaling", label_zh: "8.2 吞吐量、延遲與可靠性的擴展" },
      { label: "8.3 Cost and energy scaling", label_zh: "8.3 成本與能耗的擴展" },
      { label: "8.4 Architecture-level decomposition for scale", label_zh: "8.4 為了規模化而做的架構拆解" }
    ],
    gaps: [
      "Many literatures celebrate proof-of-concept papers while neglecting scaling architectures that make the concept real.",
      "A system can be scientifically impressive and still be economically nonviable."
    ],
    gaps_zh: [
      "學界愛追捧概念驗證的論文，卻忽略了讓概念真正能用的規模化架構。",
      "一個系統可以在科學上很驚豔，在經濟上卻完全行不通。"
    ]
  },
  {
    title: "9. Validation, trust, and reproducibility",
    title_zh: "9. 驗證、信任與可重複性",
    summary:
      "Papers that change the field by making claims more falsifiable, transferable, or operationally reliable.",
    summary_zh:
      "讓研究主張變得更容易被檢驗、更能遷移、實際操作上更可靠，進而改變整個領域。",
    tree: [
      { label: "9.1 Robust benchmarks and challenge datasets", label_zh: "9.1 穩健的基準測試與挑戰資料集" },
      { label: "9.2 Reliability and failure analysis", label_zh: "9.2 可靠性與失效分析" },
      { label: "9.3 Reproducibility protocols and reference implementations", label_zh: "9.3 可重複性規範與參考實作" },
      { label: "9.4 Safety and governance structures", label_zh: "9.4 安全與治理架構" }
    ],
    gaps: [
      "Trust-building papers are systematically under-ranked relative to frontier capability papers.",
      "Technology ecosystems often become brittle because validation culture lags behind adoption speed."
    ],
    gaps_zh: [
      "建立信任的論文在排名上總是輸給展示前沿能力的論文。",
      "技術生態系之所以越來越脆弱，就是因為驗證文化跟不上技術被採用的速度。"
    ]
  },
  {
    title: "10. Cross-domain transfer",
    title_zh: "10. 跨領域遷移",
    summary:
      "Papers whose deepest importance is that they escape the original domain and become productive elsewhere.",
    summary_zh:
      "這些論文最深層的價值在於：它們逸出原始領域，在其他場域中持續產生成效。",
    tree: [
      { label: "10.1 Methods that transfer across scales or modalities", label_zh: "10.1 可跨尺度或跨模態遷移的方法" },
      { label: "10.2 Architectures that jump from one domain to many", label_zh: "10.2 從單一領域躍遷至多領域的架構" },
      { label: "10.3 Instruments repurposed into new sciences", label_zh: "10.3 被轉用於全新科學領域的儀器" },
      { label: "10.4 Concepts that become new scientific lingua franca", label_zh: "10.4 成為新一代科學通用語的概念" }
    ],
    gaps: [
      "Most review cultures still describe progress inside silos, which hides the real transfer paths of many landmark papers.",
      "The best thesis opportunities often sit in the neglected spaces between established fields."
    ],
    gaps_zh: [
      "多數學術評審文化仍在學科孤島內描述進展，遮蔽了許多里程碑論文的真實遷移路徑。",
      "最佳的論文選題機會往往隱身於既有領域之間被忽視的交界地帶。"
    ]
  }
];

var impactBands = [
  {
    tone: "core",
    title: "High-momentum mainstream",
    title_zh: "高動量主流方向",
    summary:
      "Papers and families currently receiving intense attention because they map cleanly onto visible capability gains.",
    summary_zh:
      "當前備受矚目的論文與家族——它們直接對應到顯而易見的能力躍升。",
    items: [
      "Foundation models, transformers, diffusion systems, and AI accelerators",
      "CRISPR-derived editing systems and programmable biology",
      "Quantum computing platforms, fault tolerance, and precision sensing",
      "Perovskites, batteries, catalysis, and energy-transition device platforms"
    ],
    items_zh: [
      "基礎模型、Transformer、擴散系統與 AI 加速器",
      "基於 CRISPR 的基因編輯系統與可程式化生物學",
      "量子計算平台、容錯機制與精密感測",
      "鈣鈦礦、電池、催化劑與能源轉型元件平台"
    ]
  },
  {
    tone: "adjacent",
    title: "Adjacent compounding corridors",
    title_zh: "相鄰疊加廊道",
    summary:
      "Historically powerful branches that often matter more than their headline visibility suggests.",
    summary_zh:
      "歷史上影響深遠的分支，其實際重要性往往遠超表面的能見度。",
    items: [
      "Metrology, imaging, sequencing, and calibration papers",
      "Distributed systems abstractions and protocol papers",
      "Manufacturing process control, digital twins, and in situ monitoring",
      "Benchmark and data infrastructure papers that reshape field norms"
    ],
    items_zh: [
      "計量學、成像、定序與校準相關論文",
      "分散式系統抽象與協議論文",
      "製造過程控制、數位孿生與原位監測",
      "重塑領域規範的基準測試與資料基礎設施論文"
    ]
  },
  {
    tone: "quiet",
    title: "Quiet but high-leverage branches",
    title_zh: "低調卻高槓桿的分支",
    summary:
      "Underfashionable moves that repeatedly determine whether a technology survives translation.",
    summary_zh:
      "看似不起眼，卻反覆決定一項技術能否存活過轉化關卡的突破。",
    items: [
      "Reliability, packaging, qualification, and failure analysis",
      "Interoperability standards and ecosystem plumbing",
      "Process-route simplification and manufacturability papers",
      "Cross-domain transfer papers that unlock hidden reuse"
    ],
    items_zh: [
      "可靠性、封裝、品質認證與失效分析",
      "互通性標準與生態系統底層管線",
      "製程路線簡化與可製造性論文",
      "釋放隱藏複用潛力的跨領域遷移論文"
    ]
  }
];

var bottlenecks = [
  {
    title: "Citation bias toward visible novelty",
    title_zh: "引用偏好可見的新穎性",
    cause:
      "Capability demos, large model releases, and flashy physical effects are easier to narrate than infrastructure or process improvements.",
    cause_zh:
      "能力展示、大型模型的發布與醒目的物理效應，敘述起來遠比基礎設施或製程改進容易。",
    symptom:
      "The literature over-ranks papers that are easy to notice and under-ranks papers that quietly reshape the technology stack.",
    symptom_zh:
      "學術文獻過度推崇易被注意的論文，卻低估了那些默默重塑技術堆疊的研究。",
    consequence:
      "Students inherit a distorted picture of what historically mattered.",
    consequence_zh:
      "學生因此繼承了一幅關於「歷史上什麼真正重要」的扭曲圖像。",
    needed:
      "Evaluation that tracks translation chains, ecosystem formation, and cross-domain reuse.",
    needed_zh:
      "能追蹤轉化鏈、生態系統形成與跨領域複用的評估方法。"
  },
  {
    title: "Field silos hide transferable breakthroughs",
    title_zh: "學科壁壘遮蔽了可遷移的突破",
    cause:
      "Research communities publish, review, and cite within narrow disciplinary loops.",
    cause_zh:
      "研究社群在狹窄的學科迴圈中發表、審查與互相引用。",
    symptom:
      "The same structural breakthrough is rediscovered under different names across distant domains.",
    symptom_zh:
      "同一結構性突破在不同領域以不同名稱被反覆重新發現。",
    consequence:
      "Important analogies and thesis opportunities remain hidden.",
    consequence_zh:
      "重要的類比關係與論文選題機會因此長期隱而未現。",
    needed:
      "An atlas organized by progress mechanism rather than by department label.",
    needed_zh:
      "一部按進步機制——而非按院系標籤——組織的圖譜。"
  },
  {
    title: "Benchmark culture obscures deployment reality",
    title_zh: "基準測試文化掩蓋了部署現實",
    cause:
      "Many papers optimize clean tasks with cheap labels instead of operational constraints.",
    cause_zh:
      "許多論文最佳化的對象是附帶廉價標籤的乾淨任務，而非真實的操作約束。",
    symptom:
      "Reported gains do not survive cost, reliability, latency, or manufacturing requirements.",
    symptom_zh:
      "論文中報告的效能提升經不起成本、可靠性、延遲或製造需求的考驗。",
    consequence:
      "Translation stalls after early enthusiasm.",
    consequence_zh:
      "初期的熱情過後，技術轉化隨即陷入停滯。",
    needed:
      "Selection logic that tracks scaling route, validation regime, and downstream system fit.",
    needed_zh:
      "能追蹤規模化路徑、驗證體制與下游系統適配性的篩選邏輯。"
  },
  {
    title: "Tool-building work is structurally undercounted",
    title_zh: "工具構建工作被結構性低估",
    cause:
      "Academic prestige systems still favor isolated conceptual claims over hard engineering platforms.",
    cause_zh:
      "學術聲望體系仍偏好孤立的概念性宣稱，而非紮實的工程平台。",
    symptom:
      "Papers that create instruments, datasets, protocols, or software substrates receive less strategic attention than they deserve.",
    symptom_zh:
      "打造儀器、資料集、協議或軟體基底的論文，所獲戰略關注度遠低於其應有的水準。",
    consequence:
      "Researchers misread where long-run leverage actually comes from.",
    consequence_zh:
      "研究者因此誤判了長期槓桿效應的真正來源。",
    needed:
      "Explicit recognition of infrastructure and platform creation as breakthrough families.",
    needed_zh:
      "明確將基礎設施與平台締造納入突破家族的認定範疇。"
  },
  {
    title: "Scale-up evidence is fragmented",
    title_zh: "規模化證據過於零散",
    cause:
      "The path from lab insight to reliable manufacturing or deployed systems spans academia, vendors, and industry with incompatible evidence standards.",
    cause_zh:
      "從實驗室洞見到可靠製造或部署系統的路徑，橫跨學術界、供應商與產業界，且各方的證據標準互不相容。",
    symptom:
      "A paper may look transformative without any clear operational route.",
    symptom_zh:
      "一篇論文可能看似具有變革性，卻缺乏任何明確的落地路線。",
    consequence:
      "The community overestimates time-to-impact and underestimates integration debt.",
    consequence_zh:
      "學術界高估了技術產生影響的速度，卻低估了系統整合所需償還的技術債。",
    needed:
      "More explicit treatment of scaling architecture, process routes, and deployment context.",
    needed_zh:
      "更明確地論述規模化架構、製程路線與部署情境。"
  },
  {
    title: "Revision history is rarely mapped",
    title_zh: "修訂歷程鮮少被梳理",
    cause:
      "Landmark papers are usually discussed as isolated origin stories rather than as nodes in a chain of correction, replacement, and platform stabilization.",
    cause_zh:
      "里程碑論文通常被當作孤立的起源故事來講述，而非修正、替代與平台穩定化鏈條中的一個節點。",
    symptom:
      "Students confuse first visibility with enduring structural importance.",
    symptom_zh:
      "學生容易將「最早被看見」與「具有持久結構性重要性」混為一談。",
    consequence:
      "Historical reasoning becomes shallow and hero-paper narratives dominate.",
    consequence_zh:
      "歷史推理流於膚淺，英雄論文式的敘事遂佔據主導地位。",
    needed:
      "Atlas layers that track successors, corrections, and persistence beyond the original implementation.",
    needed_zh:
      "能追蹤後繼者、修正脈絡以及超越原始實作之持續影響力的圖譜層。"
  }
];
