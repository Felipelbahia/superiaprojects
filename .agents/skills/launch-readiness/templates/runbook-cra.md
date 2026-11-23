# Runbook: actively exploited vulnerability (EU Cyber Resilience Act)

Applies to manufacturers of products with digital elements made available in the EU, including mobile apps. Reporting duties apply from **11 September 2026** (verificado 2026-10-12, digital-strategy.ec.europa.eu/en/policies/cra-reporting). Confirm that your product is in scope before relying on this.

**Owner:** <name>, <phone>. **Backup:** <name>.

| When | Action |
|---|---|
| T0 | You become aware of an **actively exploited** vulnerability (or a severe incident). Write the timestamp. |
| T0 + 24 h | **Early warning** via the single reporting platform (ENISA, CRA Art. 16). Include the Member States where the product is available. |
| T0 + 72 h | **Notification**: product, nature of the exploit and vulnerability, mitigations taken, mitigations users can apply. |
| Fix available + 14 days | **Final report** for the vulnerability (severe incident: within one month of the 72 h notification). |

**Meanwhile:** use the kill switch for the affected feature (`ops-resilience.md`), tell affected users, ship the fix (OTA if JS-only).

**Intake:** `security@<domain>` plus `/.well-known/security.txt` (template in this folder); keep dependency alerts on (Dependabot or equivalent).

Fines and other CRA duties (SBOM, conformity) are not covered here: não verificado.
