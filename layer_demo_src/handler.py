from dateutil import parser # from layer

def main(event, context):
    example = "2022-05-16T06:31:00Z"
    dt = parser.isoparse(example)

    print("Parsed datetime from layer:", dt.isoformat())
    return {
        "statusCode": 200,
        "body": f"Layer is working, parsed: {dt.isoformat()}"
    }