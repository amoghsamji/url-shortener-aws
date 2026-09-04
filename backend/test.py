import json
from lambda_function import lambda_handler


# Create a short URL
create_event = {
    "httpMethod": "POST",
    "body": json.dumps({
        "url": "https://www.google.com/some/very/long/url"
    })
}

result = lambda_handler(create_event, None)

print("CREATE RESULT:")
print(result)


# Get the generated short code
body = json.loads(result["body"])
short_code = body["shortCode"]


# Access the short URL
get_event = {
    "httpMethod": "GET",
    "pathParameters": {
        "shortCode": short_code
    }
}

result = lambda_handler(get_event, None)

print("\nGET RESULT:")
print(result)