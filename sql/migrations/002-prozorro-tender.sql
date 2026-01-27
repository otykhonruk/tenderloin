-- prozorro tenders relational data model

create type tender_status as enum (
    'active.qualification',
    'active.awarded',
    'complete',
    'cancelled',
    'unsuccessful'
);

create type procurement_method as enum (
    'open',
    'selective',
    'limited',
    'direct'
);

create type procurement_method_type as enum (
    'aboveThresholdUA',
    'aboveThresholdEU',
    'belowThreshold',
    'reporting',
    'negotiation'
);

--  prozorro tender
create table if not exists prz_tenders (
    id char(32) primary key,
    dateCreated datetime,
    dateModified datetime,
    description text,
    owner text,
    procurementMethod procurement_method,
    procurementMethodType procurement_method_type,
    status tender_status,
    tenderID text,
    title text,
    value_currency char(3),
    value_amount decimal(19,2),
    value_vat_included boolean
);


create table if not exists prz_tender_items (
    id serial primary key,
    tender_id char(32) references prz_tenders(id),
    description text,
    classification_scheme text,
    classification_id text,
    classification_description text,
    quantity integer,
    unit_name text,
    unit_code text,
    amount decimal(19,2),
    currency char(3)
);


create table if not exists prz_procuring_entities (
    id serial primary key,
    tender_id char(32) references prz_tenders(id),
    name text,
    identifier_scheme text,
    identifier_id text,
    identifier_legal_name text,
    identifier_uri text,
    address_street_address text,
    address_locality text,
    address_region text,
    address_postal_code text,
    address_country_name text,
    contact_point_name text,
    contact_point_email text,
    contact_point_telephone text,
    contact_point_fax_number text,
    contact_point_url text
);


create table if not exists prz_addresses (
    id serial primary key,
    entity_id char(32) references prz_procuring_entities(id),
    street_address text,
    locality text,
    region text,
    postal_code text,
    country_name text
);


create table if not exists prz_identifiers (
    id text primary key,
    legal_name text,
    scheme text
);
