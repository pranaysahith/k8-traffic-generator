FROM alpine:3.12 AS permissions-giver
WORKDIR /out
COPY docker-entrypoint.sh custom-entrypoint.sh
RUN chmod +x custom-entrypoint.sh

FROM minio/mc:RELEASE.2020-09-03T00-08-28Z AS runner
COPY --from=permissions-giver /out/custom-entrypoint.sh /usr/local/bin
ENV PROTOCOL=http \
    ENDPOINT=play.min.io \
    ACCESS_KEY=Q3AM3UQ867SPQQA43P2F \
    SECRET_KEY=zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG \
    BUCKET_NAME=2063b651-92a3-4a20-a4a5-03a96e7c5a89 \
    OBJECT_NAME="000001/docs/consent-form/1599793232877_1 (1).pdf"
ENTRYPOINT [ "custom-entrypoint.sh" ]