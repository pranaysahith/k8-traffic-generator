# Dispatcher

This container dispatches processor pods that process files from an S3 bucket.

## Configuration

Several environment variables may be set for configuration:

| Environment Variable | Description      | Default                                              |
| -------------------- | ---------------- | ---------------------------------------------------- |
| `ENDPOINT`           | S3 endpoint      | `play.min.io`                                        |
| `ACCESS_KEY`         | S3 access key    | `Q3AM3UQ867SPQQA43P2F`                               |
| `SECRET_KEY`         | S3 secret key    | `zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG`           |
| `BUCKET_NAME`        | S3 bucket name   | `2063b651-92a3-4a20-a4a5-03a96e7c5a89`               |
| `PROCESSOR_IMAGE`    | Processor image  | `yardenshoham/glasswall-rebuild-eval:process-mode-0` |
| `DOWNLOADER_IMAGE`   | Downloader image | `yardenshoham/local-rebuild-downloader`              |
