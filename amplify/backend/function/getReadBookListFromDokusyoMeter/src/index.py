import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# AppSyncのエンドポイントのURL
ENDPOINT="https://s7ni7go37fak3domb2yeimie3i.appsync-api.us-east-2.amazonaws.com/graphql"
# AppSyncのAPI KEY
API_KEY="da2-g5xlj3b5ivg65dfwpnkgzgkwge"

_headers = {
    "Content-Type": "application/graphql",
    "x-api-key": API_KEY,
}

_transport = RequestsHTTPTransport(
    headers=_headers,
    url=ENDPOINT,
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

