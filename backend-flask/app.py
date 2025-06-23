from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *

# Customized Token Verification Solution w/ Cognito --->
  # Referenced for ideas: https://github.com/cgauge/Flask-AWSCognito/blob/master/flask_awscognito/plugin.py
from lib.cognitoToken import CogitoTokenVerification, extract_access_token, TokenVerifyError, FlaskAWSCognitoError
# <---

# Honeycomb, Telemetry ------->
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# <---

# XRay --->
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
# <---

# For Cloudwatch Logs --->
import watchtower
import	logging
from time import	strftime
# <---

#  Rollbar --->
# import os
# import rollbar
# import rollbar.contrib.flask
# from flask import got_request_exception
# <---

# Configuring Logger to use Cloudwatch --->
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='Cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("test log")
# <---

# Honeycomb, Tracing ------->
# Initializes tracing and an exporter that sends data to Honeycomb
#provider = TracerProvider()
#processor = BatchSpanProcessor(OTLPSpanExporter())
#provider.add_span_processor(processor)
#trace.set_tracer_provider(provider)
#tracer = trace.get_tracer(__name__)
# <---


app = Flask(__name__)

# Cognito --->
#app.config['AWS_COGNITO_USER_POOL_ID'] = os.getenv("AWS_COGNITO_USER_POOL_ID")
#app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")
#app.config['AWS_DEFAULT_REGION'] = os.getenv("AWS_DEFAULT_REGION")

cognitoToken = CogitoTokenVerification(
  user_pool_id= os.getenv("AWS_COGNITO_USER_POOL_ID"),
  user_pool_client_id= os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"), 
  region= os.getenv("AWS_DEFAULT_REGION"), 
)

#aws_auth = AWSCognitoAuthentication(app)
# <---



# Honeycomb ------->
#FlaskInstrumentor().instrument_app(app)
#RequestsInstrumentor().instrument()
#provider.add_span_processor(processor)
# <---


# XRay to Configure the XRay Recorder & Middleware --->
xray_url = os.getenv("AWS_XRAY_URL")

xray_recorder.configure( service='backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
#  <---


frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]

Cors = CORS(
	app,
	resources= {r"/api*": {"origins": origins}},
	headers= ['Content-Type', 'Authorization'],
	expose_headers= 'Authorization',
	methods= "OPTIONS,GET,HEAD,POST"
)


# Rollbar --->
# rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
# with app.app_context():
#     """init rollbar module"""
#     rollbar.init(
#         # access token
#         rollbar_access_token,
#         # environment name - any string, like 'production' or 'development'
#         'development',
#         # server root directory, makes tracebacks prettier
#         root=os.path.dirname(os.path.realpath(__file__)),
#         # flask already sets up logging
#         allow_logging_basic_config=False)
#     # send exceptions from `app` to rollbar, using flask's signal system.
#     got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
# <---


# When an Error occurs, this will create a Report/Log for Cloudwatch-->
@app.after_request
@xray_recorder.capture('Error Testing')
def after_request( response ):
  timestamp = strftime('[%Y-%b-%d %H:%M]')
  LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
  LOGGER.error( response )
  return response
# <---


@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'andrewbrown'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/home", methods=['GET'])
#@aws_auth.authentication_required
def data_home():
  access_token = extract_access_token(request.headers)
  app.logger.debug("!!!!! -------- request header: " , request , "-------- !!!!!!")
  try:
      claims = CogitoTokenVerification.verify(request.headers)
      # authenticated request
      app.logger.debug("Authenticated")
      app.logger.debug("claims", claims)
  except TokenVerifyError as e:
      # unauthenticated request
      app.logger.debug("Unauthenticated")
      app.logger.debug("claims", claims)
  data = HomeActivites.run()
  return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'andrewbrown'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

# Test Rollbar --->
# @app.route('/rollbar/test')
# def rollbar_test():
# 	rollbar.report_message('Hello World!', 'warning')
# 	return "Hello Rollbar!"
# <---



if __name__ == "__main__":
  app.run(debug=True)

