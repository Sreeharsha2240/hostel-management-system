# Derived recorded-evidence tables

These tables describe the supplied archived runs. Function-body acceptance applies to statements only; branches remain a separate full-application diagnostic. Partial missing outcomes are included in missing outcomes. Negative destinations are code-object exits.

## baseline_isolated_methods

| Module | Full statements | Full rate | Body statements | Body rate | Branch outcomes | Branch rate | Partial missing outcomes |
|---|---|---|---|---|---|---|---|
| accounts | 218/369 | 59.08% | 218 / 218 | 100.00% | 96/100 | 96.00% | 4 |
| allocations | 202/313 | 64.54% | 202 / 205 | 98.54% | 92/98 | 93.88% | 6 |
| audit | 69/158 | 43.67% | 69 / 69 | 100.00% | 26/26 | 100.00% | 0 |
| hms | 55/87 | 63.22% | 55 / 55 | 100.00% | 26/26 | 100.00% | 0 |
| hostels | 143/273 | 52.38% | 143 / 143 | 100.00% | 70/74 | 94.59% | 4 |
| payments | 131/256 | 51.17% | 131 / 131 | 100.00% | 52/54 | 96.30% | 2 |
| reports | 54/86 | 62.79% | 54 / 54 | 100.00% | 19/20 | 95.00% | 1 |
| scripts | 0/95 | 0.00% | 0 / 73 | 0.00% | 0/14 | 0.00% | 0 |
| students | 80/171 | 46.78% | 80 / 80 | 100.00% | 33/34 | 97.06% | 1 |
| Configured total | 952/1808 | 52.65% | 952 / 1028 | 92.61% | 414/446 | 92.83% | 18 |
| Application subtotal | 952/1713 | 55.58% | 952 / 955 | 99.69% | 414/432 | 95.83% | 18 |

| File | Full statements | Full rate | Missing full lines | Body statements | Missing body lines | Branch outcomes | Branch rate | Partial | Missing arcs |
|---|---|---|---|---|---|---|---|---|---|
| accounts/admin.py | 6/23 | 26.09% | 1-3, 5, 7, 10-12, 15-16, 18-19, 22, 25, 28, 31, 34 | 6/6 | none | 0/0 | N/A | 0 | none |
| accounts/backends.py | 27/36 | 75.00% | 3, 5-8, 11-13, 15 | 27/27 | none | 12/12 | 100.00% | 0 | none |
| accounts/decorators.py | 15/22 | 68.18% | 1, 3-4, 6-8, 11 | 15/15 | none | 8/8 | 100.00% | 0 | none |
| accounts/forms.py | 17/38 | 44.74% | 1-3, 5, 8-9, 11-13, 15, 25, 33-36, 38, 45-49 | 17/17 | none | 6/6 | 100.00% | 0 | none |
| accounts/management/commands/create_demo_accounts.py | 32/43 | 74.42% | 3, 5-9, 11, 14-15, 17, 23 | 32/32 | none | 10/10 | 100.00% | 0 | none |
| accounts/management/commands/create_demo_data.py | 38/55 | 69.09% | 3, 5-8, 10-16, 19-20, 22, 31-32 | 38/38 | none | 22/22 | 100.00% | 0 | none |
| accounts/middleware.py | 6/10 | 60.00% | 1, 4, 7, 10 | 6/6 | none | 2/2 | 100.00% | 0 | none |
| accounts/models.py | 6/20 | 30.00% | 1-3, 6, 13-16, 18-21, 23, 26 | 6/6 | none | 3/4 | 75.00% | 1 | 29 -> 31 |
| accounts/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| accounts/validators.py | 3/8 | 37.50% | 1-2, 5, 8, 17 | 3/3 | none | 2/2 | 100.00% | 0 | none |
| accounts/views.py | 68/111 | 61.26% | 1-9, 11-13, 15-17, 20-22, 38-40, 45-46, 66-69, 106, 109-113, 130-134, 152-156 | 68/68 | none | 31/34 | 91.18% | 3 | 73 -> 96; 77 -> 96; 87 -> 96 |
| allocations/admin.py | 3/12 | 25.00% | 1, 3, 6-9, 19, 22, 25 | 3/3 | none | 0/0 | N/A | 0 | none |
| allocations/forms.py | 0/13 | 0.00% | 1-2, 4-6, 9-12, 19-20, 23-24 | 0/0 | none | 0/0 | N/A | 0 | none |
| allocations/models.py | 69/101 | 68.32% | 1, 3-6, 9-10, 13, 16, 20-24, 26, 29, 32-34, 37, 40, 43, 45-47, 80, 106-107, 127, 205, 226, 229 | 69/71 | 127, 205 | 41/44 | 93.18% | 3 | 126 -> 127; 204 -> 205; 220 -> 223 |
| allocations/services.py | 32/47 | 68.09% | 1-3, 5-8, 10, 13-14, 23, 40-41, 50-51 | 32/32 | none | 6/6 | 100.00% | 0 | none |
| allocations/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| allocations/views.py | 98/137 | 71.53% | 1-9, 11-15, 17-19, 22, 37, 47, 52, 72-74, 102-104, 148-150, 192-194, 232-234, 251-253 | 98/99 | 52 | 45/48 | 93.75% | 3 | 51 -> 52; 79 -> 86; 199 -> 220 |
| audit/admin.py | 5/17 | 29.41% | 1, 3, 6-10, 12, 15, 18, 21, 24 | 5/5 | none | 0/0 | N/A | 0 | none |
| audit/management/commands/purge_audit_logs.py | 11/19 | 57.89% | 1, 3-4, 6, 9-10, 12, 16 | 11/11 | none | 4/4 | 100.00% | 0 | none |
| audit/mixins.py | 16/23 | 69.57% | 1-2, 5, 8, 23, 28, 32 | 16/16 | none | 4/4 | 100.00% | 0 | none |
| audit/models.py | 15/50 | 30.00% | 1, 3-6, 9-10, 30, 33, 36, 39, 46-58, 60, 67-70, 72, 74-75, 77, 88, 91 | 15/15 | none | 6/6 | 100.00% | 0 | none |
| audit/services.py | 6/8 | 75.00% | 1, 4 | 6/6 | none | 4/4 | 100.00% | 0 | none |
| audit/signals.py | 8/19 | 42.11% | 1-2, 7, 9-10, 13-14, 18-19, 32-33 | 8/8 | none | 4/4 | 100.00% | 0 | none |
| audit/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| audit/views.py | 8/19 | 42.11% | 1-4, 6-8, 10, 13-15 | 8/8 | none | 4/4 | 100.00% | 0 | none |
| hms/decorators.py | 9/15 | 60.00% | 1, 3, 5-6, 8, 11 | 9/9 | none | 2/2 | 100.00% | 0 | none |
| hms/forms.py | 6/13 | 46.15% | 3, 5-6, 9, 12, 18, 21 | 6/6 | none | 4/4 | 100.00% | 0 | none |
| hms/http.py | 24/32 | 75.00% | 3-4, 6-7, 10, 17, 24, 47 | 24/24 | none | 14/14 | 100.00% | 0 | none |
| hms/responses.py | 12/15 | 80.00% | 1, 4, 20 | 12/12 | none | 6/6 | 100.00% | 0 | none |
| hms/security_headers.py | 4/8 | 50.00% | 4, 7, 19, 22 | 4/4 | none | 0/0 | N/A | 0 | none |
| hms/urls.py | 0/4 | 0.00% | 1-3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| hostels/admin.py | 8/42 | 19.05% | 1, 3-5, 7, 10-13, 16-20, 23, 35-40, 42, 46-51, 53, 57-61 | 8/8 | none | 2/2 | 100.00% | 0 | none |
| hostels/forms.py | 13/29 | 44.83% | 1, 3, 6-7, 9, 12-15, 18-21, 30, 34, 38 | 13/13 | none | 4/4 | 100.00% | 0 | none |
| hostels/models.py | 59/110 | 53.64% | 1, 3-5, 8-11, 13-17, 19-20, 22, 26-27, 29, 37, 46-47, 49-52, 54, 59-62, 65, 73-75, 85, 113-114, 195, 199-203, 205, 210-211, 217-219, 226 | 59/59 | none | 42/42 | 100.00% | 0 | none |
| hostels/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| hostels/views.py | 63/89 | 70.79% | 1-6, 8-10, 12-13, 16, 20-22, 49-51, 86-88, 114-116, 143-144 | 63/63 | none | 22/26 | 84.62% | 4 | 157 -> 159; 159 -> 161; 161 -> 163; 163 -> 168 |
| payments/admin.py | 3/14 | 21.43% | 1, 3, 6-11, 13, 16, 19 | 3/3 | none | 0/0 | N/A | 0 | none |
| payments/forms.py | 2/18 | 11.11% | 1, 3-4, 6-7, 9, 12-14, 17, 20-21, 26-27, 33, 37 | 2/2 | none | 0/0 | N/A | 0 | none |
| payments/models.py | 41/80 | 51.25% | 3-4, 6-10, 12, 15-17, 19-20, 28-29, 35, 38-42, 44, 47-51, 56, 63-65, 67-69, 87, 90, 111-112, 162 | 41/41 | none | 21/22 | 95.45% | 1 | 94 -> 96 |
| payments/receipts.py | 14/21 | 66.67% | 1-2, 4-7, 10 | 14/14 | none | 2/2 | 100.00% | 0 | none |
| payments/services.py | 16/29 | 55.17% | 1, 3-5, 7-10, 12, 15-16, 23, 60 | 16/16 | none | 4/4 | 100.00% | 0 | none |
| payments/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| payments/views.py | 55/91 | 60.44% | 1-7, 9-12, 14-17, 20, 35-37, 64, 102-104, 108-110, 119, 126-128, 139-141, 151-153 | 55/55 | none | 25/26 | 96.15% | 1 | 42 -> 48 |
| reports/admin.py | 0/0 | N/A | none | 0/0 | none | 0/0 | N/A | 0 | none |
| reports/models.py | 0/0 | N/A | none | 0/0 | none | 0/0 | N/A | 0 | none |
| reports/services.py | 19/26 | 73.08% | 1, 3, 5-7, 10, 56 | 19/19 | none | 5/6 | 83.33% | 1 | 58 -> 60 |
| reports/urls.py | 0/4 | 0.00% | 1-2, 4, 6 | 0/0 | none | 0/0 | N/A | 0 | none |
| reports/views.py | 35/56 | 62.50% | 1, 3-7, 9-12, 14, 16, 24, 37, 47, 102-104, 108-110 | 35/35 | none | 14/14 | 100.00% | 0 | none |
| scripts/run_checks.py | 0/95 | 0.00% | 9-19, 21-22, 34-36, 39-41, 44, 46-48, 50-51, 53-56, 58, 61, 63, 117-121, 131-135, 143-144, 148, 152, 155, 157, 159-162, 164, 167-168, 173-177, 180-185, 188-190, 193-194, 196-197, 205-207, 215-222, 225, 227-228, 233-235, 242, 245-246, 249-250 | 0/73 | 35-36, 39-41, 46-48, 50-51, 53-56, 58, 63, 118-121, 131-135, 144, 148, 152, 157, 159-162, 164, 167-168, 174-177, 180-185, 188-190, 193-194, 196-197, 205-207, 215-222, 225, 227-228, 233-235, 242, 245-246 | 0/14 | 0.00% | 0 | 131 -> 132; 131 -> 134; 162 -> 164; 162 -> 167; 181 -> 182; 181 -> 184; 189 -> 190; 189 -> 193; 217 -> 218; 217 -> 221; 218 -> 219; 218 -> 220; 249 -> exit@1; 249 -> 250 |
| students/admin.py | 0/9 | 0.00% | 1, 3, 5, 8-13 | 0/0 | none | 0/0 | N/A | 0 | none |
| students/forms.py | 16/27 | 59.26% | 1-2, 4, 6, 9-10, 26-28, 43, 48 | 16/16 | none | 6/6 | 100.00% | 0 | none |
| students/models.py | 11/46 | 23.91% | 1-4, 7-8, 16-19, 21-23, 25, 35-39, 42, 46-48, 54-55, 63, 68-70, 72-74, 79, 82-83 | 11/11 | none | 8/8 | 100.00% | 0 | none |
| students/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| students/views.py | 53/86 | 61.63% | 1-8, 10-16, 18-19, 22, 29-30, 57-59, 86-88, 125-128, 176-178 | 53/53 | none | 19/20 | 95.00% | 1 | 37 -> 47 |

## expanded_isolated_methods

| Module | Full statements | Full rate | Body statements | Body rate | Branch outcomes | Branch rate | Partial missing outcomes |
|---|---|---|---|---|---|---|---|
| accounts | 218/369 | 59.08% | 218 / 218 | 100.00% | 96/100 | 96.00% | 4 |
| allocations | 205/313 | 65.50% | 205 / 205 | 100.00% | 95/98 | 96.94% | 3 |
| audit | 69/158 | 43.67% | 69 / 69 | 100.00% | 26/26 | 100.00% | 0 |
| hms | 55/87 | 63.22% | 55 / 55 | 100.00% | 26/26 | 100.00% | 0 |
| hostels | 143/273 | 52.38% | 143 / 143 | 100.00% | 70/74 | 94.59% | 4 |
| payments | 131/256 | 51.17% | 131 / 131 | 100.00% | 52/54 | 96.30% | 2 |
| reports | 54/86 | 62.79% | 54 / 54 | 100.00% | 19/20 | 95.00% | 1 |
| scripts | 0/95 | 0.00% | 0 / 73 | 0.00% | 0/14 | 0.00% | 0 |
| students | 80/171 | 46.78% | 80 / 80 | 100.00% | 33/34 | 97.06% | 1 |
| Configured total | 955/1808 | 52.82% | 955 / 1028 | 92.90% | 417/446 | 93.50% | 15 |
| Application subtotal | 955/1713 | 55.75% | 955 / 955 | 100.00% | 417/432 | 96.53% | 15 |

| File | Full statements | Full rate | Missing full lines | Body statements | Missing body lines | Branch outcomes | Branch rate | Partial | Missing arcs |
|---|---|---|---|---|---|---|---|---|---|
| accounts/admin.py | 6/23 | 26.09% | 1-3, 5, 7, 10-12, 15-16, 18-19, 22, 25, 28, 31, 34 | 6/6 | none | 0/0 | N/A | 0 | none |
| accounts/backends.py | 27/36 | 75.00% | 3, 5-8, 11-13, 15 | 27/27 | none | 12/12 | 100.00% | 0 | none |
| accounts/decorators.py | 15/22 | 68.18% | 1, 3-4, 6-8, 11 | 15/15 | none | 8/8 | 100.00% | 0 | none |
| accounts/forms.py | 17/38 | 44.74% | 1-3, 5, 8-9, 11-13, 15, 25, 33-36, 38, 45-49 | 17/17 | none | 6/6 | 100.00% | 0 | none |
| accounts/management/commands/create_demo_accounts.py | 32/43 | 74.42% | 3, 5-9, 11, 14-15, 17, 23 | 32/32 | none | 10/10 | 100.00% | 0 | none |
| accounts/management/commands/create_demo_data.py | 38/55 | 69.09% | 3, 5-8, 10-16, 19-20, 22, 31-32 | 38/38 | none | 22/22 | 100.00% | 0 | none |
| accounts/middleware.py | 6/10 | 60.00% | 1, 4, 7, 10 | 6/6 | none | 2/2 | 100.00% | 0 | none |
| accounts/models.py | 6/20 | 30.00% | 1-3, 6, 13-16, 18-21, 23, 26 | 6/6 | none | 3/4 | 75.00% | 1 | 29 -> 31 |
| accounts/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| accounts/validators.py | 3/8 | 37.50% | 1-2, 5, 8, 17 | 3/3 | none | 2/2 | 100.00% | 0 | none |
| accounts/views.py | 68/111 | 61.26% | 1-9, 11-13, 15-17, 20-22, 38-40, 45-46, 66-69, 106, 109-113, 130-134, 152-156 | 68/68 | none | 31/34 | 91.18% | 3 | 73 -> 96; 77 -> 96; 87 -> 96 |
| allocations/admin.py | 3/12 | 25.00% | 1, 3, 6-9, 19, 22, 25 | 3/3 | none | 0/0 | N/A | 0 | none |
| allocations/forms.py | 0/13 | 0.00% | 1-2, 4-6, 9-12, 19-20, 23-24 | 0/0 | none | 0/0 | N/A | 0 | none |
| allocations/models.py | 71/101 | 70.30% | 1, 3-6, 9-10, 13, 16, 20-24, 26, 29, 32-34, 37, 40, 43, 45-47, 80, 106-107, 226, 229 | 71/71 | none | 43/44 | 97.73% | 1 | 220 -> 223 |
| allocations/services.py | 32/47 | 68.09% | 1-3, 5-8, 10, 13-14, 23, 40-41, 50-51 | 32/32 | none | 6/6 | 100.00% | 0 | none |
| allocations/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| allocations/views.py | 99/137 | 72.26% | 1-9, 11-15, 17-19, 22, 37, 47, 72-74, 102-104, 148-150, 192-194, 232-234, 251-253 | 99/99 | none | 46/48 | 95.83% | 2 | 79 -> 86; 199 -> 220 |
| audit/admin.py | 5/17 | 29.41% | 1, 3, 6-10, 12, 15, 18, 21, 24 | 5/5 | none | 0/0 | N/A | 0 | none |
| audit/management/commands/purge_audit_logs.py | 11/19 | 57.89% | 1, 3-4, 6, 9-10, 12, 16 | 11/11 | none | 4/4 | 100.00% | 0 | none |
| audit/mixins.py | 16/23 | 69.57% | 1-2, 5, 8, 23, 28, 32 | 16/16 | none | 4/4 | 100.00% | 0 | none |
| audit/models.py | 15/50 | 30.00% | 1, 3-6, 9-10, 30, 33, 36, 39, 46-58, 60, 67-70, 72, 74-75, 77, 88, 91 | 15/15 | none | 6/6 | 100.00% | 0 | none |
| audit/services.py | 6/8 | 75.00% | 1, 4 | 6/6 | none | 4/4 | 100.00% | 0 | none |
| audit/signals.py | 8/19 | 42.11% | 1-2, 7, 9-10, 13-14, 18-19, 32-33 | 8/8 | none | 4/4 | 100.00% | 0 | none |
| audit/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| audit/views.py | 8/19 | 42.11% | 1-4, 6-8, 10, 13-15 | 8/8 | none | 4/4 | 100.00% | 0 | none |
| hms/decorators.py | 9/15 | 60.00% | 1, 3, 5-6, 8, 11 | 9/9 | none | 2/2 | 100.00% | 0 | none |
| hms/forms.py | 6/13 | 46.15% | 3, 5-6, 9, 12, 18, 21 | 6/6 | none | 4/4 | 100.00% | 0 | none |
| hms/http.py | 24/32 | 75.00% | 3-4, 6-7, 10, 17, 24, 47 | 24/24 | none | 14/14 | 100.00% | 0 | none |
| hms/responses.py | 12/15 | 80.00% | 1, 4, 20 | 12/12 | none | 6/6 | 100.00% | 0 | none |
| hms/security_headers.py | 4/8 | 50.00% | 4, 7, 19, 22 | 4/4 | none | 0/0 | N/A | 0 | none |
| hms/urls.py | 0/4 | 0.00% | 1-3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| hostels/admin.py | 8/42 | 19.05% | 1, 3-5, 7, 10-13, 16-20, 23, 35-40, 42, 46-51, 53, 57-61 | 8/8 | none | 2/2 | 100.00% | 0 | none |
| hostels/forms.py | 13/29 | 44.83% | 1, 3, 6-7, 9, 12-15, 18-21, 30, 34, 38 | 13/13 | none | 4/4 | 100.00% | 0 | none |
| hostels/models.py | 59/110 | 53.64% | 1, 3-5, 8-11, 13-17, 19-20, 22, 26-27, 29, 37, 46-47, 49-52, 54, 59-62, 65, 73-75, 85, 113-114, 195, 199-203, 205, 210-211, 217-219, 226 | 59/59 | none | 42/42 | 100.00% | 0 | none |
| hostels/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| hostels/views.py | 63/89 | 70.79% | 1-6, 8-10, 12-13, 16, 20-22, 49-51, 86-88, 114-116, 143-144 | 63/63 | none | 22/26 | 84.62% | 4 | 157 -> 159; 159 -> 161; 161 -> 163; 163 -> 168 |
| payments/admin.py | 3/14 | 21.43% | 1, 3, 6-11, 13, 16, 19 | 3/3 | none | 0/0 | N/A | 0 | none |
| payments/forms.py | 2/18 | 11.11% | 1, 3-4, 6-7, 9, 12-14, 17, 20-21, 26-27, 33, 37 | 2/2 | none | 0/0 | N/A | 0 | none |
| payments/models.py | 41/80 | 51.25% | 3-4, 6-10, 12, 15-17, 19-20, 28-29, 35, 38-42, 44, 47-51, 56, 63-65, 67-69, 87, 90, 111-112, 162 | 41/41 | none | 21/22 | 95.45% | 1 | 94 -> 96 |
| payments/receipts.py | 14/21 | 66.67% | 1-2, 4-7, 10 | 14/14 | none | 2/2 | 100.00% | 0 | none |
| payments/services.py | 16/29 | 55.17% | 1, 3-5, 7-10, 12, 15-16, 23, 60 | 16/16 | none | 4/4 | 100.00% | 0 | none |
| payments/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| payments/views.py | 55/91 | 60.44% | 1-7, 9-12, 14-17, 20, 35-37, 64, 102-104, 108-110, 119, 126-128, 139-141, 151-153 | 55/55 | none | 25/26 | 96.15% | 1 | 42 -> 48 |
| reports/admin.py | 0/0 | N/A | none | 0/0 | none | 0/0 | N/A | 0 | none |
| reports/models.py | 0/0 | N/A | none | 0/0 | none | 0/0 | N/A | 0 | none |
| reports/services.py | 19/26 | 73.08% | 1, 3, 5-7, 10, 56 | 19/19 | none | 5/6 | 83.33% | 1 | 58 -> 60 |
| reports/urls.py | 0/4 | 0.00% | 1-2, 4, 6 | 0/0 | none | 0/0 | N/A | 0 | none |
| reports/views.py | 35/56 | 62.50% | 1, 3-7, 9-12, 14, 16, 24, 37, 47, 102-104, 108-110 | 35/35 | none | 14/14 | 100.00% | 0 | none |
| scripts/run_checks.py | 0/95 | 0.00% | 9-19, 21-22, 34-36, 39-41, 44, 46-48, 50-51, 53-56, 58, 61, 63, 117-121, 131-135, 143-144, 148, 152, 155, 157, 159-162, 164, 167-168, 173-177, 180-185, 188-190, 193-194, 196-197, 205-207, 215-222, 225, 227-228, 233-235, 242, 245-246, 249-250 | 0/73 | 35-36, 39-41, 46-48, 50-51, 53-56, 58, 63, 118-121, 131-135, 144, 148, 152, 157, 159-162, 164, 167-168, 174-177, 180-185, 188-190, 193-194, 196-197, 205-207, 215-222, 225, 227-228, 233-235, 242, 245-246 | 0/14 | 0.00% | 0 | 131 -> 132; 131 -> 134; 162 -> 164; 162 -> 167; 181 -> 182; 181 -> 184; 189 -> 190; 189 -> 193; 217 -> 218; 217 -> 221; 218 -> 219; 218 -> 220; 249 -> exit@1; 249 -> 250 |
| students/admin.py | 0/9 | 0.00% | 1, 3, 5, 8-13 | 0/0 | none | 0/0 | N/A | 0 | none |
| students/forms.py | 16/27 | 59.26% | 1-2, 4, 6, 9-10, 26-28, 43, 48 | 16/16 | none | 6/6 | 100.00% | 0 | none |
| students/models.py | 11/46 | 23.91% | 1-4, 7-8, 16-19, 21-23, 25, 35-39, 42, 46-48, 54-55, 63, 68-70, 72-74, 79, 82-83 | 11/11 | none | 8/8 | 100.00% | 0 | none |
| students/urls.py | 0/3 | 0.00% | 1, 3, 5 | 0/0 | none | 0/0 | N/A | 0 | none |
| students/views.py | 53/86 | 61.63% | 1-8, 10-16, 18-19, 22, 29-30, 57-59, 86-88, 125-128, 176-178 | 53/53 | none | 19/20 | 95.00% | 1 | 37 -> 47 |

## full_mixed_suite

| Module | Full statements | Full rate | Body statements | Body rate | Branch outcomes | Branch rate | Partial missing outcomes |
|---|---|---|---|---|---|---|---|
| accounts | 369/369 | 100.00% | N/A | N/A | 98/100 | 98.00% | 2 |
| allocations | 313/313 | 100.00% | N/A | N/A | 98/98 | 100.00% | 0 |
| audit | 158/158 | 100.00% | N/A | N/A | 26/26 | 100.00% | 0 |
| hms | 87/87 | 100.00% | N/A | N/A | 26/26 | 100.00% | 0 |
| hostels | 273/273 | 100.00% | N/A | N/A | 74/74 | 100.00% | 0 |
| payments | 256/256 | 100.00% | N/A | N/A | 53/54 | 98.15% | 1 |
| reports | 86/86 | 100.00% | N/A | N/A | 20/20 | 100.00% | 0 |
| scripts | 79/95 | 83.16% | N/A | N/A | 12/14 | 85.71% | 2 |
| students | 171/171 | 100.00% | N/A | N/A | 34/34 | 100.00% | 0 |
| Configured total | 1792/1808 | 99.12% | N/A | N/A | 441/446 | 98.88% | 5 |
| Application subtotal | 1713/1713 | 100.00% | N/A | N/A | 429/432 | 99.31% | 3 |

| File | Full statements | Full rate | Missing full lines | Body statements | Missing body lines | Branch outcomes | Branch rate | Partial | Missing arcs |
|---|---|---|---|---|---|---|---|---|---|
| accounts/admin.py | 23/23 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| accounts/backends.py | 36/36 | 100.00% | none | N/A | N/A | 12/12 | 100.00% | 0 | none |
| accounts/decorators.py | 22/22 | 100.00% | none | N/A | N/A | 8/8 | 100.00% | 0 | none |
| accounts/forms.py | 38/38 | 100.00% | none | N/A | N/A | 6/6 | 100.00% | 0 | none |
| accounts/management/commands/create_demo_accounts.py | 43/43 | 100.00% | none | N/A | N/A | 10/10 | 100.00% | 0 | none |
| accounts/management/commands/create_demo_data.py | 55/55 | 100.00% | none | N/A | N/A | 22/22 | 100.00% | 0 | none |
| accounts/middleware.py | 10/10 | 100.00% | none | N/A | N/A | 2/2 | 100.00% | 0 | none |
| accounts/models.py | 20/20 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| accounts/urls.py | 3/3 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| accounts/validators.py | 8/8 | 100.00% | none | N/A | N/A | 2/2 | 100.00% | 0 | none |
| accounts/views.py | 111/111 | 100.00% | none | N/A | N/A | 32/34 | 94.12% | 2 | 77 -> 96; 87 -> 96 |
| allocations/admin.py | 12/12 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| allocations/forms.py | 13/13 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| allocations/models.py | 101/101 | 100.00% | none | N/A | N/A | 44/44 | 100.00% | 0 | none |
| allocations/services.py | 47/47 | 100.00% | none | N/A | N/A | 6/6 | 100.00% | 0 | none |
| allocations/urls.py | 3/3 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| allocations/views.py | 137/137 | 100.00% | none | N/A | N/A | 48/48 | 100.00% | 0 | none |
| audit/admin.py | 17/17 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| audit/management/commands/purge_audit_logs.py | 19/19 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| audit/mixins.py | 23/23 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| audit/models.py | 50/50 | 100.00% | none | N/A | N/A | 6/6 | 100.00% | 0 | none |
| audit/services.py | 8/8 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| audit/signals.py | 19/19 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| audit/urls.py | 3/3 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| audit/views.py | 19/19 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| hms/decorators.py | 15/15 | 100.00% | none | N/A | N/A | 2/2 | 100.00% | 0 | none |
| hms/forms.py | 13/13 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| hms/http.py | 32/32 | 100.00% | none | N/A | N/A | 14/14 | 100.00% | 0 | none |
| hms/responses.py | 15/15 | 100.00% | none | N/A | N/A | 6/6 | 100.00% | 0 | none |
| hms/security_headers.py | 8/8 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| hms/urls.py | 4/4 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| hostels/admin.py | 42/42 | 100.00% | none | N/A | N/A | 2/2 | 100.00% | 0 | none |
| hostels/forms.py | 29/29 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| hostels/models.py | 110/110 | 100.00% | none | N/A | N/A | 42/42 | 100.00% | 0 | none |
| hostels/urls.py | 3/3 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| hostels/views.py | 89/89 | 100.00% | none | N/A | N/A | 26/26 | 100.00% | 0 | none |
| payments/admin.py | 14/14 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| payments/forms.py | 18/18 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| payments/models.py | 80/80 | 100.00% | none | N/A | N/A | 21/22 | 95.45% | 1 | 94 -> 96 |
| payments/receipts.py | 21/21 | 100.00% | none | N/A | N/A | 2/2 | 100.00% | 0 | none |
| payments/services.py | 29/29 | 100.00% | none | N/A | N/A | 4/4 | 100.00% | 0 | none |
| payments/urls.py | 3/3 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| payments/views.py | 91/91 | 100.00% | none | N/A | N/A | 26/26 | 100.00% | 0 | none |
| reports/admin.py | 0/0 | N/A | none | N/A | N/A | 0/0 | N/A | 0 | none |
| reports/models.py | 0/0 | N/A | none | N/A | N/A | 0/0 | N/A | 0 | none |
| reports/services.py | 26/26 | 100.00% | none | N/A | N/A | 6/6 | 100.00% | 0 | none |
| reports/urls.py | 4/4 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| reports/views.py | 56/56 | 100.00% | none | N/A | N/A | 14/14 | 100.00% | 0 | none |
| scripts/run_checks.py | 79/95 | 83.16% | 35-36, 39-41, 46-48, 50-51, 53-56, 58, 250 | N/A | N/A | 12/14 | 85.71% | 2 | 162 -> 167; 249 -> 250 |
| students/admin.py | 9/9 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| students/forms.py | 27/27 | 100.00% | none | N/A | N/A | 6/6 | 100.00% | 0 | none |
| students/models.py | 46/46 | 100.00% | none | N/A | N/A | 8/8 | 100.00% | 0 | none |
| students/urls.py | 3/3 | 100.00% | none | N/A | N/A | 0/0 | N/A | 0 | none |
| students/views.py | 86/86 | 100.00% | none | N/A | N/A | 20/20 | 100.00% | 0 | none |
