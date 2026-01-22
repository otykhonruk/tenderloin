-- name: ingest_doc(src, doc_id, doc)!
insert into docs_raw(src, doc_id, doc)
values(:src, :doc_id, :doc)
on conflict do nothing


-- name: get_doc_by_id(src, id)$
select doc from docs_raw where src=:src and doc_id=:id


-- name: list_ids(src)
select doc_id from docs_raw where src=:src


-- name: get_doc_by_edrpou(src, edrpou)
select doc from docs_raw where src=:src and doc->>\'UA-EDR\'=:edrpou


-- ЄДРПОУ
-- select doc->'procuringEntity'->'identifier'->>'id' from docs_raw
