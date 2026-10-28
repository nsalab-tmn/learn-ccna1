# Floor and with-lecture measurement of the module 01 self-checks (kb#536, item 3)

Raw judge outputs behind the before/after table of learn-ccna1 #351. Method, as in the learning-study pilot
(`learn-knowledge-base`, `design/learning-study/pilot/student/tools`):

- for every material the questions are shuffled and relabelled with `build_inputs.py --seed 518`; `key.json` is
  the key after the shuffle;
- `F1.md`–`F3.md`: three fresh sub-agents play the pilot's persona (`00-persona.md`) with the question sheet only
  (prompt `F-floor.md`); an item is «floor» when at least two of three answer it right;
- `S.md`: one fresh sub-agent plays the learner who has just read the lecture, with the figures and the pilot's
  notebook of the earlier materials; `E.md` (the exam): the same learner closed-book with the notebook of all seven
  materials;
- `score.json`: the pilot's `score.py` over these files (`floor`, `S_score`, `proves_something` = right for the
  learner and wrong for the persona, the judges' own labels «знаю / догадался по формулировке / наугад» and
  «понимание / узнавание слова»).

No judge saw the author's notes or another judge's answers; the author never judged their own items.

- `final/` — the run on the text of the PR as merged; `selfcheck.md` is the shuffled sheet the judges saw.
- `rounds/v2`, `rounds/v3`, `rounds/v4` — the earlier rounds, on the text of the commits they measured
  (PR branch commits `08b564a` / `5d590b7` / `74d6757`); a material absent from a round was not changed in it. The first draft's run was discarded: its key was regenerated after the text changed, so its
  scores were invalid.

## Module 03 (learn-ccna1 PR for kb#536 item 3, module 03)

Same method; the S judge of each lecture carries the pilot's notebook of all materials before it
(`notebook/15-02.08…` for 03.01 up to `21-03.06…` for 03.07), the exam judge E the notebook after 03.07.
«Before» is the pilot's run on the original banks (`pilot/student/raw/03.*/score.json`); `final/03.*` is the run on
the text of the PR as merged.
