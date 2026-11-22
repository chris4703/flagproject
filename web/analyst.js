"use strict";

const base = "/api/analyst";
const find = selector => document.querySelector(selector);
const form = find("#filters");
const dashboard = find("#dashboard");
const login = find("#login");
const loginForm = find("#login-form");
const signOut = find("#sign-out");
const reportDialog = find("#report-dialog");
const reportContent = find("#report-content");
const timezone = "America/Phoenix";
const dateFormat = new Intl.DateTimeFormat("en-US", {
  month: "short", day: "numeric", year: "numeric", timeZone: timezone,
});
const recordColumns = {
  title: "Submission", department: "Department", solution: "Solution", benefit: "Benefit",
  impact: "Impact if wrong", effort: "Effort", status: "Governance", review: "IT review",
};
let page = 1;
let recordSort = "";
let requestVersion = 0;
let detailVersion = 0;

function element(tag, text, className) {
  const result = document.createElement(tag);
  if (text !== undefined && text !== null) result.textContent = text;
  if (className) result.className = className;
  return result;
}

function control(text, style, action) {
  const button = element("button", text, style);
  button.type = "button";
  button.addEventListener("click", action);
  return button;
}

function link(text, style, href) {
  const anchor = element("a", text, style);
  anchor.href = href;
  return anchor;
}

function message(selector, error) {
  const target = find(selector);
  target.textContent = error ? error.message : "";
  target.hidden = !error;
}

async function request(path, data) {
  const response = await fetch(base + path, data === undefined ? undefined : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data),
  });
  const result = await response.json();
  if (!response.ok) {
    const error = new Error(result.error || "The analyst workspace could not load.");
    error.status = response.status;
    throw error;
  }
  return result;
}

function showLogin(focus) {
  if (reportDialog.open) reportDialog.close();
  reportContent.replaceChildren();
  find("#summary").replaceChildren();
  find("#records").replaceChildren();
  dashboard.hidden = true;
  signOut.hidden = true;
  login.hidden = false;
  loginForm.reset();
  find("#find-assessment").reset();
  if (focus) find("#username").focus();
}

function addFilter(title, key, empty, options) {
  const group = element("div");
  const label = element("label", title, "field-label");
  const select = element("select");
  select.name = key;
  select.id = `filter-${key}`;
  label.htmlFor = select.id;
  select.append(new Option(empty, ""));
  for (const [value, name] of Object.entries(options)) select.append(new Option(name, value));
  group.append(label, select);
  form.append(group);
}

function installFilters(data) {
  form.replaceChildren();
  addFilter("Completed", "days", "All time", { 7: "Last 7 days", 30: "Last 30 days", 90: "Last 90 days" });
  addFilter("Department", "department", "All departments", data.labels.department);
  addFilter("Interview source", "source", "All interviews", data.labels.source);
  addFilter("Solution", "solution", "All classifications", data.labels.solution);
  addFilter("Expected benefit", "benefit", "All benefit levels", data.labels.benefit);
  addFilter("Impact if wrong", "impact", "All impact levels", data.labels.impact);
  addFilter("Delivery effort", "effort", "All effort levels", data.labels.effort);
  addFilter("Governance", "status", "All statuses", data.labels.governance);
  addFilter("IT review", "review", "All review statuses", data.labels.review);
  addFilter("Risk rating", "risk", "All risk ratings", data.labels.risk);
  addFilter("IT involvement", "tier", "All tiers", data.labels.tier);
}

function filterQuery(withPage) {
  const params = new URLSearchParams();
  for (const [name, value] of new FormData(form)) if (value) params.set(name, value);
  if (withPage) {
    if (page !== 1) params.set("page", page);
    if (recordSort) params.set("sort", recordSort);
  }
  return params.size ? "?" + params.toString() : "";
}

function card(title, description) {
  const wrapper = element("section", null, "card analyst-card");
  wrapper.append(element("h2", title));
  if (description) wrapper.append(element("p", description, "muted"));
  return wrapper;
}

function showActiveFilters() {
  const container = find("#active-filters");
  container.replaceChildren();
  for (const select of form.elements) {
    if (!select.value) continue;
    const label = `${select.labels[0].textContent}: ${select.selectedOptions[0].text}`;
    const remove = control(label, "filter-chip", async () => {
      select.value = "";
      page = 1;
      if (await load()) select.focus({ preventScroll: true });
    });
    remove.setAttribute("aria-label", `Clear ${label} filter`);
    const cross = element("span", "×");
    cross.setAttribute("aria-hidden", "true");
    remove.append(cross);
    container.append(remove);
  }
  container.hidden = !container.children.length;
}

function chartPoint(id, className, filters, detail, label, count, total) {
  const entries = Object.entries(filters);
  const selected = entries.every(([key, value]) => form.elements[key].value === value);
  const point = control(null, className, async () => {
    for (const [key, value] of entries) form.elements[key].value = selected ? "" : value;
    page = 1;
    if (await load()) document.getElementById(id)?.focus({ preventScroll: true });
  });
  const share = total ? Math.round(100 * count / total) : 0;
  const description = `${label} · ${count} ${count === 1 ? "submission" : "submissions"} · ${share}% of matching results`;
  const reveal = () => { detail.textContent = description; };
  const clear = () => {
    if (document.activeElement !== point && !point.matches(":hover")) detail.textContent = "";
  };
  point.id = id;
  point.setAttribute("aria-label", description);
  point.setAttribute("aria-pressed", String(selected));
  point.addEventListener("pointerenter", reveal);
  point.addEventListener("pointerleave", clear);
  point.addEventListener("focus", reveal);
  point.addEventListener("blur", clear);
  return point;
}

function distribution(data, title, field) {
  const group = element("div", null, "meter-group");
  group.dataset.chart = field;
  group.append(element("h3", title));
  const detail = element("p", null, "chart-detail");
  detail.setAttribute("aria-hidden", "true");
  for (const [value, label] of Object.entries(data.labels[field])) {
    const number = data.counts[field][value] || 0;
    const selected = form.elements[field].value === value;
    const line = number || selected
      ? chartPoint(`bar-${field}-${encodeURIComponent(value)}`, "meter-line chart-bar", { [field]: value },
        detail, label, number, data.total)
      : element("div", null, "meter-line chart-zero");
    line.dataset.value = value;
    const meter = element("meter");
    meter.max = Math.max(data.total, 1);
    meter.value = number;
    meter.setAttribute("aria-hidden", "true");
    line.append(element("span", label), meter, element("strong", number));
    group.append(line);
  }
  group.append(detail);
  return group;
}

function metrics(data) {
  const section = element("section", null, "metric-grid");
  section.setAttribute("aria-label", "Submission totals");
  const values = [
    ["Completed submissions", data.total, `${data.counts.source.custom} custom · ${data.counts.source.scenario} practice`],
    ["Governance holds", data.holds, "Review required before proceeding"],
    ["High expected benefit", data.counts.benefit.high, "Staff estimate of improvement"],
    ["High impact if wrong", data.counts.impact.serious, "Reported consequence if the result is wrong"],
  ];
  for (const [label, value, description] of values) {
    const tile = element("div", null, "card metric");
    tile.append(element("h2", label), element("strong", value), element("p", description));
    section.append(tile);
  }
  return section;
}

function matrix(data, title, description, rowLabel, rows, columns, counts) {
  const section = card(title, description);
  section.dataset.chart = rows;
  const scroll = element("div", null, "table-scroll");
  const table = element("table", null, "matrix");
  const detail = element("p", null, "chart-detail");
  detail.setAttribute("aria-hidden", "true");
  const header = table.createTHead().insertRow();
  for (const label of [rowLabel, ...Object.values(data.labels[columns])]) {
    const cell = element("th", label);
    cell.scope = "col";
    header.append(cell);
  }
  const maximumCount = Math.max(1, ...Object.values(counts).flatMap(Object.values));
  const body = table.createTBody();
  for (const [key, rowTitle] of Object.entries(data.labels[rows])) {
    const row = body.insertRow();
    const label = element("th", rowTitle);
    label.scope = "row";
    row.append(label);
    for (const [column, columnLabel] of Object.entries(data.labels[columns])) {
      const count = counts[key][column];
      const cell = row.insertCell();
      const selected = form.elements[rows].value === key && form.elements[columns].value === column;
      if (!count && !selected) {
        cell.textContent = "0";
        cell.className = "empty-cell";
        continue;
      }
      const category = rows === "benefit" ? `${rowTitle} benefit` : rowTitle;
      const label = `${category} × ${columnLabel} ${columns}`;
      const button = chartPoint(`cell-${rows}-${key}-${column}`, "matrix-button",
        { [rows]: key, [columns]: column }, detail, label, count, data.total);
      button.textContent = count;
      button.style.setProperty("--strength", `${8 + Math.round(27 * count / maximumCount)}%`);
      cell.append(button);
    }
  }
  scroll.append(table);
  section.append(scroll, detail);
  return section;
}

function summaries(data) {
  const panels = element("div", null, "analytics-grid");
  const pace = data.avg_questions === null ? "" : `Average interview length · ${data.avg_questions} questions`;
  const solutions = card("Solution classifications", pace);
  solutions.append(distribution(data, "Completed assessments", "solution"));
  const impact = card("Impact and delivery effort", "Impact is reported by staff. Effort is a preliminary scope estimate.");
  impact.append(distribution(data, "Impact if the result is wrong", "impact"),
    distribution(data, "Indicative effort", "effort"));
  const governance = card("Risk and governance", "A submission can have more than one reason for a hold.");
  governance.append(distribution(data, "Risk rating", "risk"));
  const reasons = element("div", null, "hold-reasons");
  reasons.append(element("h3", "Reasons for a hold"));
  if (!data.hold_reasons.length) reasons.append(element("p", "No holds in this view.", "muted"));
  for (const [title, count] of data.hold_reasons) {
    const row = element("div");
    row.append(element("span", title), element("strong", count));
    reasons.append(row);
  }
  governance.append(reasons);
  const routing = card("Department and IT involvement");
  routing.append(distribution(data, "Department", "department"), distribution(data, "IT involvement", "tier"));
  panels.append(solutions, impact, governance, routing);
  const matrices = element("div", null, "portfolio-grid");
  matrices.append(
    matrix(data, "Expected benefit by delivery effort", "Effort is a preliminary scope estimate.", "Benefit",
      "benefit", "effort", data.benefit_effort),
    matrix(data, "Solution by impact if wrong", "This is a measure of consequence. Select a count to see matching submissions.", "Solution",
      "solution", "impact", data.cross_tab));
  const guide = element("p", "Select a bar or cell to filter. Select it again to clear that filter.", "chart-guide");
  find("#summary").replaceChildren(metrics(data), guide, matrices, panels);
}

function governanceBadge(status, review, label, detail = false) {
  if (status === "hold" && review === "awaiting") {
    return element("span", detail ? "On hold pending IT review" : "On hold", "pill hold");
  }
  const style = status === "hold" ? "review" : status === "closed" ? "inactive" : "clear";
  return element("span", label, `pill ${style}`);
}

function renderRecords(data) {
  const sort = data.sort.replace(/^-/, "");
  const direction = data.sort.startsWith("-") ? "descending" : "ascending";
  const orderLabel = sort ? `${recordColumns[sort]} ${direction}` : "Most recent first";
  const section = card("Completed submissions", `${orderLabel} · Arizona time`);
  section.firstElementChild.id = "records-title";
  section.firstElementChild.tabIndex = -1;
  if (!data.records.length) {
    section.append(element("p", "No completed assessments match these filters.", "empty-state"));
    find("#records").replaceChildren(section);
    return;
  }
  const scroll = element("div", null, "table-scroll");
  const table = element("table", null, "records-table");
  const header = table.createTHead().insertRow();
  for (const [key, label] of Object.entries(recordColumns)) {
    const cell = element("th");
    const active = key === sort;
    cell.scope = "col";
    if (active) cell.setAttribute("aria-sort", direction);
    const button = control(label, "sort-header", async () => {
      recordSort = recordSort === key ? `-${key}` : key;
      page = 1;
      if (await load()) find(`#records [data-sort="${key}"]`)?.focus({ preventScroll: true });
    });
    button.dataset.sort = key;
    const arrow = element("span", active ? (direction === "ascending" ? "↑" : "↓") : "↕", "sort-arrow");
    arrow.setAttribute("aria-hidden", "true");
    button.append(arrow);
    cell.append(button);
    header.append(cell);
  }
  const body = table.createTBody();
  for (const item of data.records) {
    const row = body.insertRow();
    const label = row.insertCell();
    label.append(control(item.title, "record-link", () => openReport(item.id)),
      element("small", `${item.id} · ${dateFormat.format(new Date(item.date))} · ${data.labels.source[item.source]}`, "record-meta"));
    row.insertCell().textContent = item.department;
    row.insertCell().textContent = data.labels.solution[item.solution];
    row.insertCell().textContent = data.labels.benefit[item.benefit];
    row.insertCell().textContent = data.labels.impact[item.impact];
    row.insertCell().textContent = data.labels.effort[item.effort];
    row.insertCell().append(governanceBadge(item.status, item.review, data.labels.governance[item.status]));
    row.insertCell().textContent = data.labels.review[item.review];
  }
  scroll.append(table);
  section.append(scroll);
  if (data.pages > 1) {
    const paging = element("nav", null, "paging");
    paging.setAttribute("aria-label", "Submission pages");
    const move = by => async () => {
      page += by;
      if (await load()) find("#records-title").focus();
    };
    const previous = control("Previous", "secondary", move(-1));
    const next = control("Next", "secondary", move(1));
    previous.disabled = data.page <= 1;
    next.disabled = data.page >= data.pages;
    paging.append(previous, element("span", `Page ${data.page} of ${data.pages}`), next);
    section.append(paging);
  }
  const scrollPosition = find("#records .table-scroll")?.scrollLeft || 0;
  find("#records").replaceChildren(section);
  scroll.scrollLeft = scrollPosition;
}

function reviewGovernance(report) {
  const review = report.review;
  const active = review.governance === "hold" && report.first_action;
  const notice = element("div", null, active ? "analyst-governance-action" : "assessment-governance");
  notice.append(governanceBadge(review.governance, review.status, review.governance_label, true));
  if (active) {
    notice.append(element("h3", `First action · ${report.first_action.owner}`),
      element("p", report.first_action.action));
  }
  return notice;
}

function reviewPanel(report, governance) {
  const panel = element("section", null, "analyst-review");
  panel.append(element("h3", "IT review"));
  const review = report.review;
  const state = element("p", report.review_options[review.status], "analyst-review-state");
  state.tabIndex = -1;
  const contact = report.contact
    ? `${report.contact.name} · ${report.contact.email}`
    : "No follow-up contact was saved for this assessment.";
  panel.append(state, element("p", contact, "analyst-contact"));
  if (review.note) panel.append(element("p", review.note, "saved-review-note"));

  const editor = element("form", null, "review-editor");
  const field = element("label", "Change review status", "field-label");
  const select = element("select");
  select.id = "review-status";
  field.htmlFor = select.id;
  for (const [code, label] of Object.entries(report.review_options)) select.append(new Option(label, code));
  select.value = review.status;

  const details = element("div", null, "review-update-details");
  const clearance = element("label", null, "review-clearance");
  const confirmed = element("input");
  confirmed.type = "checkbox";
  clearance.append(confirmed, element("span", "Required reviewers have confirmed governance clearance."));
  const noteLabel = element("label", "Review note (optional)", "field-label");
  const note = element("textarea");
  note.id = "review-note";
  note.rows = 2;
  note.maxLength = 500;
  noteLabel.htmlFor = note.id;
  details.append(clearance, noteLabel, note);

  const save = element("button", "Save status", "secondary");
  save.type = "submit";
  const actions = element("div", null, "analyst-review-actions");
  actions.append(save);
  const error = element("p", null, "error");
  error.setAttribute("role", "alert");
  error.hidden = true;
  const mark = review.status === "awaiting"
    ? control("Mark reviewed", "secondary", () => submitStatus("reviewed"))
    : null;
  if (mark) actions.append(mark);
  if (report.contact) {
    const recipient = encodeURIComponent(report.contact.email).replace("%40", "@");
    const subject = encodeURIComponent(`IT follow-up on assessment ${report.id}`);
    actions.append(link("Draft follow-up email", "secondary", `mailto:${recipient}?subject=${subject}`));
  }
  function updateFields() {
    const changed = select.value !== review.status;
    const requiresClearance = changed && report.decision.hold && select.value === "approved";
    clearance.hidden = !requiresClearance;
    confirmed.required = requiresClearance;
    noteLabel.textContent = requiresClearance ? "Clearance reference or note" : "Review note (optional)";
    note.required = requiresClearance;
    details.hidden = !changed;
    save.disabled = !changed;
  }
  async function submitStatus(status, text = "", clearanceConfirmed = false) {
    error.hidden = true;
    select.disabled = note.disabled = confirmed.disabled = save.disabled = true;
    if (mark) mark.disabled = true;
    try {
      const updated = await request(`/reports/${report.id}/review`, {
        status, revision: review.revision, note: text, clearance_confirmed: clearanceConfirmed,
      });
      if (panel.isConnected) {
        const nextReport = { ...report, review: updated };
        const nextGovernance = reviewGovernance(nextReport);
        governance.replaceWith(nextGovernance);
        const next = reviewPanel(nextReport, nextGovernance);
        panel.replaceWith(next);
        next.querySelector(".analyst-review-state").focus({ preventScroll: true });
      }
      await load();
    } catch (failure) {
      error.textContent = failure.message;
      error.hidden = false;
      select.disabled = note.disabled = confirmed.disabled = false;
      if (mark) mark.disabled = false;
      updateFields();
    }
  }
  select.addEventListener("change", () => {
    confirmed.checked = false;
    note.value = "";
    updateFields();
  });
  editor.addEventListener("submit", event => {
    event.preventDefault();
    if (select.value !== review.status) submitStatus(select.value, note.value, confirmed.checked);
  });
  updateFields();
  editor.append(field, select, details, actions, error);
  panel.append(editor);
  return panel;
}

function requestSummaryPanel(report, call) {
  const panel = element("section", null, "request-summary");
  const title = element("h3", "Request at a glance");
  const description = element("p");
  const source = element("p", null, "summary-source");
  panel.setAttribute("aria-label", title.textContent);
  description.setAttribute("aria-live", "polite");
  panel.append(title, description, source);

  function show(summary) {
    description.textContent = [summary.text, summary.context].filter(Boolean).join(" ");
    source.textContent = summary.source === "local_ai" ? "Local AI summary from intake answers" : "From intake answers";
  }

  show(report.request_summary);
  if (report.request_summary.source !== "local_ai") {
    request(`/reports/${report.id}/summary`, {}).then(summary => {
      if (reportDialog.open && call === detailVersion) show(summary);
    }).catch(() => {
      // The submitted excerpt remains available if summarization cannot finish.
    });
  }
  return panel;
}

async function openReport(id) {
  const call = ++detailVersion;
  reportContent.replaceChildren(element("p", "Opening assessment…"));
  reportDialog.showModal();
  try {
    const report = await request(`/reports/${id}`);
    if (!reportDialog.open || call !== detailVersion) return;
    const decision = report.decision;
    const governance = reviewGovernance(report);
    const actions = element("ol", null, "clean-list");
    for (const item of report.next_actions) actions.append(element("li", `${item.owner} — ${item.action}`));
    const facts = element("dl", null, "definition-list");
    for (const [label, value] of Object.entries(report.workflow)) {
      if (value) {
        const group = element("div");
        group.append(element("dt", label), element("dd", value));
        facts.append(group);
      }
    }
    const checks = element("details", null, "analyst-hold-checks");
    if (decision.hold) {
      checks.append(element("summary", "Governance checks from the assessment"));
      const reasons = element("ul", null, "clean-list");
      const evidence = new Map(report.evidence.map((answer, index) => [
        answer.id, [`Q${index + 1} ${answer.question}`, answer.answer].filter(Boolean).join(" · "),
      ]));
      for (const item of report.checks.filter(check => check.level === "hold")) {
        const reason = element("li", `${item.name}. ${item.reason} Reviewer: ${item.reviewer}.`);
        const references = item.fields.map(field => evidence.get(field)).filter(Boolean);
        if (references.length) reason.append(element("small", references.join(" / "), "check-evidence"));
        reasons.append(reason);
      }
      checks.append(reasons);
    }
    reportContent.replaceChildren(
      element("p", `${report.department} · Assessment ID ${report.id}`, "muted"),
      requestSummaryPanel(report, call),
      governance,
      reviewPanel(report, governance),
      element("h3", `${decision.label} · ${decision.risk} risk · Tier ${decision.tier}`),
      element("p", decision.rationale),
      ...(decision.hold ? [checks] : []),
      element("h3", "Next steps"), actions, facts,
      link("Download full assessment", "secondary", `${base}/reports/${report.id}/download`));
  } catch (error) {
    if (call === detailVersion) reportContent.replaceChildren(element("p", error.message, "error"));
  }
}

async function load() {
  const call = ++requestVersion;
  message("#page-error");
  try {
    const data = await request(`/overview${filterQuery(true)}`);
    if (call !== requestVersion) return false;
    if (!form.elements.length) installFilters(data);
    showActiveFilters();
    summaries(data);
    renderRecords(data);
    find("#export").href = `${base}/export.csv${filterQuery(false)}`;
    find("#results-status").textContent = `${data.total} matching completed submissions.`;
    login.hidden = true;
    dashboard.hidden = false;
    signOut.hidden = false;
    return true;
  } catch (error) {
    if (call !== requestVersion) return false;
    if (error.status === 401) showLogin(false);
    else message("#page-error", error);
    return false;
  } finally {
    find("#loading").hidden = true;
  }
}

loginForm.addEventListener("submit", async event => {
  event.preventDefault();
  const button = loginForm.querySelector("button");
  button.disabled = true;
  message("#login-error");
  try {
    await request("/login", Object.fromEntries(new FormData(loginForm)));
    loginForm.reset();
    if (await load()) find("#main").focus();
  } catch (error) {
    message("#login-error", error);
    find("#password").value = "";
    find("#password").focus();
  } finally {
    button.disabled = false;
  }
});

signOut.addEventListener("click", async () => {
  signOut.disabled = true;
  try {
    await request("/logout", {});
    requestVersion++;
    form.replaceChildren();
    page = 1;
    recordSort = "";
    showLogin(true);
  } catch (error) {
    message("#page-error", error);
  } finally {
    signOut.disabled = false;
  }
});
find("#find-assessment").addEventListener("submit", event => {
  event.preventDefault();
  const id = find("#lookup-id").value.trim().toUpperCase();
  if (/^[0-9A-F]{12}$/.test(id)) openReport(id);
});
form.addEventListener("submit", event => event.preventDefault());
form.addEventListener("change", () => { page = 1; load(); });
find("#reset").addEventListener("click", () => { form.reset(); page = 1; load(); });
reportDialog.addEventListener("close", () => { detailVersion++; reportContent.replaceChildren(); });
window.addEventListener("pageshow", event => { if (event.persisted) load(); });
load();
