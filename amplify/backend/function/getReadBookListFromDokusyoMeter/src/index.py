import settings
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

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

query = """
        query getAllBook {
            listBooks {
                items {
                    id
                    page
                    readDate
                    title
                }
            }
        }
    """



# def handler():
def handler(event, context):
    print('received event:')
    
    rs = client.execute(gql(query))
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
# handler()

