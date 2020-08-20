from lib import bean_to_json, json_to_bean

def handle(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        return ('', 204, headers)

    try:
        if 'bean_to_json' in request.path:
            data = request.get_data(as_text=True)
            json_str, *_ = bean_to_json(data)
            headers["Content-Type"] = "application/json"
            return json_str, headers
        if 'json_to_bean' in request.path:
            data = request.get_data(as_text=True)
            bean_str, *_ = json_to_bean(data)
            headers["Content-Type"] = "application/vnd+beancount"
            return bean_str, headers
    except Exception as e:
        return e.__str__(), 500, headers

    return f'/json_to_bean or /bean_to_json!', 400


if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/<path>', methods=['GET', 'POST', 'OPTIONS'])(lambda path: handle(request))
    app.run(port=5552)