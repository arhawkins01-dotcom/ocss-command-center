# Command Center Decision Logic

This document captures report-specific decision points and the high-level behavior that the `action_logic` module should encode.

## Standard Terminology

- Command Center Dashboard
- Assigned Case View
- Automated Caseload Assignment
- Action Status Update

## Report-Specific Notes

### 56RA
- Actions: verify paternity, schedule GT, prep ADS, refer to court, close case
- Decision signals: paternity status, prior GT scheduled, ADS ready

### Locate
- Actions: complete locate efforts, clear ILSU, attempt contact, determine UNL/NAS eligibility, close or advance when NCP located
- Decision signals: ILSU status, locate source results (BMV, SVES), postal verification outcome

### P-S
- Actions: GT scheduling, ADS prep, court referral, contact letters, postal verification
- Decision signals: prior contact attempts, court referral criteria, ADS readiness

## Implementation Guidance

- Keep decision functions small and testable.
- Return a structured decision object: `{ "action": str, "status": str, "narration": str }`.
- Avoid side-effects in decision functions; return decisions and let `report_engine` apply updates and persistence.
