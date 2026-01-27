-- name: ingest_doc(doc_id, doc)!
insert into prozorro_tenders(doc_id, doc) values(:doc_id, :doc) on conflict do nothing

-- name: get_tender_by_id(id)$
select doc from prozorro_tenders where doc_id=:id

-- name: list_ids_exist(ids)
select doc_id from docs_raw where doc_id = any(:ids)

-- name: get_doc_by_edrpou(edrpou)
select doc from docs_raw where doc->>\'UA-EDR\'=:edrpou

-- name: list_tenders()
select doc_id, doc->'releases'->0->'tender'->>'title' as title
from prozorro_tenders limit 10


-- ЄДРПОУ
-- select doc->'procuringEntity'->'identifier'->>'id' from docs_raw
