"use strict";

var I18N = {
  _lang: "en",
  _dict: {
    en: {
      "site.eyebrow": "Epochal Paper Atlas",
      "site.title": "How breakthrough papers change technology",
      "site.hero": "This atlas studies landmark engineering and STEM papers by the progress mechanisms they introduced, not by discipline labels alone.",
      "card.coreThesis": "Core thesis",
      "card.coreThesisBody": "Epochal papers usually do one or more irreversible things: reveal a hidden variable, create a new control surface, make search tractable, create infrastructure that scales, or turn a scientific possibility into an engineering platform.",
      "card.thisRelease": "This release",
      "card.thisReleaseBody": "The current atlas targets 1000+ high-quality papers from roughly the last 30 years, while leaving room for older precursors when they still structure the technology landscape today.",
      "nav.anatomy": "Anatomy",
      "nav.families": "Families",
      "nav.corridors": "Corridors",
      "nav.bottlenecks": "Bottlenecks",
      "nav.canonical": "Canonical",
      "nav.evidence": "Evidence",
      "section.anatomy.kicker": "Section 1",
      "section.anatomy.title": "Breakthrough anatomy",
      "section.anatomy.desc": "A stable first-principles frame for understanding what a field-changing paper actually moves.",
      "section.families.kicker": "Section 2",
      "section.families.title": "Breakthrough families",
      "section.families.desc": "Ten recurring families of paper moves that repeatedly create large downstream technological consequences.",
      "section.corridors.kicker": "Section 3",
      "section.corridors.title": "Impact corridors",
      "section.corridors.desc": "Historical progress does not stay inside one silo. These corridors show where epochal ideas repeatedly land and compound.",
      "section.bottlenecks.kicker": "Section 4",
      "section.bottlenecks.title": "Why most papers are not epochal",
      "section.bottlenecks.desc": "The literature over-produces novelty signals and under-produces durable technological leverage. These chains explain why.",
      "section.canonical.kicker": "Section 5",
      "section.canonical.title": "Canonical reading paths",
      "section.canonical.desc": "A curated layer above the full evidence base: manual anchors plus corridor-specific representative papers that cover distinct mechanisms of technological progress.",
      "section.evidence.kicker": "Section 6",
      "section.evidence.title": "Evidence explorer",
      "section.evidence.desc": "A filterable evidence base of landmark or structurally important papers tagged by breakthrough family and technology corridor.",
      "label.failureMode": "Failure mode",
      "label.gapTitle": "Why this family is easy to miss",
      "label.rootCause": "Root cause",
      "label.observedFailure": "Observed failure",
      "label.systemicCost": "Systemic cost",
      "label.whatFix": "What the atlas must fix",
      "label.families": "Families",
      "label.corridors": "Corridors",
      "label.whySelected": "Why selected",
      "label.whyMatters": "Why it matters",
      "label.venue": "Venue",
      "label.authors": "Authors",
      "label.matchedTopics": "Matched topics",
      "label.taggedPapers": "{count} tagged papers",
      "label.cites": "{count} cites",
      "label.anchor": "anchor",
      "label.sources": "Sources",
      "label.range": "Range",
      "label.scholarlySources": "Scholarly sources",
      "label.articlesReviewsProceedings": "articles, reviews, proceedings",
      "label.manualAdditions": "Manual additions",
      "label.explicitlyCurated": "explicitly curated anchors",
      "label.selectionPolicy": "Selection policy",
      "label.familiesRepresented": "families represented in the evidence base",
      "label.totalSources": "Total sources",
      "label.uniqueRecords": "unique records after merge and dedupe",
      "label.scholarly": "Scholarly",
      "label.openalexDerived": "OpenAlex-derived scholarly works",
      "label.manual": "Manual",
      "label.handAdded": "hand-added anchors and precursor works",
      "label.techLandingZones": "technology landing zones",
      "label.manualAnchors": "Manual anchors",
      "label.handCurated": "hand-curated epochal papers",
      "label.corridorPaths": "Corridor paths",
      "label.distinctRoutes": "distinct reading routes",
      "label.canonicalSet": "Canonical set",
      "label.uniqueCanonical": "unique papers in the curated layer",
      "label.evidenceBase": "Evidence base",
      "label.allHarvested": "all harvested papers underneath",
      "label.anchorsLabel": "anchors",
      "label.pathPapers": "path papers",
      "heading.manualAnchors": "Manual anchors",
      "heading.corridorPaths": "Corridor paths",
      "heading.familiesInEvidence": "Breakthrough families in the evidence base",
      "heading.corridorsInEvidence": "Technology corridors in the evidence base",
      "filter.family": "Family",
      "filter.corridor": "Corridor",
      "filter.sort": "Sort",
      "filter.search": "Search",
      "filter.allFamilies": "All families",
      "filter.allCorridors": "All corridors",
      "sort.score": "Selection score",
      "sort.citations": "Citations",
      "sort.year": "Year",
      "sort.title": "Title",
      "search.placeholder": "Search title, venue, tags, or authors",
      "evidence.showing": "Showing {visible} of {filtered} matching sources ({total} total). Sort: {sort}.",
      "evidence.empty": "No sources match the current filters.",
      "evidence.loadMore": "Load more",
      "footer.text": "Static site. No framework. Open directly in a browser.",
      "nav.backToTop": "Back to top"
    },
    zh: {
      "site.eyebrow": "劃時代論文圖譜",
      "site.title": "突破性論文怎樣改寫了技術走向",
      "site.hero": "本圖譜不以學科分類，而是從「進步機制」切入，拆解那些真正改寫技術走向的工程與 STEM 論文。",
      "card.coreThesis": "核心觀點",
      "card.coreThesisBody": "劃時代論文通常做到了至少一件不可逆的事：發現被忽略的關鍵變數、打開新的控制維度、讓搜尋空間變得可行、建立可放大的基礎設施，或把科學原理變成工程平台。",
      "card.thisRelease": "本版收錄",
      "card.thisReleaseBody": "本版精選近三十年來逾千篇高品質論文，也收錄了至今仍在定義技術格局的早期開創之作。",
      "nav.anatomy": "剖析框架",
      "nav.families": "突破家族",
      "nav.corridors": "影響廊道",
      "nav.bottlenecks": "瓶頸分析",
      "nav.canonical": "精選導讀",
      "nav.evidence": "資料庫",
      "section.anatomy.kicker": "第一章",
      "section.anatomy.title": "突破的剖析框架",
      "section.anatomy.desc": "一套以第一性原理為基礎的分析框架，用來理解一篇改變領域的論文到底推動了什麼。",
      "section.families.kicker": "第二章",
      "section.families.title": "突破家族",
      "section.families.desc": "十種不斷重現的論文突破模式，每一種都持續為下游技術帶來深遠影響。",
      "section.corridors.kicker": "第三章",
      "section.corridors.title": "影響廊道",
      "section.corridors.desc": "技術進步從不被限制在單一領域裡。這些廊道呈現劃時代想法反覆落地、持續累積的軌跡。",
      "section.bottlenecks.kicker": "第四章",
      "section.bottlenecks.title": "為什麼多數論文稱不上劃時代",
      "section.bottlenecks.desc": "學術界大量生產「新穎」的訊號，卻很少產出能持久發揮作用的技術槓桿。以下幾條因果鏈解釋了原因。",
      "section.canonical.kicker": "第五章",
      "section.canonical.title": "經典閱讀路徑",
      "section.canonical.desc": "在完整資料庫之上另設的精選層：由手動挑選的標竿論文加上各廊道的代表性論文組成，涵蓋不同類型的技術突破機制。",
      "section.evidence.kicker": "第六章",
      "section.evidence.title": "資料探索器",
      "section.evidence.desc": "可篩選的論文資料庫，每篇都標註了對應的突破家族與技術廊道。",
      "label.failureMode": "失效模式",
      "label.gapTitle": "這個家族為什麼容易被忽略",
      "label.rootCause": "根本原因",
      "label.observedFailure": "常見失效現象",
      "label.systemicCost": "系統性代價",
      "label.whatFix": "圖譜該怎麼修正",
      "label.families": "突破家族",
      "label.corridors": "技術廊道",
      "label.whySelected": "入選原因",
      "label.whyMatters": "為何重要",
      "label.venue": "發表刊物",
      "label.authors": "作者",
      "label.matchedTopics": "相關主題",
      "label.taggedPapers": "已標記 {count} 篇",
      "label.cites": "被引用 {count} 次",
      "label.anchor": "標竿",
      "label.sources": "論文數",
      "label.range": "年份範圍",
      "label.scholarlySources": "學術來源",
      "label.articlesReviewsProceedings": "期刊論文、綜述、會議論文",
      "label.manualAdditions": "手動新增",
      "label.explicitlyCurated": "手動挑選的標竿論文",
      "label.selectionPolicy": "篩選策略",
      "label.familiesRepresented": "資料庫涵蓋的突破家族數",
      "label.totalSources": "論文總數",
      "label.uniqueRecords": "合併去重後的獨立筆數",
      "label.scholarly": "學術來源",
      "label.openalexDerived": "透過 OpenAlex 取得的學術著作",
      "label.manual": "手動新增",
      "label.handAdded": "手動加入的標竿與先驅論文",
      "label.techLandingZones": "技術落地領域",
      "label.manualAnchors": "手選標竿",
      "label.handCurated": "篇手動遴選的劃時代論文",
      "label.corridorPaths": "廊道路徑",
      "label.distinctRoutes": "條閱讀路線",
      "label.canonicalSet": "精選集",
      "label.uniqueCanonical": "精選層的獨立論文數",
      "label.evidenceBase": "資料庫",
      "label.allHarvested": "全部已收錄的論文",
      "label.anchorsLabel": "篇標竿",
      "label.pathPapers": "篇路徑論文",
      "heading.manualAnchors": "手選標竿論文",
      "heading.corridorPaths": "廊道閱讀路徑",
      "heading.familiesInEvidence": "資料庫中的突破家族",
      "heading.corridorsInEvidence": "資料庫中的技術廊道",
      "filter.family": "家族",
      "filter.corridor": "廊道",
      "filter.sort": "排序",
      "filter.search": "搜尋",
      "filter.allFamilies": "全部家族",
      "filter.allCorridors": "全部廊道",
      "sort.score": "綜合評分",
      "sort.citations": "引用次數",
      "sort.year": "年份",
      "sort.title": "標題",
      "search.placeholder": "搜尋標題、刊物、標籤或作者",
      "evidence.showing": "共 {total} 篇，篩選後 {filtered} 篇，目前顯示 {visible} 篇。排序：{sort}",
      "evidence.empty": "沒有論文符合目前的篩選條件。",
      "evidence.loadMore": "顯示更多",
      "footer.text": "純靜態網站，無框架依賴，用瀏覽器直接開啟即可。",
      "nav.backToTop": "回到頂部"
    }
  },

  t: function (key, replacements) {
    var str = (this._dict[this._lang] || this._dict.en)[key] || this._dict.en[key] || key;
    if (replacements) {
      Object.keys(replacements).forEach(function (k) {
        str = str.replace("{" + k + "}", String(replacements[k]));
      });
    }
    return str;
  },

  lang: function () {
    return this._lang;
  },

  setLang: function (lang) {
    if (!this._dict[lang]) return;
    this._lang = lang;
    document.documentElement.lang = lang;
    try {
      localStorage.setItem("atlas-lang", lang);
    } catch (e) { /* private browsing */ }
    document.dispatchEvent(new CustomEvent("langchange", { detail: { lang: lang } }));
  },

  init: function () {
    var saved;
    try {
      saved = localStorage.getItem("atlas-lang");
    } catch (e) { /* private browsing */ }
    if (saved && this._dict[saved]) {
      this._lang = saved;
    } else {
      var nav = (navigator.language || "").toLowerCase();
      this._lang = nav.startsWith("zh") ? "zh" : "en";
    }
    document.documentElement.lang = this._lang;
  }
};

I18N.init();
