-- Table for storing raw responses from prozorro and dream APIs
create table if not exists docs_raw (
    id serial primary key,
    modified_at timestamp default current_timestamp,
    src char(1) not null, -- P: prozorro, D: dream
    stage integer not null default 0,
    doc_id text not null,
    doc jsonb
);
create unique index if not exists idx_raw_data_src_doc on raw_data (src, doc_id);


-- Raw data from spending.gov.ua transactions API endpoint
create table if not exists spd_transaction_raw (
    id bigint primary key, -- унікальний ідентифікатор трансакції в Системі
    doc_vob	text, -- код розрахункового документа
    doc_vob_name text, -- назва коду розрахункового документа
    doc_number	text, -- номер розрахункового документа, до 35 знаків
    doc_date	text, -- дата складання розрахункового документа у форматі РРРР-ММ-ДД
    doc_v_date	text, -- дата валютування документа у форматі РРРР-ММ-ДД
    trans_date	text, -- дата оплати у форматі РРРР-ММ-ДД
    amount decimal(19,2), -- сума оплати в гривнях з копійками, роздільник крапка
    amount_cop bigint, -- сума оплати в копійках
    currency text, -- літеральний код валюти (довідник)
    payer_edrpou char(8), -- код ЄДРПОУ платника, 8 знаків
    payer_name text, -- найменування платника, до 140 знаків
    payer_account text, -- рахунок платника (IBAN), до 29 знаків
    payer_mfo char(6), -- код банку платника (опціонально), 6 знаків
    payer_bank text, -- найменування банку платника (опціонально), до 140 знаків
    payer_edrpou_fact char(8), -- код ЄДРПОУ фактичного платника, 8 знаків
    payer_name_fact	text, -- найменування фактичного платника, до 140 знаків
    recipt_edrpou char(10), -- код ЄДРПОУ отримувача, 8 або 10 знаків
    recipt_name	text, -- найменування отримувача, до 140 знаків
    recipt_account text, -- рахунок отримувача (IBAN), до 29 знаків
    recipt_mfo char(6), -- код банку отримувача (опціонально), 6 знаків
    recipt_bank	text, -- найменування банку отримувача (опціонально), до 140 знаків
    recipt_edrpou_fact char(10), -- код ЄДРПОУ фактичного отримувача, 8 або 10 знаків
    recipt_name_fact text, -- найменування фактичного отримувача, до 140 знаків
    payment_details	text, -- призначення платежу, до 420 знаків
    doc_add_attr text, -- додатковий реквізит, до 80 знаків (опціонально)
    region_id integer, -- Ціле число	код регіону (довідник)
    payment_type text, -- тип платіжної системи
    payment_data text, -- додаткові дані для типу платіжної системи (опціонально)
    source_id integer, -- унікальний ідентифікатор джерела даних в Системі
    source_name	text, -- найменування джерела даних, до 140 знаків
    kekv integer, --код економічної класифікації видатків, 4 знаки (довідник)
    kpk	text, -- код програмної класифікації видатків та кредитування, до 7 знаків (довідник ДБ, довідник МБ)
    contractId text, -- унікальний ідентифікатор договору про закупівлю в системі Prozorro, 32 знаки
    contractNumber text, -- унікальний ідентифікатор закупівлі в системі Prozorro, 22 знаки
    budgetCode char(10), -- код бюджету, 10 знаків (довідник)
    system_key text, -- Внутрішній номер документа
    system_key_ff text -- Ідентифікатор бюджетного фінансового зобов’язання		
);
