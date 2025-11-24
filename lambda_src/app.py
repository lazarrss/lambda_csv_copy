import os
import boto3
import urllib.parse

s3 = boto3.client("s3")

DEST_BUCKET = os.environ.get("DEST_BUCKET")
DEST_PREFIX = os.environ.get("DEST_PREFIX", "processed/")


def handler(event, context):
    print("EVENT:", event)

    if not DEST_BUCKET:
        raise RuntimeError("DEST_BUCKET env var nije podešen")

    for record in event["Records"]:
        src_bucket = record["s3"]["bucket"]["name"]
        src_key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"], encoding="utf-8"
        )

        print(f"Reading s3://{src_bucket}/{src_key}")

        obj = s3.get_object(Bucket=src_bucket, Key=src_key)
        body = obj["Body"].read()  # bytes, ne diramo sadržaj

        dest_key = DEST_PREFIX.rstrip("/") + "/" + src_key.split("/")[-1]

        print(f"Writing s3://{DEST_BUCKET}/{dest_key}")

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=dest_key,
            Body=body,
            ContentType="text/csv",
        )

    return {"statusCode": 200}
