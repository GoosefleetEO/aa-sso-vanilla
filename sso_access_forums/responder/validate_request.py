from django.http import HttpRequest

def validate_request(request: HttpRequest, client_id):
    request_data = request.GET.dict()

    _validate_client_id(request_data, client_id)
    _validate_timestamp(request_data)

def _validate_client_id(request_data: dict, client_id):
    if not 'client_id' in request_data:
        raise RuntimeError(f"Missing parameter 'client_id'")

    if request_data['client_id'] != client_id:
        raise RuntimeError(f'Invalid client{request_data["client_id"]}')

def _validate_timestamp(request_data: dict):
    if not 'timestamp' in request_data:
        # We want this so we can do
        # basic sanity checking on if the user's
        # auth has expired.
        #
        # The example doesn't *do* anything
        # with the value, but it's the thought
        # that counts
        raise RuntimeError("Missing parameter 'timestamp'")