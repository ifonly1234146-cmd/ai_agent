---
name: jaryo-db-schema
description: 자료조사DB Notion schema and data source ID for page creation
metadata:
  type: project
---

자료조사DB data source ID: `a440287a-4656-4ee5-a5f5-f1ff22cac08c`
Database ID: `c3e2ac43-a0de-413d-8a11-35167dee5d79`
Parent page: 노션DB (`38c8fb56-c419-8007-8774-d6dd94e2cce2`)

Schema fields:
- 조사명 (title) — page title
- 기한 (date) — use `date:기한:start` key when creating pages
- 담당자 (person) — JSON array of user IDs
- 상세내용 (text) — summary/description of the research
- 완료여부 (checkbox) — "__YES__" / "__NO__"

**Why:** Use data_source_id (not database_id) when calling notion-create-pages for this DB, as it has a single collection source.

**How to apply:** Always pass `{"type": "data_source_id", "data_source_id": "a440287a-4656-4ee5-a5f5-f1ff22cac08c"}` as the parent when creating pages in 자료조사DB.
