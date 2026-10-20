# Second Pass

Short audio courses on the few books worth a second, deeper pass.

Each course breaks a book into its key concepts and chapters. Every chapter is a 5–10 minute single-narrator audio lesson, followed by a 10-question quiz built into the page — answer all 10, submit, and the page marks your answers and explains why each correct answer is right.

**Live site:** https://zanyaziz.github.io/second-pass/

## First course

- **Thinking, Fast and Slow** by Daniel Kahneman — 12 chapters. Chapter 1 (The Two Systems) is live with audio + quiz; the remaining chapters are listed and added as their audio is produced.

## How it is built

- `data/courses.json` is the source of truth (courses → chapters → audio path + quiz sets), the same pattern as the book library's `books.json`.
- `python3 build.py` regenerates `index.html` and one page per course.
- Audio lives in `assets/audio/`. To add a chapter: produce the lesson, add its file, fill in the chapter's `audio`, `duration`, and `quiz` in `data/courses.json`, rerun `build.py`, commit, push.

Audio is generated privately for personal learning; nothing here is published to any podcast or RSS feed.
