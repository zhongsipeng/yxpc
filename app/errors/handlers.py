import time
from flask import g, jsonify
from app.errors.exceptions import BusinessError
from jsonschema import ValidationError
from app.tools.resultmodel import successModel, failModel


def register_handlers(app):
    @app.before_request
    def before_request():
        g.exception_occurred = False

    @app.errorhandler(BusinessError)
    @app.errorhandler(ValidationError)
    def handle_business_error(e):
        g.exception_occurred = True
        # if(isinstance(e, BusinessError)):
        response = jsonify(failModel(e.message))
        # else:
        #     response = jsonify(failModel("系统异常"))
        return response
    # @app.after_request
    def wrap_response(response):
        if response.content_type != "application/json":
            return response
        try:
            if not g.exception_occurred :
                data = response.get_json()
                wrapped = successModel(data)
                response.data = jsonify(wrapped).data
        except Exception as e:
            print (e)   
        
        return response