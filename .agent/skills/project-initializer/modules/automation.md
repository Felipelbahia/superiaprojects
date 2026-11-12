## Automation and data rules

For projects that build workflows, scrapers, data pipelines or forecasts.

- **Use the domain SIP, do not improvise:**

  | Subject | SIP |
  |---|---|
  | n8n workflows, nodes, expressions | `sip-n8n` |
  | Scraping, crawling, search, extraction | `sip-firecrawl` |
  | Seasonality, trends, demand forecast | `sip-trends-previsao-demanda` |

- **Firecrawl scale:** under 10 scrapes in the batch, use the Firecrawl MCP; 10 or more, use Firecrawl Local via `sip-firecrawl` (health → start → use → **always stop** at the end).
- **Credentials:** live in the platform's credential store or `.env`, never inside exported workflow JSON, code or logs.
- **Test before activating, and keep the test:** run every workflow or pipeline on sample data and show the result before turning it on in production. Save that sample input and the expected result in the project (path from the destination map) and run them again after every change to the workflow.
- **Data:** never overwrite or delete production data without confirmation; keep the raw input of each run so it can be redone.
