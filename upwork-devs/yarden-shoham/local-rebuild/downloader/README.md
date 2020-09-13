# Downloader

This container downloads a single object from S3.

## Configuration

Several environment variables may be set for configuration:

| Environment Variable | Description                                    | Default                                            |
| -------------------- | ---------------------------------------------- | -------------------------------------------------- |
| `PROTOCOL`           | Protocol to use when connecting to S3 endpoint | `http`                                             |
| `ENDPOINT`           | S3 endpoint                                    | `play.min.io`                                      |
| `ACCESS_KEY`         | S3 access key                                  | `Q3AM3UQ867SPQQA43P2F`                             |
| `SECRET_KEY`         | S3 secret key                                  | `zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG`         |
| `BUCKET_NAME`        | S3 bucket name                                 | `2063b651-92a3-4a20-a4a5-03a96e7c5a89`             |
| `OBJECT_NAME`        | S3 object name                                 | `000001/docs/consent-form/1599793232877_1 (1).pdf` |
