import json
import uuid
import boto3
from datetime import datetime, timezone


# DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLShortener")


def lambda_handler(event, context):
    method = event.get("httpMethod", "GET")

    # =========================
    # POST /shorten
    # =========================
    if method == "POST":
        try:
            body = json.loads(event.get("body", "{}"))
        except json.JSONDecodeError:
            return response(400, {"message": "Invalid JSON"})

        original_url = body.get("url")

        if not original_url:
            return response(400, {"message": "URL is required"})

        # Generate a 6-character short code
        short_code = str(uuid.uuid4())[:6]

        # Current UTC time
        created_at = datetime.now(timezone.utc)

        # Expire after 7 days
        expires_at = int(created_at.timestamp()) + (7 * 24 * 60 * 60)

        item = {
            "shortCode": short_code,
            "originalUrl": original_url,
            "createdAt": created_at.isoformat(),
            "expiresAt": expires_at
        }

        # Save URL to DynamoDB
        table.put_item(Item=item)

        return response(
            201,
            {
                "shortCode": short_code,
                "shortUrl": f"/{short_code}",
                "originalUrl": original_url,
                "expiresAt": expires_at
            }
        )

    # =========================
    # GET /{shortCode}
    # =========================
    if method == "GET":
        path_parameters = event.get("pathParameters") or {}

        short_code = path_parameters.get("shortCode")

        if not short_code:
            return response(
                400,
                {"message": "Short code is required"}
            )

        # Look up short code in DynamoDB
        result = table.get_item(
            Key={
                "shortCode": short_code
            }
        )

        item = result.get("Item")

        if not item:
            return response(
                404,
                {"message": "Short URL not found or expired"}
            )

        # Real browser redirect
        return {
            "statusCode": 302,
            "headers": {
                "Location": item["originalUrl"],
                "Content-Type": "text/plain",
                "Access-Control-Allow-Origin": "*"
            },
            "body": ""
        }

    # =========================
    # Unsupported method
    # =========================
    return response(
        405,
        {"message": "Method not allowed"}
    )


# =========================
# Standard API response
# =========================
def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }