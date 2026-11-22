"use strict";

const screen = document.querySelector("#screen");
const home = document.querySelector("#home");
const status = document.querySelector("#status");
const progress = document.querySelector("#progress");
const mode = document.querySelector("#mode");
const sessionKey = "flagstaff-navigator-session";
let options;
let current;
let busy = false;

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text) element.textContent = text;
  if (className) element.className = className;
  return element;
}

function button(text, className, action) {
  const item = node("button", text, className);
  item.type = "button";
  item.addEventListener("click", action);
  return item;
}

function heading(kicker, title, description) {
  const header = node("header", null, "page-heading");
  if (kicker) header.append(node("p", kicker, "staff-caption"));
  header.append(node("h1", title));
  if (description) header.append(node("p", description, "intro"));
  return header;
}

function setupPage(stage, focus = true) {
  document.body.dataset.stage = ["start", "questions", "review", "receipt"][stage];
  home.hidden = stage === 0;
  home.textContent = stage === 3 ? "Start another interview" : "Start over";
  progress.hidden = stage === 0 || stage === 3;
  progress.querySelectorAll("li").forEach((item, index) => {
    item.className = index < stage ? "done" : index === stage ? "active" : "";
    if (index === stage) item.setAttribute("aria-current", "step");
    else item.removeAttribute("aria-current");
  });
  status.textContent = "";
  if (!focus) return;
  const heading = screen.querySelector("h1");
  heading.tabIndex = -1;
  heading.focus({ preventScroll: true });
  window.scrollTo({ top: 0, behavior: "instant" });
}

async function api(path, payload) {
  const config = payload ? {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
  } : {};
  const response = await fetch(path, config);
  const result = await response.json();
  if (!response.ok) {
    const error = new Error(result.error ?? "Try that action again.");
    error.status = response.status;
    throw error;
  }
  return result;
}

function showError(error, errorBox) {
  errorBox.textContent = error.message || "Could not reach Flagstaff WIP. Try again.";
  errorBox.hidden = false;
}

function errorMessage() {
  const error = node("p", "", "error");
  error.hidden = true;
  error.setAttribute("role", "alert");
  return error;
}

async function runAction(control, error, work) {
  if (busy) return;
  busy = true;
  home.disabled = true;
  control.disabled = true;
  error.hidden = true;
  status.textContent = "Working…";
  try {
    await work();
  } catch (problem) {
    showError(problem, error);
    if (problem.status === 409 && current) {
      status.textContent = "Reloading the latest interview.";
      try {
        await refresh();
      } catch (reloadProblem) {
        showError(reloadProblem, error);
      }
    }
  } finally {
    busy = false;
    home.disabled = false;
    control.disabled = false;
    status.textContent = "";
  }
}

function renderHome(focus) {
  const header = heading("For public safety staff", "What could work better?",
    "Pick one task your team does today. Tell us what starts it, what you do, and what would make it easier or more reliable.");
  const example = node("p", null, "start-example");
  example.append(node("strong", "Example"), document.createTextNode(
    "“Every Thursday, I check the sign-out sheet for borrowed radio chargers. I copy the overdue entries into a list and send it to the training lead. An up-to-date list by room would help us follow up without copying the entries each week.”"));
  const expect = node("p", null, "start-expect");
  expect.append(node("strong", "What to expect"), document.createTextNode(
    "We’ll build on what you share and ask you to confirm details like what information the change would use. You can review your answers before sending them to IT. Keep the assessment ID you receive for follow-up."));
  header.append(example, expect);
  header.append(node("p", "Leave case, patient and personnel records out of your answers.", "start-privacy"));
  const grid = node("div", null, "start-layout");
  const primary = node("section", null, "card start-card");
  primary.append(node("h2", "Get started"));
  const fields = node("form");
  const nameLabel = node("label", "Name", "field-label");
  nameLabel.htmlFor = "contact-name";
  const name = node("input");
  name.type = "text";
  name.id = nameLabel.htmlFor;
  name.required = true;
  name.maxLength = 120;
  name.autocomplete = "name";
  const emailLabel = node("label", "Email address", "field-label");
  emailLabel.htmlFor = "contact-email";
  const email = node("input");
  email.type = "email";
  email.id = emailLabel.htmlFor;
  email.required = true;
  email.maxLength = 254;
  email.autocomplete = "email";
  const purpose = node("p", "IT uses these details for follow-up.", "contact-note");
  purpose.id = "contact-purpose";
  name.setAttribute("aria-describedby", purpose.id);
  email.setAttribute("aria-describedby", purpose.id);
  const contact = node("div", null, "contact-fields");
  contact.append(nameLabel, name, emailLabel, email, purpose);
  const selectLabel = node("label", "Department", "field-label");
  selectLabel.htmlFor = "department";
  const select = node("select");
  select.id = "department";
  select.required = true;
  const placeholder = node("option", "Select a department");
  placeholder.value = "";
  placeholder.disabled = true;
  placeholder.selected = true;
  select.append(placeholder);
  for (const department of options.departments) select.append(node("option", department));
  const submit = node("button", "Begin interview", "primary");
  submit.type = "submit";
  const error = errorMessage();
  fields.append(contact, selectLabel, select, submit);
  fields.addEventListener("submit", event => {
    event.preventDefault();
    runAction(submit, error, () => start({
      department: select.value,
      contact: { name: name.value.trim(), email: email.value.trim() },
    }));
  });
  primary.append(fields);
  const practice = node("details", null, "practice-picker");
  practice.append(node("summary", "Try a practice scenario"),
    node("p", "Choose an example and use the sample answers as you go.", "muted"));
  const scenarios = node("div", null, "practice-options");
  for (const scenario of options.scenarios) {
    const card = button("", "scenario", event => {
      runAction(event.currentTarget, error, () => start({ scenario: scenario.id }));
    });
    card.append(node("span", scenario.department, "scenario-department"),
      node("strong", scenario.title), node("span", scenario.description, "scenario-description"));
    scenarios.append(card);
  }
  practice.append(scenarios);
  grid.append(header, primary);
  screen.replaceChildren(error, grid, practice);
  setupPage(0, focus);
}

async function start(selection) {
  current = await api("/api/sessions", selection);
  sessionStorage.setItem(sessionKey, current.id);
  render();
}

async function refresh() {
  current = await api(`/api/sessions/${current.id}`);
  render();
}

async function change(action) {
  current = await api(`/api/sessions/${current.id}`, { ...action, revision: current.revision });
  render();
}

function answerList(items, editable) {
  const list = node("div", null, "answer-list");
  for (const item of items) {
    const row = node("div", null, "answer-row");
    const detail = node("div");
    detail.append(node("h3", item.title));
    if (item.answer) detail.append(node("p", item.answer, "response"));
    if (item.note) detail.append(node("p", item.note, "muted"));
    if (item.source_number) detail.append(node("small", `Detail from question ${item.source_number}`, "muted"));
    if (!item.note && !item.answer) detail.append(node("p", "Skipped", "muted"));
    row.append(detail);
    if (editable) {
      const edit = button("Change", "ghost", event => {
        if (!window.confirm("Editing this answer clears the answers after it so the interview can adjust. Continue?")) return;
        runAction(event.currentTarget, document.querySelector(".error"), () => change({ action: "revise", id: item.id }));
      });
      edit.setAttribute("aria-label", `Change answer to “${item.title}”`);
      row.append(edit);
    }
    list.append(row);
  }
  return list;
}

const editGuidance = "Changing an earlier answer clears the answers that follow it so the interview can adapt.";

function renderQuestion() {
  const question = current.question;
  const isOpeningQuestion = question.id === "goal";
  const count = current.evidence.length;
  const form = node("form", null, "card question-card");
  const error = errorMessage();
  const tools = node("div", null, "question-tools");
  if (count) tools.append(button("← Back", "ghost back-link", event =>
    runAction(event.currentTarget, error, () => change({ action: "back" }))));
  tools.append(node("span", `${current.department} · Question ${count + 1}`, "question-position"));
  if (question.selection === "local AI") tools.append(node("span", "Local AI follow-up", "question-source"));
  const title = node("h1", question.title);
  title.id = "question-title";
  const hint = node("p", question.hint, "question-hint");
  hint.id = "question-hint";
  form.setAttribute("aria-labelledby", title.id);
  form.append(tools, title, hint);
  if (question.why) {
    const why = node("details", null, "question-why");
    why.append(node("summary", "Why are we asking?"), node("p", question.why));
    form.append(why);
  }
  if (question.process_context) {
    const context = node("div", null, "opening-example");
    context.append(node("strong", "From your first answer"),
      list(question.process_context.map(excerpt => `“${excerpt}”`)));
    form.append(context);
  }
  if (question.process_reused) {
    form.append(node("p", "Your first answer already covers how the task works.", "opening-example"));
  }
  let choices;
  const prefill = current.draft || {};
  const earlier = question.earlier_detail;
  if (question.options.length) {
    choices = node("fieldset", null, "choices");
    choices.append(node("legend", earlier ? "Confirm the option that fits" : "Choose one answer", "sr-only"));
    choices.setAttribute("aria-describedby", earlier ? `${hint.id} earlier-detail` : hint.id);
    for (const option of question.options) {
      const label = node("label", null, "choice");
      const radio = node("input");
      radio.type = "radio";
      radio.name = "value";
      radio.value = option.value;
      radio.required = true;
      radio.checked = option.value === prefill.value;
      label.append(radio, node("span", option.label));
      choices.append(label);
    }
  }
  const answerLabel = question.note === "required" ? "Your answer" : "Your answer (optional)";
  const label = question.detail ? `${question.detail} (optional)` : answerLabel;
  const noteLabel = node("label", isOpeningQuestion ? "The task today and what could be better" : label, "field-label");
  noteLabel.htmlFor = "note";
  const note = node("textarea");
  note.id = "note";
  note.name = "note";
  note.maxLength = 900;
  note.setAttribute("aria-describedby", hint.id);
  note.value = prefill.note || "";
  note.required = question.note === "required";
  note.minLength = note.required ? 8 : 0;
  const noteGroup = node("div", null, choices ? "question-note compact-note" : "question-note");
  if (choices && !question.example_answer) note.placeholder = question.placeholder;
  noteGroup.append(noteLabel, note);

  if (earlier) {
    const context = node("div", null, "opening-example earlier-detail");
    const excerpt = node("div");
    excerpt.id = "earlier-detail";
    excerpt.append(node("strong", `From your answer to question ${earlier.source_number}`),
      node("div", `“${earlier.excerpt}”`), node("p", "Confirm which option fits below.", "muted"));
    const include = button("Include this detail", "ghost", () => {
      const existing = note.value.trim();
      if (!existing.includes(earlier.excerpt)) {
        const combined = [earlier.excerpt, existing].filter(Boolean).join("\n");
        if (combined.length > note.maxLength) {
          note.focus();
          status.textContent = "This detail would put your note over 900 characters. You can shorten your note.";
          return;
        }
        note.value = combined;
      }
      note.focus();
      status.textContent = "Earlier detail included. You can edit it.";
    });
    context.append(excerpt, include);
    form.append(context);
  }

  if (question.example_answer) {
    const fill = button("Use example answer", "secondary example-action", () => {
      const answer = question.example_answer;
      const matching = choices ? [...choices.querySelectorAll("input")].find(radio => radio.value === answer.value) : null;
      if (matching) matching.checked = true;
      note.value = answer.note;
      if (matching) matching.focus({ preventScroll: true });
      else note.focus({ preventScroll: true });
      status.textContent = "Example answer filled in. You can edit it.";
    });
    form.append(fill);
  }
  if (choices) form.append(choices);
  const showExample = !choices && !question.example_answer && Boolean(question.placeholder);
  if (showExample && isOpeningQuestion) {
    const example = node("p", null, "opening-example");
    example.id = "opening-example";
    example.append(node("strong", "Example"), document.createTextNode(` ${question.placeholder}`));
    note.setAttribute("aria-describedby", `${hint.id} ${example.id}`);
    form.append(example);
  }
  form.append(noteGroup);
  if (showExample && !isOpeningQuestion) {
    const example = node("details", null, "question-example");
    example.append(node("summary", "See an example"), node("p", question.placeholder));
    form.append(example);
  }
  form.append(error);
  const actions = node("div", null, "actions question-actions");
  const next = node("button", "Continue", "primary");
  next.type = "submit";
  actions.append(next);
  form.append(actions);
  form.addEventListener("submit", event => {
    event.preventDefault();
    const data = new FormData(form);
    runAction(next, error, async () => {
      next.textContent = question.alternatives > 1 ? "Continuing…" : "Saving…";
      try {
        await change({ action: "answer", id: question.id, value: data.get("value") || "", note: note.value });
      } finally {
        next.textContent = "Continue";
      }
    });
  });

  screen.replaceChildren(form);
  if (count) {
    const details = node("details", null, "question-history history");
    details.append(node("summary", `Earlier answers (${count})`),
      node("p", editGuidance, "muted"), answerList(current.evidence, false));
    screen.append(details);
  } else {
    screen.append(node("p", editGuidance, "question-footnote"));
  }
  setupPage(1);
}

function renderReview() {
  const header = heading(current.department, "Check your answers",
    "Read through what you shared. You can make changes before sending it to IT.");
  const card = node("section", null, "card review-card");
  const error = errorMessage();
  const benefit = node("div", null, "benefit-form");
  const label = node("label", "How much would this help? (optional)", "field-label");
  label.htmlFor = "expected-benefit";
  const select = node("select");
  select.id = label.htmlFor;
  select.setAttribute("aria-describedby", "benefit-hint");
  const help = node("p", "Think about time saved, fewer mistakes, or more reliable work.", "muted");
  help.id = "benefit-hint";
  for (const key of ["unknown", "low", "moderate", "high"]) {
    select.append(new Option(options.benefits[key], key));
  }
  benefit.append(label, help, select);
  const actions = node("div", null, "actions");
  actions.append(button("Submit to IT", "primary", event =>
    runAction(event.currentTarget, error, () => change({ action: "finish", expected_benefit: select.value }))));
  card.append(error, node("p", editGuidance, "muted"));
  if (current.reused_example) {
    const example = node("div", null, "opening-example");
    example.append(node("strong", `Example from question ${current.reused_example.source_number}`),
      node("div", `“${current.reused_example.excerpt}”`));
    card.append(example);
  }
  card.append(answerList(current.evidence, true), benefit, actions);
  const why = node("details", null, "question-history completion-note");
  why.append(node("summary", "Why did the questions end?"),
    node("p", `You answered ${current.evidence.length} questions. ${current.review_reason || "Your answers are ready for review."}`));
  screen.replaceChildren(header, why, card);
  setupPage(2);
}

function reportBlock(title, content) {
  const section = node("section", null, "report-block");
  section.append(node("h2", title), content);
  return section;
}

function list(items, ordered = false) {
  const container = node(ordered ? "ol" : "ul", null, "clean-list");
  for (const item of items) container.append(node("li", item));
  return container;
}

function definitionList(pairs) {
  const container = node("dl", null, "definition-list");
  for (const [title, value] of pairs) {
    const group = node("div");
    group.append(node("dt", title), node("dd", value));
    container.append(group);
  }
  return container;
}

function assessmentReceipt(report) {
  const receipt = node("section", null, "card assessment-receipt");
  receipt.setAttribute("aria-labelledby", "receipt-title");
  const title = node("h1", "Your assessment is saved.");
  title.id = "receipt-title";
  const updates = {
    reviewed: "IT has marked your assessment reviewed.",
    needs_info: "IT needs more information to continue reviewing your assessment.",
    approved: "IT has approved the next step for your assessment.",
    closed: "IT has closed this assessment.",
  };
  const explanation = updates[current.review_status] || (current.scenario
    ? "This practice assessment is available in the IT review queue."
    : current.has_contact
      ? "IT will review your submission and use the email you provided for follow-up."
      : "Your assessment is available in the IT review queue.");
  receipt.append(title, node("p", explanation));
  receipt.append(node("p", "Keep this ID handy if you contact IT about your idea.", "muted"));
  const label = node("label", "Assessment ID", "field-label");
  label.htmlFor = "assessment-id";
  const id = node("input");
  id.id = label.htmlFor;
  id.type = "text";
  id.readOnly = true;
  id.value = report.id;
  const feedback = node("span", "", "copy-feedback");
  feedback.setAttribute("role", "status");
  const copy = button("Copy assessment ID", "secondary", async () => {
    try {
      await navigator.clipboard.writeText(report.id);
      feedback.textContent = "Assessment ID copied.";
    } catch {
      id.focus();
      id.select();
      feedback.textContent = "ID selected. Use your device’s copy shortcut.";
    }
  });
  const download = node("a", "Download assessment", "ghost");
  download.href = `/api/sessions/${current.id}/download`;
  const field = node("div", null, "receipt-actions");
  field.append(id, copy, download);
  receipt.append(label, field, feedback);
  return receipt;
}

function renderReport() {
  const report = current.report;
  const d = report.decision;
  const featured = node("section", null, "report-main");
  const tiles = node("div", null, "decision-grid");
  for (const [label, value] of [["SOLUTION FIT", d.label], ["RISK", d.risk], [`IT INVOLVEMENT · TIER ${d.tier}`, d.it]]) {
    const tile = node("div", null, "decision");
    tile.append(node("p", label, "eyebrow"), node("h2", value));
    tiles.append(tile);
  }
  const governance = {
    hold: current.review_status === "awaiting" ? "On hold pending IT review" : "Governance review required",
    cleared: "Governance clearance recorded",
    closed: "Closed with governance flags",
    ready: "No governance hold",
  };
  const activeHold = current.governance_status === "hold";
  const route = node("aside", null, activeHold ? "route hold receipt-hold" : "route");
  route.append(node("strong", governance[current.governance_status]));
  if (activeHold && report.first_action) {
    route.append(node("p", report.first_action.action));
  } else if (!d.hold) {
    route.append(node("p", d.route));
  }
  if (!activeHold) featured.append(route);
  featured.append(tiles, node("p", d.rationale), node("p", d.recommendation));

  const risk = node("ul", null, "check-list");
  for (const check of report.checks) {
    const item = node("li");
    item.append(node("span", check.level, `pill ${check.level}`), node("strong", check.name),
      node("p", check.reason), node("small", check.reviewer));
    risk.append(item);
  }
  const explain = node("div", null, "score-grid");
  const questionTitles = new Map(report.evidence.map((answer, index) => [answer.id, `Q${index + 1} · ${answer.question}`]));
  for (const [key, score] of Object.entries(report.scores)) {
    const item = node("div");
    item.append(node("h3", `${key === "ai" ? "AI" : "Automation"} · ${score.total}/10`),
      score.items.length ? list(score.items.map(signal =>
        [`+${signal.points} ${signal.evidence}`, questionTitles.get(signal.field)].filter(Boolean).join(" · "))) :
        node("p", "No scored signals were collected.", "muted"));
    explain.append(item);
  }
  const count = node("p", `${report.question_count} answers · ${report.model_count} local AI follow-up selections · Rules ${report.version}`, "muted");
  const evidence = node("details", null, "report-block");
  evidence.append(node("summary", "Read the interview record"), answerList(report.evidence.map(item => ({
    ...item, title: item.question,
  })), false));
  const assumptions = report.assumptions.map(value => value.replace(/^The scenario and examples are fictional\. /, ""));
  const detail = node("details", null, "card staff-assessment");
  detail.append(node("summary", "View assessment details"), featured,
    reportBlock("Next steps", list(report.next_actions.map(action => `${action.owner} — ${action.action}`), true)),
    reportBlock("Current workflow", definitionList(Object.entries(report.workflow))),
    reportBlock("Risk and governance", risk),
    reportBlock("Proposed requirements", list(report.requirements)),
    reportBlock("Screening scores", explain),
    reportBlock("Assumptions and open questions", list([...assumptions, ...report.unknowns])),
    evidence, count);
  screen.replaceChildren(assessmentReceipt(report));
  if (activeHold) screen.append(route);
  screen.append(detail);
  setupPage(3);
}

function render() {
  if (!current) renderHome(true);
  else if (current.report) renderReport();
  else if (current.question) renderQuestion();
  else renderReview();
}

home.addEventListener("click", () => {
  if (!current.report && !window.confirm("Start over and leave this interview?")) return;
  sessionStorage.removeItem(sessionKey);
  current = null;
  render();
});

async function initialize() {
  try {
    options = await api("/api/options");
    const saved = sessionStorage.getItem(sessionKey);
    if (saved) {
      try {
        current = await api(`/api/sessions/${saved}`);
      } catch (error) {
        if (error.status !== 404) throw error;
        sessionStorage.removeItem(sessionKey);
      }
    }
    if (current) render();
    else renderHome(false);
    try {
      const health = await api("/api/health");
      mode.lastChild.textContent = health.model_ready ? " Local AI ready" : " Local rules ready";
    } catch {
      mode.lastChild.textContent = " Interview ready";
    }
  } catch {
    screen.replaceChildren(heading("Flagstaff WIP", "The interview is unavailable",
      "Check that the local app is running, then reload this page."));
  }
}
initialize();
