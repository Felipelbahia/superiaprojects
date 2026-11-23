## Content rules

For projects that produce text: e-mails, posts, articles, scripts, press releases, newsletters.

- **Voice and audience:** before writing, read the project's brand files (`brand/` or `STANDARDS.md`: tone, audience, words to avoid). Missing? Ask for them once and save the answer there.
- **Facts:** every number, date, name and quote has a source the owner can check; no source = mark it `[to confirm]`, never invent.
- **Draft as a file:** every piece is saved as a file in the project before it is sent, scheduled or published.
- **Anti-slop pass (mandatory):** before delivering a final text, run skill `geral-anti-slop` (via `sip-marketing`) and remove AI clichés.
- **Approval before sending:** never send, schedule or publish without the owner's explicit approval of the final text. A draft approved earlier does not cover later edits.
- **Use the domain SIP, do not improvise:**

  | Subject | SIP |
  |---|---|
  | Copy, social, video, growth, marketing strategy | `sip-marketing` |
  | Press, PR, media monitoring | `sip-imprensa` |
  | E-mail campaigns, segments, Mautic, Mailgun | `sip-mautic` |
  | Web research, scraping, crawling, extraction | `sip-firecrawl` |

- **Automatable checks:** what a script can check (required metadata fields, broken links, dates, words to avoid from `brand/`) becomes a check in the project's `verification.json` of skill `deliverable-verification` (`forbidden`, `required_mentions`; links and dates as `custom_checks`) and runs before every delivery.
- Bulk e-mail or a new sending domain: run skill `launch-readiness` (deliverability) first.
