# HMS-16 focused evidence

- **Source:** `8322b4c20c067d512c4bb439fdedd19d4fa27223` (`main`), fetched 5 November 2026.
- **Environment:** Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable MySQL 8.0.46 on loopback.
- **Data:** synthetic fixtures; the Django-created `test_hms` database was isolated and destroyed by the test runner.
- **Command:**
  `python manage.py test accounts.tests accounts.test_security audit.tests students.test_self_service students.tests.StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal --noinput -v 1`
- **Historical owner-reported result:** 47 passed, 0 failures, 0 errors, 104.605 seconds; raw focused JUnit/stdout is not committed.
- **Historical owner-reported additional checks:** `manage.py check --deploy --database default` passed with secure cookies, HTTPS redirect and HSTS enabled; `manage.py migrate --check` and `makemigrations --check --dry-run` passed after migration. Effective deployment-check configuration is not committed.
- **Limits:** test-client HTTPS checks verify Django cookie/configuration behavior, not a real TLS connection. The full verification run on this Windows environment found one separate Cobertura helper failure; see the [System Validation Report](../../System_Validation_Report.md).

The full case-by-case disposition and test-method mapping is in the [System Validation Report](../../System_Validation_Report.md).

## Independent technical review — 8 November 2026

The [System Validation Report](../../System_Validation_Report.md) now distinguishes retained owner observations from accepted original-case outcomes, lists the original security subconditions missing from the focused evidence, separates TC-SEC-06 PARTIAL from TC-SEC-08 NOT RUN, and supplies consolidated case/RTM/defect metrics. The [sanitized extraction](independent-review-20261108.json) records the reviewed main revision, unchanged case/source hashes, exact-main JUnit and `run.json` input hashes and actual issue ages. It is a review of existing evidence, not a fresh 47-method execution, TLS/ZAP run, human signature, approved deviation or final submission.
