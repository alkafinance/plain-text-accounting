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
    if 'bean_to_json' in request.path:
        data = request.get_data(as_text=True)
        json_str, *_ = bean_to_json(data)
        return json_str, {"Content-Type": "application/json"}
    if 'json_to_bean' in request.path:
        data = request.get_data(as_text=True)
        bean_str, *_ = json_to_bean(data)
        return bean_str, {"Content-Type": "application/vnd+beancount"}
    return f'/json_to_bean or /bean_to_json!', 400


if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/<path>', methods=['GET', 'POST'])(lambda path: handle(request))
    app.run()