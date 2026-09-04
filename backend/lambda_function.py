import json
import uuid
import boto3
from datetime import datetime, timezone


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLShortener")


def lambda_handler(event, context):
    method = event.get("httpMethod", "GET")

    # POST /shorten
    if method == "POST":
        body = json.loads(event.get("body", "{}"))

        original_url = body.get("url")

        if not original_url:
            return response(400, {"message": "URL is required"})

        short_code = str(uuid.uuid4())[:6]

        item = {
            "shortCode": short_code,
            "originalUrl": original_url,
            "createdAt": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=item)

        return response(
            201,
            {
                "shortCode": short_code,
                "shortUrl": f"/{short_code}",
                "originalUrl": original_url
            }
        )

    # GET /{shortCode}
    if method == "GET":
        path_parameters = event.get("pathParameters") or {}
        short_code = path_parameters.get("shortCode")

        if not short_code:
            return response(400, {"message": "Short code is required"})

        result = table.get_item(
            Key={
                "shortCode": short_code
            }
        )

        item = result.get("Item")

        if not item:
            return response(404, {"message": "Short URL not found"})

        return {
    "statusCode": 302,
    "headers": {
        "Location": item["originalUrl"],
        "Access-Control-Allow-Origin": "*"
    },
    "body": ""
}

    return response(405, {"message": "Method not allowed"})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }