# Local desktop browser observations — 10 November 2026

An isolated HMS instance was started on Windows with the existing synthetic MySQL database on loopback. The code base was `9cac895` with documentation-only work on top. Django's database system check reported no issues. The connected Chrome browser opened the local sign-in page; its exact version was not established.

A synthetic Warden signed in successfully. The dashboard, student list, bed availability list, allocation list, payments list and occupancy report opened and displayed their expected headings and synthetic records. The occupancy report showed the seeded 60-bed hostel with one occupied, 58 available and one under maintenance. These are page and navigation observations; they do not establish all create/edit workflows or the complete compatibility case.

An attempt to open Edge through the connected browser returned “Browser is not available”; no Edge test is claimed. Firefox, older browser versions, Linux deployment workflows and a real phone were not exercised in this run. The owner has separately approved skipping phone testing for mini-project tracking. TC-QUAL-03 remains NOT RUN against its original full criteria. This short local session is not a working-hours availability measurement.
