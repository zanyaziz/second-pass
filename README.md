# Second Pass

Short audio courses on the few books worth a second, deeper pass.

Each course breaks a book into its key concepts and chapters. Every chapter is a 10–15 minute single-narrator audio lesson (up to 20 minutes where a chapter needs it), followed by a collapsed 10-question quiz card — click the card to reveal the questions, answer all 10, submit, and the page marks your answers and explains why each correct answer is right. Collapsing the card again keeps your answers (it does not re-render or reset them). The audio lessons themselves do not end with questions: each closes with a short summary, so a course can be listened to straight through.

Continuous play is on by default: when a chapter's audio ends, the next chapter starts automatically and scrolls into view, so a course plays straight through like a podcast. Untick "Continuous play" at the top of a course page to stop at the end of each chapter.

**Live site:** https://zanyaziz.github.io/second-pass/

## Courses

- **Thinking, Fast and Slow** by Daniel Kahneman — 12 chapters, all live with audio + quiz (about 2 hours 48 minutes total).
- **The Conquest of Happiness** by Bertrand Russell — 17 chapters, all live with audio + quiz (about 4 hours 3 minutes total).

## How it is built

- `data/courses.json` is the source of truth (courses → chapters → audio path + quiz sets), the same pattern as the book library's `books.json`.
- `python3 build.py` regenerates `index.html` and one page per course.
- Audio lives in `assets/audio/`. To add a chapter: produce the lesson, add its file, fill in the chapter's `audio`, `duration`, and `quiz` in `data/courses.json`, rerun `build.py`, commit, push.

Audio is generated privately for personal learning; nothing here is published to any podcast or RSS feed.
