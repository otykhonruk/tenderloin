-- name: ingest_doc(id, status, code, cdu_response)!
insert into dream_ideas(id, status, code, cdu_response)
values(:id, :status, :code, :cdu_response)
on conflict do nothing

-- name: get_idea_by_id(id)$
select doc from dream_ideas where id=:id

-- name: ideas_exist(ids)
select id from dream_ideas where id = any(:ids)

-- name: get_doc_by_edrpou(edrpou)
select doc from docs_raw where doc->>\'UA-EDR\'=:edrpou
