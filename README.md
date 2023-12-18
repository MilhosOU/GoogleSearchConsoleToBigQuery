# GoogleSearchConsoleToBigQuery

This script is used to upload historical data from Google Search Console to BigQuery

The automatic connection from Search Console to BigQuery does not export historical data, but only from the day of the connection.

In order to push data to BigQuery from SearchConsole, it is important to:
- Enable Google Search API on Google Cloud Platform.
- Create a service account to manage BigQuery.
- Create a service account to manage Search Console and add it as user to the Google Search Console.
- Having a table on bigquery with already initiated an export automatic from Google Search Console, usually it is inside a _searchconsole_ schema.

# Usage

- Modify env variables as shown below.
- Modify start_date and end_date inside the script.


## Env Variables

```bash
export SITE_URL="sc-domain:THIS-IS-AN-EXAMPLE.COM"
export BIGQUERY_EXPORT_TABLE="PROJECT_ID.SCHEMA.TABLE"
export SERVICE_ACCOUNT_BIGQUERY="/PATH-TO-SERVICE_ACCOUNT-BIGQUERY"
export SERVICE_ACCOUNT_SEARCH_CONSOLE="/PATH-TO-SERVICE-ACCOUNT-SEARCH-CONSOLE"
```

## Notes

![Useful Google Notes](https://support.google.com/webmasters/answer/12917991?hl=en)
