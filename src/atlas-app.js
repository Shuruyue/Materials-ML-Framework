/**
 * @file atlas-app.js
 * @description Rendering engine for the ML x Materials Science Atlas.
 *
 * This module owns the application state, all DOM rendering functions, and the
 * main initialisation routine.  It reads from global data variables defined in
 * companion script files:
 *
 *   architectureSteps, taxonomyBranches, frontierBands, bottlenecks, agenda
 *   UI_COPY, CATEGORY_COPY, ZH_STRINGS
 *   window.MATERIALS_ML_ATLAS_DATA  (JSON payload)
 *
 * Every user-supplied or data-driven string that is interpolated into innerHTML
 * is passed through escapeHtml() to prevent cross-site scripting.  Where it is
 * practical the code uses DOM APIs (createElement / textContent) instead.
 */
"use strict";

/* ------------------------------------------------------------------ */
/*  Utility: HTML-escape for safe innerHTML interpolation              */
/* ------------------------------------------------------------------ */

function escapeHtml(str) {
  if (typeof str !== "string") return str;
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/* ------------------------------------------------------------------ */
/*  Application state (shared across scripts via var)                  */
/* ------------------------------------------------------------------ */

var appState = {
  lang: localStorage.getItem("materialsAtlasLanguage") || "en",
  query: "",
  activeCategory: "all"
};

/* ------------------------------------------------------------------ */
/*  Localisation helpers                                               */
/* ------------------------------------------------------------------ */

function getUi() {
  return UI_COPY[appState.lang];
}

function categoryCopy(category) {
  return CATEGORY_COPY[category.id]?.[appState.lang] || {
    label: category.label,
    description: category.description
  };
}

function tr(value) {
  if (typeof value !== "string") {
    return value;
  }
  if (appState.lang === "zh") {
    return ZH_STRINGS[value] || value;
  }
  return value;
}

/* ------------------------------------------------------------------ */
/*  Low-level DOM helpers                                              */
/* ------------------------------------------------------------------ */

function clearContainer(id) {
  document.getElementById(id).innerHTML = "";
}

/**
 * Build a <ul class="panel-list"> from an array of translatable strings.
 * Uses textContent so no escaping is required.
 */
function createList(items) {
  var list = document.createElement("ul");
  list.className = "panel-list";
  items.forEach(function (item) {
    var li = document.createElement("li");
    li.textContent = tr(item);
    list.appendChild(li);
  });
  return list;
}

/* ------------------------------------------------------------------ */
/*  Static copy (uses textContent throughout -- safe by default)       */
/* ------------------------------------------------------------------ */

function applyStaticCopy() {
  var ui = getUi();
  document.documentElement.lang = appState.lang === "zh" ? "zh-Hant" : "en";
  document.title = ui.pageTitle;

  var meta = document.querySelector('meta[name="description"]');
  if (meta) {
    meta.setAttribute("content", ui.pageDescription);
  }

  document.getElementById("nav-architecture").textContent = ui.nav.architecture;
  document.getElementById("nav-taxonomy").textContent = ui.nav.taxonomy;
  document.getElementById("nav-frontiers").textContent = ui.nav.frontiers;
  document.getElementById("nav-bottlenecks").textContent = ui.nav.bottlenecks;
  document.getElementById("nav-agenda").textContent = ui.nav.agenda;
  document.getElementById("nav-evidence").textContent = ui.nav.evidence;

  document.getElementById("hero-eyebrow").textContent = ui.heroEyebrow;
  document.getElementById("hero-title").textContent = ui.heroTitle;
  document.getElementById("hero-copy").textContent = ui.heroCopy;
  document.getElementById("utility-title").textContent = ui.utilityTitle;
  document.getElementById("utility-formula").textContent = ui.utilityFormula;

  document.getElementById("guide-title").textContent = ui.guideTitle;
  var guideList = document.getElementById("guide-list");
  guideList.innerHTML = "";
  ui.guideItems.forEach(function (item) {
    var li = document.createElement("li");
    li.textContent = item;
    guideList.appendChild(li);
  });

  document.getElementById("architecture-kicker").textContent = ui.sections.architectureKicker;
  document.getElementById("architecture-title").textContent = ui.sections.architectureTitle;
  document.getElementById("architecture-sub").textContent = ui.sections.architectureSub;
  document.getElementById("taxonomy-kicker").textContent = ui.sections.taxonomyKicker;
  document.getElementById("taxonomy-title").textContent = ui.sections.taxonomyTitle;
  document.getElementById("taxonomy-sub").textContent = ui.sections.taxonomySub;
  document.getElementById("frontiers-kicker").textContent = ui.sections.frontiersKicker;
  document.getElementById("frontiers-title").textContent = ui.sections.frontiersTitle;
  document.getElementById("frontiers-sub").textContent = ui.sections.frontiersSub;
  document.getElementById("bottlenecks-kicker").textContent = ui.sections.bottlenecksKicker;
  document.getElementById("bottlenecks-title").textContent = ui.sections.bottlenecksTitle;
  document.getElementById("bottlenecks-sub").textContent = ui.sections.bottlenecksSub;
  document.getElementById("agenda-kicker").textContent = ui.sections.agendaKicker;
  document.getElementById("agenda-title").textContent = ui.sections.agendaTitle;
  document.getElementById("agenda-sub").textContent = ui.sections.agendaSub;
  document.getElementById("evidence-kicker").textContent = ui.sections.evidenceKicker;
  document.getElementById("evidence-title").textContent = ui.sections.evidenceTitle;
  document.getElementById("evidence-sub").textContent = ui.sections.evidenceSub;

  document.getElementById("source-search").setAttribute("placeholder", ui.labels.searchPlaceholder);
  document.getElementById("empty-state").textContent = ui.labels.emptyState;
  document.getElementById("footer-copy").textContent = ui.labels.footer;

  document.querySelectorAll(".lang-button").forEach(function (button) {
    button.classList.toggle("is-active", button.dataset.lang === appState.lang);
  });
}

/* ------------------------------------------------------------------ */
/*  Section: Architecture                                              */
/* ------------------------------------------------------------------ */

function renderArchitecture() {
  var grid = document.getElementById("architecture-grid");
  architectureSteps.forEach(function (step) {
    var card = document.createElement("article");
    card.className = "architecture-card";

    var indexDiv = document.createElement("div");
    indexDiv.className = "architecture-index";
    indexDiv.textContent = step.index;

    var heading = document.createElement("h3");
    heading.textContent = tr(step.title);

    var para = document.createElement("p");
    para.textContent = tr(step.summary);

    var riskDiv = document.createElement("div");
    riskDiv.className = "architecture-risk";
    riskDiv.textContent = tr(step.risk);

    card.appendChild(indexDiv);
    card.appendChild(heading);
    card.appendChild(para);
    card.appendChild(riskDiv);
    card.appendChild(createList(step.bullets));
    grid.appendChild(card);
  });
}

/* ------------------------------------------------------------------ */
/*  Section: Taxonomy                                                  */
/* ------------------------------------------------------------------ */

function buildTree(nodes) {
  var list = document.createElement("ul");
  list.className = "tree-list";
  nodes.forEach(function (node) {
    var li = document.createElement("li");

    var label = document.createElement("div");
    label.className = "tree-label";
    // Replace ASCII arrows with the proper Unicode arrow character
    label.textContent = tr(node.label).replace(/->/g, "\u2192");

    li.appendChild(label);

    if (node.note) {
      var note = document.createElement("div");
      note.className = "tree-note";
      note.textContent = tr(node.note);
      li.appendChild(note);
    }
    if (node.children) {
      li.appendChild(buildTree(node.children));
    }
    list.appendChild(li);
  });
  return list;
}

function renderTaxonomy() {
  var grid = document.getElementById("taxonomy-grid");
  taxonomyBranches.forEach(function (branch) {
    var card = document.createElement("article");
    card.className = "taxonomy-card";
    var ui = getUi();

    var heading = document.createElement("h3");
    heading.textContent = tr(branch.title);

    var summary = document.createElement("p");
    summary.className = "taxonomy-summary";
    summary.textContent = tr(branch.summary);

    var treeWrap = document.createElement("div");
    treeWrap.className = "tree-wrap";
    treeWrap.appendChild(buildTree(branch.tree));

    var gapBox = document.createElement("div");
    gapBox.className = "gap-box";
    var gapTitle = document.createElement("div");
    gapTitle.className = "gap-title";
    gapTitle.textContent = ui.labels.openProblems;
    gapBox.appendChild(gapTitle);
    gapBox.appendChild(createList(branch.gaps));

    card.appendChild(heading);
    card.appendChild(summary);
    card.appendChild(treeWrap);
    card.appendChild(gapBox);
    grid.appendChild(card);
  });
}

/* ------------------------------------------------------------------ */
/*  Section: Frontier Bands                                            */
/* ------------------------------------------------------------------ */

function renderBands() {
  var grid = document.getElementById("band-grid");
  frontierBands.forEach(function (band) {
    var card = document.createElement("article");
    card.className = "band-card " + band.tone;

    var heading = document.createElement("h3");
    heading.textContent = tr(band.title);

    var para = document.createElement("p");
    para.textContent = tr(band.summary);

    card.appendChild(heading);
    card.appendChild(para);
    card.appendChild(createList(band.items));
    grid.appendChild(card);
  });
}

/* ------------------------------------------------------------------ */
/*  Section: Bottlenecks                                               */
/* ------------------------------------------------------------------ */

function renderBottlenecks() {
  var grid = document.getElementById("issue-grid");
  var ui = getUi();

  bottlenecks.forEach(function (issue) {
    var card = document.createElement("article");
    card.className = "issue-card";

    var heading = document.createElement("h3");
    heading.textContent = tr(issue.title);
    card.appendChild(heading);

    var chain = document.createElement("div");
    chain.className = "issue-chain";

    var pairs = [
      [ui.labels.rootCause, issue.cause],
      [ui.labels.observedFailure, issue.symptom],
      [ui.labels.systemicCost, issue.consequence],
      [ui.labels.breakthroughNeeded, issue.needed]
    ];

    pairs.forEach(function (pair) {
      var block = document.createElement("div");
      block.className = "chain-block";
      var lbl = document.createElement("div");
      lbl.className = "chain-label";
      lbl.textContent = pair[0];
      block.appendChild(lbl);
      block.appendChild(document.createTextNode(tr(pair[1])));
      chain.appendChild(block);
    });

    card.appendChild(chain);
    grid.appendChild(card);
  });
}

/* ------------------------------------------------------------------ */
/*  Section: Research Agenda                                           */
/* ------------------------------------------------------------------ */

function renderAgenda() {
  var grid = document.getElementById("agenda-grid");
  var ui = getUi();

  agenda.forEach(function (item) {
    var card = document.createElement("article");
    card.className = "agenda-card";

    var heading = document.createElement("h3");
    heading.textContent = tr(item.title);

    var goalPara = document.createElement("p");
    goalPara.className = "agenda-goal";
    goalPara.textContent = tr(item.goal);

    /* Required Modules block */
    var modulesBlock = document.createElement("div");
    modulesBlock.className = "chain-block agenda-modules";
    var modulesLabel = document.createElement("div");
    modulesLabel.className = "chain-label";
    modulesLabel.textContent = ui.labels.requiredModules;
    modulesBlock.appendChild(modulesLabel);
    modulesBlock.appendChild(createList(item.modules));

    /* Success Condition block */
    var successBlock = document.createElement("div");
    successBlock.className = "chain-block";
    var successLabel = document.createElement("div");
    successLabel.className = "chain-label";
    successLabel.textContent = ui.labels.successCondition;
    successBlock.appendChild(successLabel);
    successBlock.appendChild(document.createTextNode(tr(item.success)));

    card.appendChild(heading);
    card.appendChild(goalPara);
    card.appendChild(modulesBlock);
    card.appendChild(successBlock);
    grid.appendChild(card);
  });
}

/* ------------------------------------------------------------------ */
/*  Stat cards (reusable)                                              */
/* ------------------------------------------------------------------ */

function createStatCard(label, value, note) {
  var card = document.createElement("article");
  card.className = "stat-card";

  var labelDiv = document.createElement("div");
  labelDiv.className = "stat-label";
  labelDiv.textContent = label;

  var valueDiv = document.createElement("div");
  valueDiv.className = "stat-value";
  valueDiv.textContent = value;

  var noteDiv = document.createElement("div");
  noteDiv.className = "stat-note";
  noteDiv.textContent = note;

  card.appendChild(labelDiv);
  card.appendChild(valueDiv);
  card.appendChild(noteDiv);
  return card;
}

/* ------------------------------------------------------------------ */
/*  Hero panels & evidence stats                                       */
/* ------------------------------------------------------------------ */

function renderHeroPanels(data) {
  var panels = document.getElementById("hero-panels");
  var summary = data.summary;
  var ui = getUi();
  panels.appendChild(createStatCard(ui.stats.sources[0], summary.total_unique_sources, ui.stats.sources[1]));
  panels.appendChild(createStatCard(ui.stats.clusters[0], data.categories.length, ui.stats.clusters[1]));
  panels.appendChild(createStatCard(ui.stats.branches[0], taxonomyBranches.length, ui.stats.branches[1]));
  panels.appendChild(createStatCard(ui.stats.range[0], summary.year_range.min + "\u2013" + summary.year_range.max, ui.stats.range[1]));
}

function renderEvidenceStats(data) {
  var container = document.getElementById("evidence-stats");
  var summary = data.summary;
  var ui = getUi();
  container.appendChild(createStatCard(ui.stats.totalSources[0], summary.total_unique_sources, ui.stats.totalSources[1]));
  container.appendChild(createStatCard(ui.stats.scholarly[0], summary.scholarly_source_count, ui.stats.scholarly[1]));
  container.appendChild(createStatCard(ui.stats.official[0], summary.manual_source_count, ui.stats.official[1]));
  container.appendChild(createStatCard(ui.stats.policy[0], ui.labels.selectionPolicyValue, summary.selection_policy.map(tr).join(" ")));
}

/* ------------------------------------------------------------------ */
/*  Category cards                                                     */
/* ------------------------------------------------------------------ */

function renderCategoryCards(data) {
  var container = document.getElementById("category-grid");
  data.categories.forEach(function (category) {
    var localized = categoryCopy(category);
    var card = document.createElement("article");
    card.className = "category-card";

    var heading = document.createElement("h3");
    heading.textContent = localized.label;

    var desc = document.createElement("p");
    desc.textContent = localized.description;

    var countDiv = document.createElement("div");
    countDiv.className = "category-count";
    countDiv.textContent = category.selected_count + " " + (appState.lang === "zh" ? "\u7B46\u9AD8\u4EAE\u4F86\u6E90" : "highlighted sources");

    card.appendChild(heading);
    card.appendChild(desc);
    card.appendChild(countDiv);
    container.appendChild(card);
  });
}

/* ------------------------------------------------------------------ */
/*  Evidence explorer helpers                                          */
/* ------------------------------------------------------------------ */

function byId(list) {
  return Object.fromEntries(list.map(function (item) { return [item.id, item]; }));
}

function formatCategories(source, categoryMap) {
  return (source.category_ids || [])
    .map(function (id) {
      var category = categoryMap[id];
      return category ? categoryCopy(category).label : "";
    })
    .filter(Boolean)
    .join(" | ");
}

/**
 * Build source link anchors.  URLs originate from the curated dataset and are
 * considered safe, but label text is still escaped for defence in depth.
 */
function formatSourceLinks(source) {
  var ui = getUi();
  var links = [];
  if (source.doi_url) {
    links.push('<a href="' + escapeHtml(source.doi_url) + '" target="_blank" rel="noreferrer">' + escapeHtml(ui.labels.doi) + "</a>");
  }
  if (source.openalex_url) {
    links.push('<a href="' + escapeHtml(source.openalex_url) + '" target="_blank" rel="noreferrer">' + escapeHtml(ui.labels.openalex) + "</a>");
  }
  if (source.url) {
    links.push('<a href="' + escapeHtml(source.url) + '" target="_blank" rel="noreferrer">' + escapeHtml(ui.labels.officialPage) + "</a>");
  }
  return links.join("");
}

/* ------------------------------------------------------------------ */
/*  Source cards (innerHTML kept for the complex nested template,       */
/*  but every interpolated value is escaped)                           */
/* ------------------------------------------------------------------ */

function renderSources(data, activeCategory, query) {
  var grid = document.getElementById("sources-grid");
  var empty = document.getElementById("empty-state");
  var categoryMap = byId(data.categories);
  var ui = getUi();
  var normalizedQuery = query.trim().toLowerCase();

  var filtered = data.sources.filter(function (source) {
    var matchesCategory = activeCategory === "all" || (source.category_ids || []).includes(activeCategory);
    var haystack = [
      source.title,
      source.venue,
      source.authors,
      source.type,
      formatCategories(source, categoryMap)
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    var matchesQuery = !normalizedQuery || haystack.includes(normalizedQuery);
    return matchesCategory && matchesQuery;
  });

  grid.innerHTML = "";
  empty.hidden = filtered.length !== 0;

  filtered.forEach(function (source) {
    var card = document.createElement("article");
    card.className = "source-card";
    var categories = formatCategories(source, categoryMap);
    card.innerHTML =
      '<div class="source-topline">' +
        '<span class="source-year">' + escapeHtml(String(source.year)) + "</span>" +
        '<span class="source-type">' + escapeHtml(tr(source.type)) + "</span>" +
      "</div>" +
      "<h3>" + escapeHtml(source.title) + "</h3>" +
      '<ul class="source-meta">' +
        (source.venue ? "<li><strong>" + escapeHtml(ui.labels.venue) + ":</strong> " + escapeHtml(source.venue) + "</li>" : "") +
        (source.authors ? "<li><strong>" + escapeHtml(ui.labels.authors) + ":</strong> " + escapeHtml(source.authors) + "</li>" : "") +
        (categories ? "<li><strong>" + escapeHtml(ui.labels.clusters) + ":</strong> " + escapeHtml(categories) + "</li>" : "") +
        (source.note ? "<li><strong>" + escapeHtml(ui.labels.note) + ":</strong> " + escapeHtml(tr(source.note)) + "</li>" : "") +
      "</ul>" +
      '<div class="source-links">' + formatSourceLinks(source) + "</div>";
    grid.appendChild(card);
  });
}

/* ------------------------------------------------------------------ */
/*  Filter chip bar                                                    */
/* ------------------------------------------------------------------ */

function renderFilterChips(data, state) {
  var chipBar = document.getElementById("chip-bar");
  var ui = getUi();
  var categories = [{ id: "all", label: ui.labels.allClusters }].concat(
    data.categories.map(function (category) {
      return { id: category.id, label: categoryCopy(category).label };
    })
  );
  chipBar.innerHTML = "";
  categories.forEach(function (category) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "chip-button" + (state.activeCategory === category.id ? " is-active" : "");
    button.textContent = category.label;
    button.addEventListener("click", function () {
      state.activeCategory = category.id;
      renderFilterChips(data, state);
      renderSources(data, state.activeCategory, state.query);
    });
    chipBar.appendChild(button);
  });
}

/* ------------------------------------------------------------------ */
/*  Evidence explorer init                                             */
/* ------------------------------------------------------------------ */

function initEvidenceExplorer(data) {
  var search = document.getElementById("source-search");
  search.value = appState.query;
  if (!search.dataset.bound) {
    search.addEventListener("input", function (event) {
      appState.query = event.target.value;
      renderSources(data, appState.activeCategory, appState.query);
    });
    search.dataset.bound = "true";
  }
  renderFilterChips(data, appState);
  renderSources(data, appState.activeCategory, appState.query);
}

/* ------------------------------------------------------------------ */
/*  Full re-render                                                     */
/* ------------------------------------------------------------------ */

function rerender(data) {
  applyStaticCopy();
  ["hero-panels", "architecture-grid", "taxonomy-grid", "band-grid", "issue-grid", "agenda-grid", "evidence-stats", "category-grid"].forEach(clearContainer);
  renderHeroPanels(data);
  renderArchitecture();
  renderTaxonomy();
  renderBands();
  renderBottlenecks();
  renderAgenda();
  renderEvidenceStats(data);
  renderCategoryCards(data);
  initEvidenceExplorer(data);
}

/* ------------------------------------------------------------------ */
/*  Bootstrap                                                          */
/* ------------------------------------------------------------------ */

function initialize() {
  var data = window.MATERIALS_ML_ATLAS_DATA;
  if (!data) {
    var fallback = document.createElement("main");
    fallback.className = "page";
    var msg = document.createElement("div");
    msg.className = "empty-state";
    msg.textContent = "materials_ml_atlas_data.js is missing or failed to load.";
    fallback.appendChild(msg);
    document.body.innerHTML = "";
    document.body.appendChild(fallback);
    return;
  }

  document.querySelectorAll(".lang-button").forEach(function (button) {
    if (!button.dataset.bound) {
      button.addEventListener("click", function () {
        var nextLang = button.dataset.lang;
        if (nextLang === appState.lang) {
          return;
        }
        appState.lang = nextLang;
        localStorage.setItem("materialsAtlasLanguage", nextLang);
        rerender(data);
      });
      button.dataset.bound = "true";
    }
  });

  rerender(data);
}

initialize();
