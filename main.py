import os
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build

start_date = "2023-12-16"
end_date = "2023-12-16"

def initialize_bigquery_client(serviceAccountBigQuery):
    credentials = service_account.Credentials.from_service_account_file(
        serviceAccountBigQuery,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return bigquery.Client(
        credentials=credentials,
        project=credentials.project_id,
    )

def initialize_search_console_client(serviceAccountSearchConsole):
    credentials = service_account.Credentials.from_service_account_file(
        serviceAccountSearchConsole,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    return build(
      'searchconsole',
      'v1',
      credentials=credentials,
      cache_discovery=False
    )

def main(config):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    while start <= end:
        
        print(f"Extracting data from {start.strftime('%Y-%m-%d')}")

        # Get data from Search Console
        query_request = {
            'startDate': start.strftime("%Y-%m-%d"),
            'endDate': start.strftime("%Y-%m-%d"),
            'dimensions': ['query', 'page', 'country', 'device', 'date'],
            'rowLimit': 25000
        }

        response = config['search_console_client'].searchanalytics().query(
            siteUrl=config['site_url'],
            body=query_request
        ).execute()

        print(f"/tExtracted {len(response.get('rows', []))} rows")

        if len(response.get('rows', [])) > 0:

            # Save data to BigQuery
            export_rows = []
            for i, row in enumerate(response.get('rows', [])):
            
                export_rows.append({
                    "data_date": row['keys'][4],
                    "site_url": site_url,
                    "query": row['keys'][0],
                    "is_anonymized_query": False,
                    "country": row['keys'][2],
                    "search_type": "web",
                    "device": row['keys'][3],
                    "impressions": row['impressions'],
                    "clicks": row['clicks'],
                    "sum_top_position": int(round(float(row['position'])))
                })
            
            try:
                error = config['bigquery_client'].insert_rows_json(
                    config['bigQueryExportTable'],
                    export_rows
                )
                if error != []:
                    print("Encountered errors while inserting rows: {}".format(error))
            except Exception as e:
                print(f"Error saving products: {e}")

        start += timedelta(days=1)

if __name__ == "__main__":

    site_url = os.environ['SITE_URL']
    bigQueryExportTable = os.environ['BIGQUERY_EXPORT_TABLE']
    serviceAccountBigQuery = os.environ['SERVICE_ACCOUNT_BIGQUERY']
    serviceAccountSearchConsole = os.environ['SERVICE_ACCOUNT_SEARCH_CONSOLE']

    bigquery_client = initialize_bigquery_client(serviceAccountBigQuery)
    search_console_client = initialize_search_console_client(serviceAccountSearchConsole)

    config = {
        "site_url": site_url,
        "bigQueryExportTable": bigQueryExportTable,
        "bigquery_client": bigquery_client,
        "search_console_client": search_console_client
    }

    main(config)
