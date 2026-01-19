-- Description: Table for storing raw data and logging ingestion process
create table if not exists ingestion_log (
    id serial primary key,
    modified_at timestamp default current_timestamp,
    status text not null,
    stage integer not null default 0,
    src char(3) not null, -- prz, spd, drm
    doc_id text,
    doc jsonb
);

create index if not exists idx_ingestion_log_src_doc on ingestion_log (src, doc_id);
