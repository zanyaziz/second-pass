"""Build the Second Pass site (index.html + one page per course) from data/courses.json."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
data = json.loads((ROOT / "data" / "courses.json").read_text())

CSS = """
  :root { --bg:#12100c; --card:#1d1a14; --ink:#f0e9da; --muted:#a89f8d; --accent:#e0a458;
          --good:#7bc47f; --bad:#e07a5f; --line:#2e2a21; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
         background:var(--bg); color:var(--ink); line-height:1.55; }
  header { text-align:center; padding:3rem 1.5rem 1.5rem; }
  h1 { margin:.5rem 0 .25rem; font-size:2rem; }
  .sub { color:var(--muted); margin:0 0 2rem; }
  main { max-width:860px; margin:0 auto; padding:0 1.25rem 3rem; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:16px;
          padding:1.5rem; margin-bottom:1.25rem; }
  .ep { display:inline-block; font-size:.75rem; letter-spacing:.12em; text-transform:uppercase;
        color:var(--accent); border:1px solid var(--accent); border-radius:999px;
        padding:.15rem .75rem; margin-bottom:.5rem; }
  .card h2 { margin:.25rem 0 .1rem; font-size:1.4rem; }
  .author { color:var(--muted); margin:0 0 .75rem; font-style:italic; }
  .concepts { color:var(--muted); font-size:.92rem; margin:.25rem 0 .75rem; }
  .blurb { margin:.5rem 0 1rem; }
  audio { width:100%; margin:.25rem 0 1rem; }
  .pending-note { background:#2a2415; border:1px dashed var(--accent); border-radius:10px;
                  padding:.75rem 1rem; color:var(--muted); }
  .btn { display:inline-block; text-decoration:none; padding:.55rem 1rem; border-radius:10px;
         font-size:.95rem; border:1px solid #3a352a; color:var(--ink); background:transparent;
         cursor:pointer; font-family:inherit; }
  .btn.primary { background:var(--accent); color:#1a1408; border-color:var(--accent); font-weight:600; }
  .btn:disabled { opacity:.4; cursor:default; }
  a { color:var(--accent); }
  .back { display:inline-block; margin:1.25rem 0 0 1.25rem; }
  fieldset.q { border:1px solid var(--line); border-radius:12px; margin:0 0 1rem; padding:1rem 1.25rem 1.25rem; }
  fieldset.q legend { font-weight:600; padding:0 .4rem; }
  fieldset.q label { display:block; padding:.35rem .5rem; border-radius:8px; cursor:pointer; }
  fieldset.q label:hover { background:#262219; }
  fieldset.q.missing { border-color:var(--bad); }
  fieldset.q.right { border-color:var(--good); }
  fieldset.q.wrong { border-color:var(--bad); }
  .opt-correct { background:rgba(123,196,127,.15); outline:1px solid var(--good); }
  .opt-picked-wrong { background:rgba(224,122,95,.15); outline:1px solid var(--bad); }
  .why { display:none; margin:.75rem 0 0; padding:.75rem 1rem; border-radius:10px;
         background:#262219; color:var(--ink); font-size:.95rem; }
  .why.show { display:block; }
  .verdict { font-weight:700; }
  .verdict.ok { color:var(--good); } .verdict.no { color:var(--bad); }
  .score { font-size:1.1rem; font-weight:700; margin:1rem 0; }
  .quiz-msg { color:var(--bad); font-weight:600; min-height:1.4em; }
  footer { text-align:center; color:var(--muted); font-size:.85rem; padding:2rem 1rem; }
"""

QUIZ_JS = """
<script>
function initQuiz(rootId, quizData) {
  var root = document.getElementById(rootId);
  var form = root.querySelector('form');
  var msg = root.querySelector('.quiz-msg');
  var scoreEl = root.querySelector('.score');
  quizData.forEach(function(item, qi) {
    var fs = document.createElement('fieldset');
    fs.className = 'q'; fs.dataset.answer = item.answer;
    var lg = document.createElement('legend');
    lg.textContent = 'Q' + (qi + 1) + '. ' + item.q;
    fs.appendChild(lg);
    item.options.forEach(function(opt, oi) {
      var label = document.createElement('label');
      var input = document.createElement('input');
      input.type = 'radio'; input.name = rootId + '-q' + qi; input.value = oi;
      label.appendChild(input);
      label.appendChild(document.createTextNode(' ' + opt));
      fs.appendChild(label);
    });
    var why = document.createElement('p');
    why.className = 'why'; why.textContent = item.why;
    fs.appendChild(why);
    form.appendChild(fs);
  });
  root.querySelector('.check-btn').addEventListener('click', function() {
    var fieldsets = form.querySelectorAll('fieldset.q');
    var missing = 0, score = 0;
    fieldsets.forEach(function(fs) {
      var picked = fs.querySelector('input[type=radio]:checked');
      fs.classList.remove('missing');
      if (!picked) { missing++; fs.classList.add('missing'); }
    });
    if (missing > 0) {
      msg.textContent = 'Answer all ' + fieldsets.length + ' questions first — ' + missing + ' to go.';
      return;
    }
    msg.textContent = '';
    fieldsets.forEach(function(fs) {
      var answer = parseInt(fs.dataset.answer, 10);
      var picked = fs.querySelector('input[type=radio]:checked');
      var labels = fs.querySelectorAll('label');
      labels[answer].classList.add('opt-correct');
      var verdict = document.createElement('p');
      verdict.className = 'verdict';
      if (parseInt(picked.value, 10) === answer) {
        score++; fs.classList.add('right');
        verdict.classList.add('ok'); verdict.textContent = '✓ Correct';
      } else {
        fs.classList.add('wrong');
        picked.closest('label').classList.add('opt-picked-wrong');
        verdict.classList.add('no'); verdict.textContent = '✗ Not quite — the highlighted answer is the right one.';
      }
      fs.appendChild(verdict);
      fs.querySelector('.why').classList.add('show');
      fs.querySelectorAll('input').forEach(function(i) { i.disabled = true; });
    });
    scoreEl.textContent = 'You scored ' + score + ' out of ' + fieldsets.length + '.';
    root.querySelector('.check-btn').disabled = true;
    root.querySelector('.retry-btn').style.display = 'inline-block';
  });
  root.querySelector('.retry-btn').addEventListener('click', function() { location.reload(); });
}
</script>
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
{body}
<footer>Second Pass — short audio courses on books worth a second, deeper pass.</footer>
</body>
</html>
"""


def build_index():
    cards = []
    for c in data["courses"]:
        live = sum(1 for ch in c["chapters"] if ch.get("audio"))
        cards.append(f"""
    <article class="card">
      <div class="ep">Course</div>
      <h2>{esc(c['title'])}</h2>
      <p class="author">{esc(c['author'])}</p>
      <p class="blurb">{esc(c['blurb'])}</p>
      <p class="concepts">{len(c['chapters'])} chapters · {live} available now</p>
      <a class="btn primary" href="{c['slug']}.html">Open the course</a>
    </article>""")
    body = f"""
<header>
  <h1>Second Pass</h1>
  <p class="sub">A few books deserve more than a summary. These are the ones — broken into short audio chapters, each with a quiz to make the ideas stick.</p>
</header>
<main>
{''.join(cards)}
</main>"""
    (ROOT / "index.html").write_text(page("Second Pass — Book Courses", body))
    print("wrote index.html with", len(data["courses"]), "course(s)")


def quiz_block(ch):
    qid = f"quiz-{ch['slug']}"
    quiz_json = json.dumps(ch["quiz"])
    return f"""
      <div class="quiz" id="{qid}">
        <h3>Quiz — {len(ch['quiz'])} questions</h3>
        <p class="concepts">Answer all {len(ch['quiz'])}, then check yourself. Explanations appear under every question.</p>
        <form></form>
        <p class="quiz-msg"></p>
        <button type="button" class="btn primary check-btn">Check my answers</button>
        <button type="button" class="btn retry-btn" style="display:none">Try again</button>
        <p class="score"></p>
      </div>
<script type="application/json" id="{qid}-data">{quiz_json}</script>"""


def build_course(c):
    parts = [f"""
<a class="back" href="index.html">← All courses</a>
<header>
  <h1>{esc(c['title'])}</h1>
  <p class="sub">by {esc(c['author'])} · {len(c['chapters'])} chapters</p>
</header>
<main>"""]
    quiz_inits = []
    for ch in c["chapters"]:
        block = f"""
    <article class="card" id="chapter-{ch['n']}">
      <div class="ep">Chapter {ch['n']}</div>
      <h2>{esc(ch['title'])}</h2>
      <p class="concepts">{esc(ch['concepts'])}</p>"""
        if ch.get("audio"):
            block += f"""
      <audio controls preload="none" src="{ch['audio']}"></audio>"""
            if ch.get("duration"):
                block += f"""
      <p class="concepts">🎧 {esc(ch['duration'])}</p>"""
        else:
            block += """
      <div class="pending-note">🎧 Audio coming soon — this chapter is in production.</div>"""
        if ch.get("quiz"):
            block += quiz_block(ch)
            quiz_inits.append(
                f"initQuiz('quiz-{ch['slug']}', JSON.parse(document.getElementById('quiz-{ch['slug']}-data').textContent));")
        block += "\n    </article>"
        parts.append(block)
    parts.append("</main>")
    if quiz_inits:
        parts.append(QUIZ_JS)
        parts.append("<script>\n" + "\n".join(quiz_inits) + "\n</script>")
    out = ROOT / f"{c['slug']}.html"
    out.write_text(page(f"{c['title']} — Second Pass", "\n".join(parts)))
    print(f"wrote {out.name} with {len(c['chapters'])} chapters")


if __name__ == "__main__":
    build_index()
    for course in data["courses"]:
        build_course(course)
