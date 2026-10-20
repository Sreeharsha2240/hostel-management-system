# Hostel Management System (HMS) — Part-1

Team 3 — Software Engineering Mini Project (PES University)

Part-1 documentation for Team 3. The documents include revision histories showing the contributions made during preparation.

## Team and roles

| Member | SRN | Team Role | Main Technical Responsibility |
|---|---|---|---|
| G.V.N. Sreeharsha | PES1UG24CS163 | Team Lead / Product Owner | C2 Authentication and Access Control, C8 Audit, integration, requirements |
| Chennamraju Vaishnavi | PES1UG24CS129 | QA / Test Lead | C3 Student, C4 Hostel/Room/Bed, test ownership |
| Devansh Gupta | PES1UG24CS145 | Architecture / Development Lead | C5 Allocation, C6 Payment, C7 Reports, architecture |

## Contents

- `SRS_Hostel_Management_System.docx` — Software Requirements Specification
- `SAD_Hostel_Management_System.docx` — Software Architecture and Design Specification
- `Test_Plan_Hostel_Management_System.docx` — Software Test Plan (33 test cases, RTM)
- `HMS_Part1_Work_Distribution.docx` — responsibility matrix for the three members
- `HMS_Part1_Sprint_Backlog.docx` — sprint goal, backlog, deliverables, definition of done
- `Design_README.md` — design deliverables overview
- `diagrams/` — UML diagrams (PNG) and editable Mermaid sources (`.mmd`)
- `pdf/` — PDF copies of all five documents

Cross-document IDs: REQ-1 to REQ-24, NFR-1 to NFR-12, SO-1 to SO-4, BR-1 to BR-6, C1 to C10, SD-1/SD-2, API-xx, TC-xxx.

## Code structure

Each module in SAD 3.4 is a separate Django app.

| Path | Component | Owner |
|---|---|---|
| `hms/` | Project settings and URL routing | — |
| `accounts/` | C2 Auth & Access Control | Sreeharsha |
| `students/` | C3 Student Module | Vaishnavi |
| `hostels/` | C4 Hostel, Room & Bed Module | Vaishnavi |
| `allocations/` | C5 Allocation Module | Devansh |
| `payments/` | C6 Payment & Receipt Module | Devansh |
| `reports/` | C7 Report Module | Devansh |
| `audit/` | C8 Audit & Logging | Sreeharsha |

The project uses a custom user model, `accounts.User` (`AUTH_USER_MODEL`). Refer to users with `settings.AUTH_USER_MODEL` in model fields and `get_user_model()` in code, never `django.contrib.auth.models.User`.

## Development setup

Requires Python 3.11+, Git and MySQL 8 (8.4 LTS recommended; MySQL 8.0, named in the SRS, reached end of life in April 2026). On Linux, `pip` compiles `mysqlclient`, so install its build packages first: `sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config`.

```powershell
git clone https://github.com/Sreeharsha2240/hostel-management-system.git
cd hostel-management-system
python -m venv .venv
# If PowerShell says running scripts is disabled, first run once:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env            # Linux/macOS: cp .env.example .env
```

Edit `.env`: replace `DJANGO_SECRET_KEY` with a generated key (the command is in the file) and set `DB_PASSWORD` to the password chosen in the database setup below. `.env` holds secrets and is ignored by Git; never commit it.

```powershell
python manage.py check --database default   # verifies the MySQL connection
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The site runs at http://127.0.0.1:8000/ and the Django admin at http://127.0.0.1:8000/admin/. Run the tests with `python manage.py test`.

### Authentication and role access (HMS-04)

- Sign in at `/login/` with a username and password. Admin, Warden and Student accounts receive separate dashboards. Signing out uses a POST request and clears the session.
- Admins manage accounts at `/manage/users/`: they can create accounts, assign roles and deactivate accounts. Warden and Student requests to account-management routes receive HTTP 403, including direct POST requests.
- Passwords are stored with Django's password hasher and must have at least eight characters, including a letter and a digit. Usernames are unique.
- Five consecutive failed logins lock the account for 15 minutes. The login form uses the same generic error for unknown usernames, incorrect passwords and locked accounts.
- Sessions expire after 15 minutes of inactivity. For HTTPS, set `DJANGO_SESSION_COOKIE_SECURE=True` as described below.
- Verify authentication behavior with `python manage.py test accounts.tests`. That suite includes a local test-client timing check requiring login and each role's dashboard to respond in under two seconds; production response times depend on the deployment environment.

### Database setup (MySQL)

1. Install MySQL Server 8 (Windows: `winget install Oracle.MySQL`, then run MySQL Configurator from the Start menu; Ubuntu: `sudo apt install mysql-server`) and make sure the server is running on port 3306.
2. Create the database and an application account. Open a MySQL prompt as root (Windows: **MySQL 8.4 Command Line Client** in the Start menu, which asks for the root password; Ubuntu: `sudo mysql`) and run the statements below, choosing your own password:

   ```sql
   CREATE DATABASE hms CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
   CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'choose-a-password';
   GRANT ALL PRIVILEGES ON hms.* TO 'hms_user'@'localhost';
   -- Django's test runner creates and drops a separate test_hms database.
   GRANT ALL PRIVILEGES ON test_hms.* TO 'hms_user'@'localhost';
   ```

   The application connects only as `hms_user`, which has no rights outside these two databases (SAD 3.9). Do not use the root account in `.env`.
3. Put the same password in `DB_PASSWORD` in `.env`. Change `DB_NAME`, `DB_HOST` or `DB_PORT` only if your setup differs from the defaults; if you rename the database, grant on `test_<new name>` instead of `test_hms`.
4. Run `python manage.py migrate` to create the tables. `python manage.py showmigrations` lists what has been applied.

**Working with migrations.** After changing a model, run `python manage.py makemigrations <app>` and commit the generated file in `<app>/migrations/` together with the model change. Never edit or delete a migration that is already on `main`; add a new one instead.
For an HTTPS deployment, set `DJANGO_SESSION_COOKIE_SECURE=True` in the environment; leave it `False` for the documented local HTTP development server.

## Team collaboration (HMS-03)

### Student records (HMS-06)

Admin and Warden users can register/search students at `/students/`, view each
student, update contact/course/year/guardian fields and deactivate records.
Student users cannot access these staff routes. Student IDs are canonical
uppercase, exactly 13 alphanumeric characters, unique and immutable. Duplicate
IDs produce `Student ID already registered`. Dates of birth accept DD-MM-YYYY
or ISO dates; displayed dates use DD-MM-YYYY. Mobile numbers require ten digits,
year is 1–5, and field lengths follow SRS Appendix B. Records are retained when
deactivated; permanent deletion is blocked.

`GET /students/?q=<id-or-partial-name>&hostel=<hostel-id>` supports search and
25-row pagination. `PATCH /students/<id>/` accepts partial updates to the allowed
fields; attempts to change Student ID return HTTP 422. Creation, updates and
deactivation are audited atomically. Django admin exposes records read-only.

The read adapter in `students/allocation_access.py` uses the SAD contract
`allocations.Allocation(student, bed, vacated_on)`. It filters by the student's
current hostel and refuses deactivation while an active allocation exists,
including the bed in the error. Before HMS-08 supplies that model there are no
allocation records, so hostel searches have no matches. HMS-08 must acquire the
Student row lock before allocation to serialize it with deactivation. Tests
exercise this read contract using a temporary MySQL table, not a Sprint 2
allocation implementation; integration must be repeated against the actual
Allocation model when it arrives.

`python manage.py test students --noinput` covers validation, authorization,
duplicate/immutable IDs, search, soft deletion, audit rollback and the allocation
read contract. It also checks paginated searches over 5,000 dummy student
records against the two-second target; this is not the 50-user load test.

### Hostels, rooms and beds (HMS-07)

After `python manage.py migrate`, Admin users can add and edit hostels at
`/hostels/`, create rooms from each hostel page and change bed status. Wardens
can read hostel/room lists and search `/beds/available/`; Students cannot access
these staff pages. Forms and JSON requests enforce the same permissions and
validation. JSON clients send `Content-Type: application/json` for writes and
`Accept: application/json` for reads, with a session and CSRF token.

Room capacity is 1–4. Saving a room creates the required A–D beds atomically;
repeated saves preserve existing bed IDs and statuses. Growing capacity adds
only missing beds. Shrinking removes only excess Available beds and refuses
beds that are occupied, under maintenance or protected by allocation history.
Renaming a room updates bed labels without replacing the bed records. Room
types follow the SRS Single/Double/Triple choices; capacity is configured
separately, including the SRS allowance of four beds. Room fees are nonnegative
INR amounts; allocation/payment behavior remains in Sprint 2.

`/beds/available/?hostel=<id>&floor=0&room_type=Triple` supports combined filters
and excludes Occupied and Maintenance beds. Lists use 25 records per page.
Hostel records in Django admin are read-only; use application forms for audited
changes. `python manage.py test hostels --noinput` tests validation, permissions,
automatic beds, capacity changes, rollback and filtering.

### Session security and audit logging (HMS-05)

Run `python manage.py migrate` after updating: the audit app adds its first table.
Admin users can read and filter events at `/audit/` (or request JSON using
`Accept: application/json`). Wardens and Students receive HTTP 403. The Django
admin also exposes a read-only audit list to Admin superusers.

Both `/login/` and Django's `/admin/login/` use the same five-attempt, 15-minute
lockout backend. Successful logins, failed attempts, logout and account changes
write audit events. Events store the acting user when authenticated, action,
affected record identifiers and timestamp; credentials, submitted usernames for
unknown accounts, session tokens and request bodies are not stored. An attempted
account is identified as the affected record for a failed login, not as an
authenticated actor. Data changes and their audit entries share a transaction.

Sessions use a rolling 15-minute expiry and HttpOnly cookies. Authenticated pages
send `Cache-Control: no-store`. The `.env.example` explicitly allows local HTTP.
For HTTPS deployment, set `DJANGO_DEBUG=False`,
`DJANGO_SESSION_COOKIE_SECURE=True`, `DJANGO_CSRF_COOKIE_SECURE=True` and
`DJANGO_SECURE_SSL_REDIRECT=True`, and configure TLS at the web server.

Audit events cannot be edited or deleted through the application or its normal
ORM operations. `python manage.py purge_audit_logs --dry-run` reports expired
entries; omit `--dry-run` to remove only entries older than 366 days. The command
rejects a shorter retention period. No cleanup is scheduled automatically.
Future allocation, release and payment services must call
`audit.services.record_event(...)` inside their transaction; those Sprint 2
operations are not implemented by HMS-05.

Run `python manage.py test audit accounts --noinput` for audit, session and
lockout regression tests on the configured MySQL server.

### Branches and commits

- Start from the latest `main` and create one branch per issue: `feature/HMS-<number>-short-description` for features or `fix/HMS-<number>-short-description` for fixes (for example, `feature/HMS-04-role-login`).
- Keep commits focused and use `HMS-<number>: imperative summary` (for example, `HMS-04: Add role-aware login`).
- Do not commit secrets, local databases, generated files, or unrelated changes.

### Pull requests and reviews

- Open a pull request into `main`, link the issue, and describe the change, acceptance criteria covered, and checks run (or why a check could not be run).
- Request at least one review from a teammate. The author must not approve their own pull request.
- Reviewers check the changed code, issue acceptance criteria, security implications, and relevant tests/checks. Request changes for defects; approve only after they are addressed.
- Merge only after the required review and checks pass. Use the repository's configured merge method and delete the feature branch after merging.

