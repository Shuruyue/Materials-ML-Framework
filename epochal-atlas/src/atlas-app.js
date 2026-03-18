"use strict";

/* ── Helpers ── */

function el(tag, className, text) {
  var node = document.createElement(tag);
  if (className) node.className = className;
  if (typeof text === "string") node.textContent = text;
  return node;
}

function tField(obj, field) {
  if (I18N.lang() === "zh" && obj[field + "_zh"]) return obj[field + "_zh"];
  return obj[field];
}

function tTreeLabel(node) {
  if (I18N.lang() === "zh" && node.label_zh) return node.label_zh;
  return node.label;
}

function createList(items, className) {
  var list = el("ul", className || "panel-list");
  items.forEach(function (item) {
    list.appendChild(el("li", "", item));
  });
  return list;
}

function createStatCard(label, value, note) {
  var card = el("article", "stat-card");
  card.appendChild(el("div", "stat-label", label));
  card.appendChild(el("div", "stat-value", String(value)));
  card.appendChild(el("div", "stat-note", note));
  return card;
}

function createSourceLinks(source) {
  var links = el("div", "source-links");
  if (source.doi_url) {
    var doi = el("a", "", "DOI");
    doi.href = source.doi_url;
    doi.target = "_blank";
    doi.rel = "noreferrer";
    links.appendChild(doi);
  }
  if (source.openalex_url) {
    var oa = el("a", "", "OpenAlex");
    oa.href = source.openalex_url;
    oa.target = "_blank";
    oa.rel = "noreferrer";
    links.appendChild(oa);
  }
  return links;
}

function debounce(fn, ms) {
  var timer;
  return function () {
    var ctx = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () { fn.apply(ctx, args); }, ms);
  };
}

function byId(list) {
  return Object.fromEntries(list.map(function (item) { return [item.id, item]; }));
}

function formatNames(ids, map) {
  return (ids || [])
    .map(function (id) { return map[id] ? map[id].label : ""; })
    .filter(Boolean)
    .join(" | ");
}

/* ── Section renderers ── */

function renderAnatomy() {
  var grid = document.getElementById("anatomy-grid");
  grid.innerHTML = "";
  anatomySteps.forEach(function (step) {
    var card = el("article", "anatomy-card");
    card.appendChild(el("div", "step-index", step.index));
    card.appendChild(el("h3", "", tField(step, "title")));
    card.appendChild(el("p", "", tField(step, "summary")));
    card.appendChild(createList(tField(step, "bullets") || step.bullets));
    var risk = el("div", "risk-box");
    risk.appendChild(el("div", "risk-label", I18N.t("label.failureMode")));
    risk.appendChild(el("p", "", tField(step, "risk")));
    card.appendChild(risk);
    grid.appendChild(card);
  });
}

function renderFamilies() {
  var grid = document.getElementById("family-grid");
  grid.innerHTML = "";
  breakthroughFamilies.forEach(function (family) {
    var card = el("article", "family-card");
    card.appendChild(el("h3", "", tField(family, "title")));
    card.appendChild(el("p", "family-summary", tField(family, "summary")));
    card.appendChild(createList(
      family.tree.map(function (node) { return tTreeLabel(node); }),
      "tree-list"
    ));
    var gapBox = el("div", "gap-box");
    gapBox.appendChild(el("div", "gap-title", I18N.t("label.gapTitle")));
    gapBox.appendChild(createList(tField(family, "gaps") || family.gaps));
    card.appendChild(gapBox);
    grid.appendChild(card);
  });
}

function renderImpactBands() {
  var grid = document.getElementById("band-grid");
  grid.innerHTML = "";
  impactBands.forEach(function (band) {
    var card = el("article", "band-card " + band.tone);
    card.appendChild(el("h3", "", tField(band, "title")));
    card.appendChild(el("p", "", tField(band, "summary")));
    card.appendChild(createList(tField(band, "items") || band.items));
    grid.appendChild(card);
  });
}

function renderBottlenecks() {
  var grid = document.getElementById("issue-grid");
  grid.innerHTML = "";
  bottlenecks.forEach(function (issue) {
    var card = el("article", "issue-card");
    card.appendChild(el("h3", "", tField(issue, "title")));
    [
      [I18N.t("label.rootCause"), tField(issue, "cause")],
      [I18N.t("label.observedFailure"), tField(issue, "symptom")],
      [I18N.t("label.systemicCost"), tField(issue, "consequence")],
      [I18N.t("label.whatFix"), tField(issue, "needed")]
    ].forEach(function (pair) {
      var block = el("div", "chain-block");
      block.appendChild(el("div", "chain-label", pair[0]));
      block.appendChild(el("p", "", pair[1]));
      card.appendChild(block);
    });
    grid.appendChild(card);
  });
}

/* ── Data-driven renderers ── */

function renderHeroStats(data) {
  var summary = data.summary;
  var heroStats = document.getElementById("hero-stats");
  heroStats.innerHTML = "";
  [
    [I18N.t("label.sources"), summary.total_unique_sources],
    [I18N.t("label.families"), data.categories.length],
    [I18N.t("label.corridors"), data.corridors.length],
    [I18N.t("label.range"), summary.year_range.min + "\u2013" + summary.year_range.max]
  ].forEach(function (pair) {
    var stat = el("article", "hero-stat");
    stat.appendChild(el("div", "hero-stat-label", pair[0]));
    stat.appendChild(el("div", "hero-stat-value", String(pair[1])));
    heroStats.appendChild(stat);
  });
}

function renderHeroPanels(data) {
  var summary = data.summary;
  var container = document.getElementById("hero-panels");
  /* keep the two formula-cards, only clear stat-cards */
  var statCards = container.querySelectorAll(".stat-card");
  statCards.forEach(function (c) { c.remove(); });
  container.appendChild(createStatCard(
    I18N.t("label.scholarlySources"), summary.scholarly_source_count,
    I18N.t("label.articlesReviewsProceedings")
  ));
  container.appendChild(createStatCard(
    I18N.t("label.manualAdditions"), summary.manual_source_count,
    I18N.t("label.explicitlyCurated")
  ));
  container.appendChild(createStatCard(
    I18N.t("label.selectionPolicy"), data.categories.length,
    I18N.t("label.familiesRepresented")
  ));
}

function renderEvidenceStats(data) {
  var summary = data.summary;
  var grid = document.getElementById("evidence-stats");
  grid.innerHTML = "";
  grid.appendChild(createStatCard(I18N.t("label.totalSources"), summary.total_unique_sources, I18N.t("label.uniqueRecords")));
  grid.appendChild(createStatCard(I18N.t("label.scholarly"), summary.scholarly_source_count, I18N.t("label.openalexDerived")));
  grid.appendChild(createStatCard(I18N.t("label.manual"), summary.manual_source_count, I18N.t("label.handAdded")));
  grid.appendChild(createStatCard(I18N.t("label.corridors"), data.corridors.length, I18N.t("label.techLandingZones")));
}

function renderCategoryCards(data) {
  var grid = document.getElementById("category-grid");
  grid.innerHTML = "";
  data.categories.forEach(function (category) {
    var card = el("article", "mini-card");
    card.appendChild(el("h4", "", category.label));
    card.appendChild(el("p", "", category.description));
    card.appendChild(el("div", "mini-meta", I18N.t("label.taggedPapers", { count: category.selected_count })));
    grid.appendChild(card);
  });
}

function renderCorridorCards(data, targetId) {
  var grid = document.getElementById(targetId);
  grid.innerHTML = "";
  data.corridors.forEach(function (corridor) {
    var card = el("article", "mini-card");
    card.appendChild(el("h4", "", corridor.label));
    card.appendChild(el("p", "", corridor.description));
    card.appendChild(el("div", "mini-meta", I18N.t("label.taggedPapers", { count: corridor.selected_count })));
    grid.appendChild(card);
  });
}

function renderCanonical(canonical, data) {
  if (!canonical) return;

  var sourceMap = byId(canonical.sources || []);
  var familyMap = byId(data.categories);
  var corridorMap = byId(data.corridors);
  var statsGrid = document.getElementById("canonical-stats");
  var anchorGrid = document.getElementById("canonical-anchor-grid");
  var pathGrid = document.getElementById("canonical-path-grid");

  statsGrid.innerHTML = "";
  anchorGrid.innerHTML = "";
  pathGrid.innerHTML = "";

  [
    [I18N.t("label.manualAnchors"), canonical.summary.manual_anchor_count, I18N.t("label.handCurated")],
    [I18N.t("label.corridorPaths"), canonical.summary.corridor_count, I18N.t("label.distinctRoutes")],
    [I18N.t("label.canonicalSet"), canonical.summary.total_unique_sources, I18N.t("label.uniqueCanonical")],
    [I18N.t("label.evidenceBase"), data.summary.total_unique_sources, I18N.t("label.allHarvested")]
  ].forEach(function (item) {
    statsGrid.appendChild(createStatCard(item[0], item[1], item[2]));
  });

  (canonical.manual_anchor_ids || []).forEach(function (sourceId) {
    var source = sourceMap[sourceId];
    if (!source) return;

    var card = el("article", "source-card canonical-anchor-card");
    var top = el("div", "source-topline");
    top.appendChild(el("span", "chip", String(source.year || "")));
    top.appendChild(el("span", "chip", I18N.t("label.anchor")));
    if (source.venue) top.appendChild(el("span", "chip", source.venue));
    card.appendChild(top);
    card.appendChild(el("h3", "", source.title));

    var meta = el("ul", "source-meta");
    [
      [I18N.t("label.families"), formatNames(source.category_ids, familyMap)],
      [I18N.t("label.corridors"), formatNames(source.corridor_ids, corridorMap)],
      [I18N.t("label.whyMatters"), source.note]
    ].forEach(function (pair) {
      if (!pair[1]) return;
      var li = el("li");
      li.appendChild(el("strong", "", pair[0] + ": "));
      li.appendChild(document.createTextNode(pair[1]));
      meta.appendChild(li);
    });
    card.appendChild(meta);
    card.appendChild(createSourceLinks(source));
    anchorGrid.appendChild(card);
  });

  (canonical.corridor_lists || []).forEach(function (corridor) {
    var card = el("article", "mini-card path-card");
    card.appendChild(el("h4", "", corridor.label));
    card.appendChild(el("p", "", corridor.description));
    card.appendChild(
      el(
        "div",
        "mini-meta",
        (corridor.anchor_source_ids || []).length + " " + I18N.t("label.anchorsLabel") + " | " +
        (corridor.source_ids || []).length + " " + I18N.t("label.pathPapers")
      )
    );

    var list = el("ul", "path-list");
    (corridor.source_ids || []).forEach(function (sourceId) {
      var source = sourceMap[sourceId];
      if (!source) return;
      var item = el("li");
      var line = source.title + " (" + source.year + ")";
      if (source.type === "manual") line += " [" + I18N.t("label.anchor") + "]";
      item.textContent = line;
      list.appendChild(item);
    });
    card.appendChild(list);
    pathGrid.appendChild(card);
  });
}

/* ── Filters and source explorer ── */

function buildFilters(data) {
  var familySelect = document.getElementById("family-filter");
  var corridorSelect = document.getElementById("corridor-filter");

  familySelect.innerHTML = "";
  corridorSelect.innerHTML = "";

  [{ id: "all", label: I18N.t("filter.allFamilies") }].concat(data.categories).forEach(function (item) {
    var option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.label;
    familySelect.appendChild(option);
  });

  [{ id: "all", label: I18N.t("filter.allCorridors") }].concat(data.corridors).forEach(function (item) {
    var option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.label;
    corridorSelect.appendChild(option);
  });
}

function compareSources(sortKey) {
  if (sortKey === "citations") {
    return function (a, b) { return (b.cited_by_count || 0) - (a.cited_by_count || 0); };
  }
  if (sortKey === "year") {
    return function (a, b) { return (b.year || 0) - (a.year || 0); };
  }
  if (sortKey === "title") {
    return function (a, b) { return a.title.localeCompare(b.title); };
  }
  return function (a, b) { return (b.selection_score || 0) - (a.selection_score || 0); };
}

var _sourceUpdateFn = null;

function renderSources(data) {
  var sourcesGrid = document.getElementById("sources-grid");
  var emptyState = document.getElementById("empty-state");
  var selectionNote = document.getElementById("selection-note");
  var familyMap = byId(data.categories);
  var corridorMap = byId(data.corridors);
  var maxVisible = 120;

  /* Restore saved filter state */
  try {
    var saved = JSON.parse(localStorage.getItem("atlas-filters") || "{}");
    if (saved.family) document.getElementById("family-filter").value = saved.family;
    if (saved.corridor) document.getElementById("corridor-filter").value = saved.corridor;
    if (saved.sort) document.getElementById("sort-filter").value = saved.sort;
  } catch (e) { /* private browsing */ }

  function update() {
    var family = document.getElementById("family-filter").value;
    var corridor = document.getElementById("corridor-filter").value;
    var query = document.getElementById("source-search").value.trim().toLowerCase();
    var sortKey = document.getElementById("sort-filter").value;

    /* Persist filter state */
    try {
      localStorage.setItem("atlas-filters", JSON.stringify({ family: family, corridor: corridor, sort: sortKey }));
    } catch (e) { /* private browsing */ }

    var filtered = data.sources.filter(function (source) {
      var familyOk = family === "all" || (source.category_ids || []).indexOf(family) !== -1;
      var corridorOk = corridor === "all" || (source.corridor_ids || []).indexOf(corridor) !== -1;
      if (!familyOk || !corridorOk) return false;

      if (!query) return true;
      var haystack = [
        source.title,
        source.venue,
        source.authors,
        source.note,
        formatNames(source.category_ids, familyMap),
        formatNames(source.corridor_ids, corridorMap),
        (source.matched_topics || []).join(" | ")
      ].filter(Boolean).join(" ").toLowerCase();
      return haystack.indexOf(query) !== -1;
    }).sort(compareSources(sortKey));

    var visible = filtered.slice(0, maxVisible);
    sourcesGrid.innerHTML = "";
    emptyState.hidden = filtered.length !== 0;
    emptyState.textContent = I18N.t("evidence.empty");

    var sortLabels = { score: I18N.t("sort.score"), citations: I18N.t("sort.citations"), year: I18N.t("sort.year"), title: I18N.t("sort.title") };
    selectionNote.textContent = I18N.t("evidence.showing", {
      visible: visible.length,
      filtered: filtered.length,
      total: data.sources.length,
      sort: sortLabels[sortKey] || sortKey
    });

    visible.forEach(function (source) {
      var card = el("article", "source-card");
      var top = el("div", "source-topline");
      top.appendChild(el("span", "chip", String(source.year || "")));
      if (source.type === "manual") {
        top.appendChild(el("span", "chip", I18N.t("label.anchor")));
      } else {
        top.appendChild(el("span", "chip", source.type || ""));
      }
      top.appendChild(el("span", "chip", I18N.t("label.cites", { count: source.cited_by_count || 0 })));
      card.appendChild(top);

      card.appendChild(el("h3", "", source.title));

      var meta = el("ul", "source-meta");
      [
        [I18N.t("label.venue"), source.venue],
        [I18N.t("label.authors"), source.authors],
        [I18N.t("label.families"), formatNames(source.category_ids, familyMap)],
        [I18N.t("label.corridors"), formatNames(source.corridor_ids, corridorMap)],
        [I18N.t("label.whySelected"), source.note],
        [I18N.t("label.matchedTopics"), (source.matched_topics || []).slice(0, 5).join(" | ")]
      ].forEach(function (pair) {
        if (!pair[1]) return;
        var li = el("li");
        li.appendChild(el("strong", "", pair[0] + ": "));
        li.appendChild(document.createTextNode(pair[1]));
        meta.appendChild(li);
      });
      card.appendChild(meta);

      card.appendChild(createSourceLinks(source));
      sourcesGrid.appendChild(card);
    });

    /* Load-more button */
    var existing = document.getElementById("load-more-btn");
    if (existing) existing.remove();
    if (filtered.length > maxVisible) {
      var btn = el("button", "load-more-btn", I18N.t("evidence.loadMore"));
      btn.id = "load-more-btn";
      btn.addEventListener("click", function () {
        maxVisible += 120;
        update();
      });
      sourcesGrid.parentNode.insertBefore(btn, emptyState);
    }
  }

  _sourceUpdateFn = update;

  document.getElementById("family-filter").addEventListener("change", update);
  document.getElementById("corridor-filter").addEventListener("change", update);
  document.getElementById("sort-filter").addEventListener("change", update);
  document.getElementById("source-search").addEventListener("input", debounce(update, 200));
  update();
}

/* ── Static i18n elements ── */

function translateStaticElements() {
  var nodes = document.querySelectorAll("[data-i18n]");
  nodes.forEach(function (node) {
    var key = node.getAttribute("data-i18n");
    if (node.tagName === "INPUT") {
      node.placeholder = I18N.t(key);
    } else {
      node.textContent = I18N.t(key);
    }
  });

  /* Update sort options */
  var sortFilter = document.getElementById("sort-filter");
  if (sortFilter) {
    var opts = sortFilter.options;
    var sortKeys = ["sort.score", "sort.citations", "sort.year", "sort.title"];
    for (var i = 0; i < opts.length && i < sortKeys.length; i++) {
      opts[i].textContent = I18N.t(sortKeys[i]);
    }
  }

  /* Update language toggle active state */
  var toggle = document.getElementById("lang-toggle");
  if (toggle) {
    toggle.querySelectorAll(".lang-option").forEach(function (opt) {
      if (opt.getAttribute("data-lang") === I18N.lang()) {
        opt.setAttribute("data-active", "");
      } else {
        opt.removeAttribute("data-active");
      }
    });
  }
}

/* ── Active nav highlighting ── */

function initNavHighlight() {
  var sections = document.querySelectorAll("main .section");
  var navLinks = document.querySelectorAll(".nav-row a[href^='#']");
  if (!sections.length || !("IntersectionObserver" in window)) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        navLinks.forEach(function (link) {
          link.classList.toggle("active", link.getAttribute("href") === "#" + entry.target.id);
        });
      }
    });
  }, { rootMargin: "-20% 0px -75% 0px" });

  sections.forEach(function (s) { observer.observe(s); });
}

/* ── Back-to-top button ── */

function initBackToTop() {
  var btn = el("button", "back-to-top", "\u2191");
  btn.setAttribute("aria-label", I18N.t("nav.backToTop"));
  btn.hidden = true;
  document.body.appendChild(btn);
  window.addEventListener("scroll", function () {
    btn.hidden = window.scrollY < 600;
  });
  btn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ── Main init ── */

function init() {
  var data = window.EPOCHAL_PAPERS_ATLAS_DATA;
  var canonical = window.EPOCHAL_PAPERS_ATLAS_CANONICAL;
  if (!data) {
    throw new Error("Expected EPOCHAL_PAPERS_ATLAS_DATA to be loaded before atlas-app.js");
  }

  function renderAll() {
    translateStaticElements();
    renderHeroStats(data);
    renderHeroPanels(data);
    renderAnatomy();
    renderFamilies();
    renderImpactBands();
    renderCorridorCards(data, "corridor-grid");
    renderBottlenecks();
    renderCanonical(canonical, data);
    renderEvidenceStats(data);
    renderCategoryCards(data);
    renderCorridorCards(data, "evidence-corridor-grid");
    buildFilters(data);
    if (_sourceUpdateFn) {
      _sourceUpdateFn();
    } else {
      renderSources(data);
    }
  }

  renderAll();
  initNavHighlight();
  initBackToTop();

  /* Language toggle */
  var toggle = document.getElementById("lang-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      I18N.setLang(I18N.lang() === "en" ? "zh" : "en");
    });
  }

  /* Re-render on language change */
  document.addEventListener("langchange", renderAll);
}

init();
