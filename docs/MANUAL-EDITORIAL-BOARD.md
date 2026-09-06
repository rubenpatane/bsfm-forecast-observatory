# Manual editorial board

Status: public editorial surface, non-scoring

The featured board rendered on the overview and forecast pages is maintained in
`site/data/editorial-board.json`. It is intentionally outside AGGIORNA's
scientific outcome and forecast generation paths.

## Update rule

An editor may update the board when a relevant reported occurrence needs a
plain-language comparison with a frozen forecast. Every revision must:

1. retain the frozen forecast values exactly;
2. show similarities and mismatches with equal prominence;
3. distinguish discovery/reporting sources from competent-authority evidence;
4. keep unresolved target membership `PENDING_OFFICIAL_ADJUDICATION`;
5. keep `scientific_effect` equal to `NONE` until a separate canonical outcome
   artifact is admitted under the governing protocol;
6. never describe a case outside the frozen horizon as a scored hit;
7. update `updated_on` and rely on public Git history to preserve prior wording.

The board may explain a descriptive near miss. It cannot alter F-002, PD14, an
outcome ledger, a score, a validation gate or a model parameter.
