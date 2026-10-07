# Hostel Management System — Design Deliverables

## Design Ownership / Revision History

| Version | Contributor | Contribution |
|---|---|---|
| 1.0 | G.V.N. Sreeharsha | Initial SAD baseline and requirement alignment |
| 1.1 | Chennamraju Vaishnavi | Design review from the testing perspective |
| 1.2 | Devansh Gupta | Architecture and security design review |

## UML Diagrams

| ID | Diagram | Main Flow |
|---|---|---|
| UC-01 | Use Case Diagram | Admin, Warden and Student interaction with HMS |
| CD-01 | Component Diagram | Web UI, application modules C2–C8, data layer C9 and MySQL C10 |
| SD-01 | Student Registration | Validation, duplicate Student ID check and save (REQ-5, REQ-6) |
| SD-02 | Bed Allocation | Transactional allocation with row lock and business-rule checks (REQ-14 to REQ-16) |

## Traceability

The diagrams are mapped to SRS requirements and SAD components. Editable diagram sources are kept in `diagrams/` as Mermaid (`.mmd`); the PNG files are the figures used in the SRS and SAD.
