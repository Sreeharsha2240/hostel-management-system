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

Requires Python 3.11+ and Git.

```powershell
git clone https://github.com/Sreeharsha2240/hostel-management-system.git
cd hostel-management-system
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env            # Linux/macOS: cp .env.example .env
```

Edit `.env` and replace `DJANGO_SECRET_KEY` with a generated key (the command is in the file). `.env` holds secrets and is ignored by Git; never commit it.

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The site runs at http://127.0.0.1:8000/ and the Django admin at http://127.0.0.1:8000/admin/.

Until the MySQL configuration (HMS-02) is merged, the project uses Django's default local SQLite file.
