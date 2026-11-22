"""Find explicit details in staff notes for questions that may come later."""

import re


# These cues surface context. They never infer an answer choice or clear a check.
CUES = {
    "existing": r"\b(?:built[- ]in|already (?:has|does|covers|supports)|existing (?:feature|report|template)|(?:checked|looked).{0,55}(?:feature|can already|nothing|couldn.t find))\b",
    "barrier": r"\b(?:need(?:s|ed)? (?:training|guidance|access|permissions?|to (?:set up|enable))|don.t know how to (?:find|run|use)|lack(?:s|ing)? (?:training|access))\b",
    "data": r"\b(?:criminal justice|patient|health records?|medical records?|CJIS|HIPAA|restricted|confidential|personally identifiable|routine (?:administrative|inventory)|(?:equipment|inventory|asset) (?:labels|tags|counts))\b",
    "systems": r"\b(?:from|between|copy\w*|mov\w*)\b.{1,100}\b(?:into|to|and)\b.{0,36}\b(?:tracker|spreadsheet|workbook|system|database|portal|shared (?:drive|folder)|app)\b|\b(?:stays? in|all in|kept in) (?:the|one|our)\b",
    "changes": r"\b(?:read[- ]only|only (?:reads?|drafts?)|no (?:write|admin) access|would (?:add|update|delete|send|write|edit)|administrator access|admin permissions?)\b",
    "impact": r"\b(?:if\b.{0,55}\b(?:wrong|incorrect|missed)|(?:could|would|might) (?:delay|cause rework|disclose|affect|hurt|mislead)|easy to fix)\b",
    "owner": r"\b(?:owns? (?:the |this |both )?(?:workflow|process|work|data|information)|(?:can|must) approve (?:the |this )?(?:access|use|permissions?)|process owner|data owner)\b",
    "boundary": r"\b(?:administrative (?:only|support)|(?:only|strictly|purely) administrative|no (?:live|operational) decisions?|live (?:dispatch|response|decision)|(?:affects?|influences?) (?:dispatch|enforcement|clinical care|.+? rights))\b",
    "frequency": r"\b(?:(?:every|each) (?:\w+ )?(?:morning|evening|shift|day|week|month|quarter|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)|daily|weekly|monthly|on (?:Mondays|Tuesdays|Wednesdays|Thursdays|Fridays|Saturdays|Sundays)|(?:when(?:ever)?|once) .{1,55}\b(?:arrives?|comes? in|is received)|(?:\d+|one|two|three|four|five|ten|twenty) (?:minutes?|hours?|times|items|requests|records|entries|forms|calls))\b",
    "rules": r"\b(?:fixed rules?|same (?:rules?|steps?|checks?)|(?:consistent|written|documented) rules?|(?:no|requires?|needs?) (?:manual |professional )?(?:judgment|interpretation)|whether .{1,60} (?:counts?|qualifies))\b",
    "input": r"\b(?:work from|inputs? (?:are|include|come from)|start(?:s)? with|comes? from|open\w*|receiv\w*|export\w*|use\w*)\b.{0,55}\b(?:forms?|lists?|logs?|spreadsheets?|notes?|emails?|documents?|records?|images?|workbooks?|CSV|tables?|messages?)\b|\b(?:forms?|lists?|logs?|spreadsheets?|notes?|emails?|documents?|messages?)\b.{0,50}\b(?:arrive|come in|are received)\b",
    "output": r"\b(?:want|need|produce|generate|end up with)\b.{0,45}\b(?:lists?|drafts?|reports?|summar(?:y|ies)|queues?|reminders?|results?|updates?|checklists?|dashboards?)\b|\b(?:the result|the output|should end with|at the end)\b",
    "judgment": r"\b(?:interpret\w*|use (?:their |professional )?judgment|decide whether|read between the lines|compare .{1,50} against the source)\b",
    "exceptions": r"\b(?:exception\w*|late|missing|duplicate\w*|conflict\w*)\b.{1,100}\b(?:flag\w*|review\w*|handle\w*|check\w*|send\w*|skip\w*|fix\w*|follow[- ]?up)\b",
    "people": r"\b(?:would use|uses? the (?:list|result|report|draft)|goes? to|for our|for the .{1,35} team|send\w* .{1,40} to (?:the|our)|send\w* (?:the |our )?(?:coordinator|lead|supervisor))\b",
    "tools": r"\b(?:approved (?:tool|app|software|workbook|platform)|(?:tool|app|software|workbook|platform) (?:is|was) approved|(?:new|external|outside) (?:vendor|AI service)|nothing (?:suitable|is) approved)\b",
    "review": r"\b(?:review\w*|check\w*|approv\w*|sign\w* off)\b.{0,90}\b(?:before|after)\b|\b(?:no one|nobody) (?:review\w*|check\w*|approv\w*)\b",
}
SIGNALS = {key: re.compile(pattern, re.I) for key, pattern in CUES.items()}
NOT_A_DETAIL = re.compile(r"\[email omitted\]|\b(?:ignore|return|output) (?:the|all|a JSON) (?:instructions?|prompts?|rules?|JSON|object)\b", re.I)
EXAMPLE = re.compile(
    r"^(?:for example,? )?(?:if|when) (.+?)(?:,\s*(?:then\s+)?|\s+then\s+)"
    r"((?:flag|mark|send|show|list|route|skip|record|add|leave|notify|return|"
    r"(?:the|staff|we) .{1,50} should)\b.+)$", re.I,
)
SPECIFIC_INPUT = re.compile(r"\b(?:row|record|entry|form|note|log|list|file|report|tracker|sheet|item|request|field|message|count|label|drill)s?\b", re.I)


def collect_context(note, answered):
    matches = {}
    for sentence in re.split(r"(?<=[.!?;])\s+|[\r\n]+", note):
        excerpt = sentence.strip()
        if not 12 <= len(excerpt) <= 280 or excerpt.endswith("?") or "@" in excerpt or NOT_A_DETAIL.search(excerpt):
            continue
        for key, cue in SIGNALS.items():
            if key not in answered and cue.search(excerpt):
                matches[key] = excerpt
        if "example" not in answered and (case := EXAMPLE.fullmatch(excerpt)):
            given, expected = case.groups()
            if SPECIFIC_INPUT.search(given) and len(given.split()) >= 4 and len(expected.split()) >= 4:
                matches["example"] = excerpt
    return matches


def earlier_detail(answers, key):
    for number, answer in reversed(list(enumerate(answers.values(), 1))):
        context = answer.get("prior_context")
        if context is None:  # Drafts saved before context screening can resume.
            context = collect_context(answer["note"], ())
        if excerpt := context.get(key):
            return {"excerpt": excerpt, "source_number": number}
    return None


def reused_example(answers):
    if "example" not in answers:
        return earlier_detail(answers, "example")
    return None
