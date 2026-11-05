# HMS-16 focused evidence

- **Source:** `8322b4c20c067d512c4bb439fdedd19d4fa27223` (`main`), fetched 5 November 2026.
- **Environment:** Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable MySQL 8.0.46 on loopback.
- **Data:** synthetic fixtures; the Django-created `test_hms` database was isolated and destroyed by the test runner.
- **Command:**
  `python manage.py test accounts.tests accounts.test_security audit.tests students.test_self_service students.tests.StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal --noinput -v 1`
- **Result:** 47 passed, 0 failures, 0 errors, 104.605 seconds.
- **Additional checks:** `manage.py check --deploy --database default` passed with secure cookies, HTTPS redirect and HSTS enabled; `manage.py migrate --check` and `makemigrations --check --dry-run` passed after migration.
- **Limits:** test-client HTTPS checks verify Django cookie/configuration behavior, not a real TLS connection. The full verification run on this Windows environment found one separate Cobertura helper failure; see `../System_Validation_Report.md`.

The full case-by-case disposition and test-method mapping is in the [System Validation Report](../../System_Validation_Report.md).