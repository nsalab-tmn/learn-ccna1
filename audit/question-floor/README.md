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

## Module 02 (learn-ccna1 PR for kb#536 item 3, module 02)

Same method and persona; the S judge of each lecture carries the pilot's notebook of all materials before it
(`notebook/07-01.08…` for 02.01 up to `14-02.07…` for 02.08), the exam judge E the notebook after 02.08.
«Before» is the pilot's run on the original banks (`pilot/student/raw/02.*/score.json`).

- `final/02.*` — the run on the text of the PR as merged: 02.02 and 02.10 from round 4, 02.03, 02.04, 02.05 and 02.07
  from round 3, 02.01, 02.06 and 02.08 from round 1 (their banks and keys did not change between the rounds; 02.01 changed only
  an answer comment, which the judges do not see).
- `rounds/m02-v1/` — round 1 on every material (PR branch commit `5ae9bcf`); 02.05 was revised after it
  (q01 key without the word «энергозависимая», a4 added; q08-a2 replaced by a5) and re-judged.
- `rounds/m02-v2/` — round 2, the run kb reviewed (PR branch commit `462a596`): 02.05 re-judged, the rest as in
  round 1. After the review 02.02, 02.03, 02.05 and 02.07 each lost one added item, 02.03 q11 became q03 and
  02.07 q07 became q01, 02.04 q14-a2 was reworded, and the exam replaced thirteen recall items with cases
  (q45–q57) and dropped the medium from the reload item (q57 for q36); those six materials were re-judged.
- `rounds/m02-v3/` — round 3 of 02.02 and 02.10, the run kb re-reviewed (commit `ab111c7`). After it 02.02 lost q13
  (the exam's q55 tests the same point), and the exam re-cased q46, q49, q51, q53 and q56 (they mirrored self-check
  items), fixed q55's premise, gave q47 two keys of four and relabelled q45 and q07 `remember`; both were re-judged.
  02.07 changed only a comment.
- 01.10 q56: after the module-01 run in `final/01.10-exam` the wording of a1 and a4 changed (both now about
  sending reports, teacher track); the key and the other options did not, so the run was not repeated.
- 02.10 q49: after round 4 the key's wording changed from «Из этой строки его не узнать: пароль зашифрован» to «В записи
  его нет открытым текстом: он зашифрован» (kb: the algorithm is weak), with the same meaning; the sheets in
  `final/02.10-exam` and `rounds/` show the earlier wording, and the run was not repeated.

## Module 03 (learn-ccna1 PR for kb#536 item 3, module 03)

Same method; the S judge of each lecture carries the pilot's notebook of all materials before it
(`notebook/15-02.08…` for 03.01 up to `21-03.06…` for 03.07), the exam judge E the notebook after 03.07.
«Before» is the pilot's run on the original banks (`pilot/student/raw/03.*/score.json`); `final/03.*` is the run on
the text of the PR as merged.

- `rounds/m03-v1/03.08-exam` — the exam's round 1 (39 items, PR branch commit `9d3396c`): the floor got 35/39 and the
  judges named the cross-cues (q04's ISO description → q25, q05's PDU gloss → q32, q28 → q09 and q37) and the
  duplicates (q14/q21/q18, q22/q24, q06/q39, q12/q38, q19/q34). Round 2 replaced the duplicates and the recall items
  with cases (q45–q52, 36 items) and was re-judged; the lectures did not change between the rounds.
- `rounds/m03-v2/` — round 2 of 03.01, 03.02, 03.04, 03.05, 03.06 and 03.08, the run kb reviewed (commit `ead4470`).
  After it the exam re-cased q43, q44, q46, q49, q50 (they mirrored self-check items), fixed q42-a3 and q52-a2's
  comment, and replaced q04's ISO premise with ITU-T's; 03.02 q09 and 03.04 q07 were retired (03.04 q08 swaps for
  q07), 03.04 q02 and q08 re-cased, 03.06 q11-a4 replaced and q13, q14 added, 03.01 says «рассылка»; 03.05's text
  changed one sentence (#378), so only its with-lecture judge was re-run. Those six materials were re-judged; 03.03
  and 03.07 did not change (03.07's objective did, which the judges do not see).
- `rounds/m03-v3/03.06-data-encapsulation` — round 3 of 03.06, the run kb reviewed (commit `a73f7df`). Three of its eight
  keys were «Сегмент», so q13 was re-keyed to the sequence numbers and q14 to the packet left after only the Ethernet
  header and trailer come off; 03.06 was re-judged.
