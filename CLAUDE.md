# Repository instructions

Read `AGENTS.md` and `README.md` for the current state and source layout. This repository contains the 2026 Japanese course materials for 実践・制約プログラミング.

- Do not commit, stage, or push without explicit maintainer permission.
- Preserve unrelated existing changes, including untracked files.
- The current review copies are `materials/sessions/<slug>/` and `workbook/sessions/<slug>/`. Review and edit those files directly.
- `design/curriculum-2026.md` records the current course: ten regular sessions followed by an individual project in sessions 11–15. Reflect new maintainer decisions there; do not restore old curriculum assumptions.
- Keep teacher answers, completed advanced-exercise solutions, hidden tests, rubrics, and quality records in the private `../cp-practice-design/teacher/` repository. Do not copy them into the public tree.
- Treat `materials/` as editable source and `workbook/` as learner-facing distribution. Learner-path reviews use these public materials without consulting teacher files.
- Register pages, URLs, and handouts in `site/nav.yaml`. Source links must resolve within this repository. Do not link public materials to private planning documents.
- Use 「第NN回」 and 「学習者」. Do not include learner information, lesson logs, names, hostnames, IP addresses, or environment-specific identifiers. Use repository-relative paths.
- Do not normally inspect generated or dependency directories such as `.site/`, `.pages/`, `__pycache__/`, and `vendor/`.
- Run checks relevant to the changes. Machine checks do not establish that human review or classroom trials are complete.
