import settings
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import dokusyometer
import json

_headers = {
    "Content-Type": "application/graphql",
    "x-api-key": settings.API_KEY,
}

_transport = RequestsHTTPTransport(
    headers=_headers,
    url=settings.ENDPOINT,
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)


def handler():
# def handler(event, context):    

    dm = dokusyometer.DokusyoMeter(settings.DOKUSYO_USER, settings.DOKUSYO_PASS)
    batch_json = dm.scrap_readbooks()
    # TODO: 本当はエラー分岐が必要


    query = """
        mutation batchAddBook($batch_json: [BookInput]) {
            batchAddBook(books: $batch_json) {
                id
                title
                author
                page
                readDate
            }
        }
        """

    rs = client.execute(gql(query), variable_values=json.dumps({"batch_json": batch_json}))
    print(rs)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
          },
        'body': rs
    }

# for debug
handler()

