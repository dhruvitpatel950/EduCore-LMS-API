from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "status": "failure",
            "code": response.status_code,
            "message": "An error occurred",
            "errors": {}
        }

        if "detail" in response.data:
            custom_data["message"] = response.data["detail"]
            del response.data["detail"]

        else:
            custom_data["message"] = "Validation Failed"
            custom_data["errors"] = response.data    

        response.data = custom_data
    return response        