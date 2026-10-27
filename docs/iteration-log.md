# TaskFlow — Iteration Journal

## Iteration 1: Initial Implementation

**Goal:** Deliver a working task management application.

**Work performed:**

- Implemented the Flask API for task management.
- Integrated the MySQL database.
- Developed the frontend using HTML, CSS, and JavaScript.
- Implemented task creation, listing, updating, filtering, and deletion.
- Created eight automated API tests using pytest.
- Configured GitHub Actions to run the automated tests.

**Observed evidence:**

- The application was tested locally through the browser.
- The automated test suite passed all eight tests.
- The GitHub Actions workflow completed successfully, as observed by the team.
- Git commits recorded the implementation and CI configuration.

**Limitations:**

- The initial implementation was developed under a short deadline.
- No controlled comparison against a conventional development process was performed.
- No measured comparison of defect rates, feedback time, or developer confidence is available.
- TDD and pair programming have not been established as completed practices by the evidence currently recorded.

## Iteration 2: Technical Quality Improvement

**Goal:** Strengthen feedback, maintainability, and confidence when modifying the application.

**Activities planned:**

- Review the existing test suite and identify missing test cases.
- Conduct a pair-programming session with driver and navigator roles, if possible.
- Identify and refactor one real section of code without intentionally changing its behavior.
- Run the automated test suite after any code changes.
- Verify the GitHub Actions workflow.
- Record any defects, feedback time, and technical debt identified.

**Results:**
Iteration 2 activities and results must be completed after the planned work has been performed. The team will record the changes made, the tests executed, and the evidence collected.

**Limitations:**

- The effects of the planned activities have not yet been measured.
- No improvement in development speed or defect reduction will be claimed without supporting evidence.

## Retrospective

**What went well?**

- The team developed a working task management application with a frontend, backend, and MySQL database.
- Eight automated API tests were implemented.
- A GitHub Actions workflow was configured to execute the tests automatically.
- A technical Definition of Done was created to clarify quality expectations.

**What was difficult?**

- The short deadline limited the time available for experimentation and evaluation.
- The current test suite does not cover every possible application behavior.
- The project does not yet provide a controlled comparison of conventional development and XP practices.

**What did we learn?**

- Automated tests provide repeatable feedback about the behaviors they cover.
- Continuous integration helps verify changes consistently.
- Passing tests do not guarantee that the entire application is free of defects.
- Technical quality practices need to be applied and documented, not merely described in theory.

**One improvement for the next iteration:**
Review test coverage, add relevant tests, and perform a documented refactoring while checking that the existing tests continue to pass.

**Action items:**

- **Action:** Review and improve the technical Definition of Done.
- **Responsible member:** Majd mohamed
- **Evidence:** Updated Definition of Done document.

- **Action:** Review and improve automated test coverage.
- **Responsible member:** lassade mrabet
- **Evidence:** Updated tests and recorded test results.

- **Action:** Conduct and document a pair-programming session.
- **Responsible members:** Mohamed aziz cherif Oussama Rhim
- **Evidence:** Session notes, roles, task performed, and observations.

## Final Note

This journal distinguishes completed work from planned activities. Any additional XP practice or experiment will be recorded as completed only when the team has performed it and collected supporting evidence.
