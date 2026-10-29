# HMS submission checklist

This checklist covers the whole Team 3 submission: planning, design, implementation, verification and packaging. The local audit changes from 28–29 October are not on the remote branch yet. Check the course rubric for required slides, live demo, signatures and naming; those requirements cannot be inferred from the source repository.

## Planning and team records

- [x] Sprint schedule and estimated backlog are documented in `HMS_Part1_Sprint_Backlog.docx`.
- [x] Member responsibilities and test ownership are documented in `HMS_Part1_Work_Distribution.docx`.
- [x] Sprint implementation notes are available in `docs/SPRINT1_TESTING.md` and `docs/SPRINT2.md`.
- [x] Added a two-sprint burndown reconstruction: `docs/BURNDOWN.md`, `docs/burndown.svg` and `docs/BURNDOWN_DATA.csv`. It uses dated merged changes and backlog story points, not invented daily board data. Sprint 2 is in progress as of 29 October; issue #13 retains 5 points and 30 October actual is blank.
- [ ] Confirm the instructor accepts a merge-history reconstruction. If daily board history is required, export it and replace this chart with verified daily values.

## Requirements and design package

- [x] SRS, SAD and Test Plan are present as DOCX files.
- [x] Five PDF copies are present in `pdf/`; compare them to their DOCX sources after any later edits.
- [x] `Design_README.md` and four UML diagrams are present in rendered PNG and editable Mermaid formats.
- [x] The Test Plan contains 33 test cases and an RTM, as listed in README.

## Implementation and Git

- [x] Django source, migrations, dependency manifests, `.env.example`, setup guide and CI workflow are present.
- [x] Bed availability is paginated at 50 rows; a regression test covers page size, total count and page two.
- [ ] Commit the pagination fix and audit evidence, then push and confirm CI on that exact commit. The latest local test run is not remote CI.
- [ ] Confirm GitHub issue states and owners match the completed work. The Part 1 backlog is a planning artifact, not a current board export.
- [x] Added `.tmp/` to `.gitignore`; keep generated credentials, database dumps, JMeter results and downloaded tools out of the submission.

## Verification evidence

- [x] Latest local SQLite-compatible suite: 154 passed, 0 failures/errors; 163 discovered, with 9 MySQL-specific tests excluded. See `test-evidence/E2E_FINAL_TESTS.txt`.
- [x] Earlier CI run #29 passed MySQL 8.4 on Python 3.11 and 3.14; that run predates pagination.
- [x] Before pagination, a 50-user/10-minute-peak local JMeter run completed with no failed samples. The 2,000-bed listing averaged 12.2 seconds (p95 29.6 seconds, maximum 46.8 seconds), which prompted pagination.
- [ ] Repeat the JMeter smoke/full load after pagination. A post-change attempt was blocked by loopback socket access and is recorded as invalid, not a pass.
- [x] A populated local MySQL dump restore to a separate database had matching table counts; a manual timestamped backup ZIP passed integrity validation.
- [ ] If daily backup automation is required, arrange a permitted Task Scheduler job and capture a fresh backup/restore record; local scheduling was blocked by Windows task/CIM permissions.
- [ ] If security scanning/live deployment is required, run ZAP and verify TLS/Secure cookies against the actual demo host. Django production-profile settings validation alone is not live deployment evidence.
- [ ] Walk through Admin, Warden and Student accounts in a browser and save only rubric-requested screenshots. Browser automation was unavailable in the earlier audit; this is not a reproduced application defect.

## Final packaging

- [ ] Check Git status and include only source, required documents, diagrams and evidence. Exclude `.tmp/`, `.env`, local databases, passwords, backups and raw load files.
- [ ] Follow the README setup from a clean environment and verify demo accounts are fresh, synthetic and distributed only through the instructor-approved channel.
- [ ] Check DOCX/PDF pairs, filenames, team names/IDs, page rendering, links, signatures and rubric-specific cover fields.
- [ ] Confirm whether slides, a demo video or live URL are required. No slide deck is present in this repository.
