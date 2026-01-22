GENERIC_INGEST_DOC_QUERY = '''
 INSERT INTO ingestion_log(status, src, doc_id, doc) VALUES($1, $2, $3, $4) ON CONFLICT DO NOTHING
'''

GET_DOC_BY_ID_QUERY = 'SELECT doc FROM ingestion_log WHERE src=$1 and doc_id=$2'

LIST_DOCS_QUERY = 'SELECT doc_id FROM ingestion_log WHERE src=$1'
