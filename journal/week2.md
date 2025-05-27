# Week 2 — Distributed Tracing

# Summary
As you are reading my descriptions of what I input, I made the corrections and fixed Typos while I wrote these notes, so you won’t necessarily see what typos or syntax errors I made, yet I note when I ran into such mistakes.



# HoneyComb
I found while attempting to follow along with Anderw’s Tutorial, that a few things changed for HoneyComb, so I reviewed the HoneyComb OpenTelemetry Python just to be sure, however following what Andrew does in the Tutorial pretty much Works.

!!
Despite attempting to read and make sure I was keeping with current HoneyComb Documentation, I believe it’s best to follow the older tutorial that ExamPro provides, SINCE Honeycomb themselves has admitted that previous code & directories are still working but under maintenance; until they've fully released an update, there might be some issues however I have not found any issues following the older tutorial for HoneyComb.
!!

__1st] Created a new Honeycomb Environment "AWS_ExamPro_Bootcamp_CRUDDUR"; and 
created the Environmental Variable HONEYCOMB_API_KEY, setting to my API Key for
HONEYCOMB__

__2nd] Added to Docker Compose YML file, for the Backend-flask environment:__

```
# OTEL packages for Honeycomb ; I've commented it out for now, since I am not sending OTEL traffic --->
OTEL_SERVICE_NAME: "backend-flask"
OTEL_EXPORTER_OTLP_PROTOCOL: http/protobuf
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
# < ---
``` 

__3rd] Add required installations for Open Telemetry to the "requirments.txt" file__

```
# OTEL packages for Honeycomb ; I've commented it out for now, since I am not sending OTEL traffic --->
opentelemetry-api
opentelemetry-sdk
opentelemetry-exporter-otlp-proto-http
opentelemetry-instrumentation-flask
opentelemetry-instrumentation-requests
# <---
```

__4th] added to my Backend-flask's “app.py” file:

```
# Honeycomb, Telemetry ------->
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# <---

# Honeycomb, Tracing ------->
Initializes tracing and an exporter that sends data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
# <---

app = Flask(__name__)

# Honeycomb ------->
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
provider.add_span_processor(processor)
# <---
```

__5th] Docker Compose Up__

__6th] Once the Docker was up and running__

Access the Frontend via port 3000 URL, and was able to log into the application just fine
Accessed the Backend via port 4567 URL at .../api/activities/home ; I did not see data
Then I checked Docker container logs for Backend and saw...
"
Failed to export batch code: 401, reason: !missing 'x-honeycomb-team' header
"

I had a typo in the Header; called it HEADER instead of HEARDS, I was 
missing the S; fixed that and got a new error message:
"
Failed to export batch code: 401, reason: =unknown API key - check your credentials, region, and API URL
"

Typically 401 SIP Error codes are due to failed authentication or credentials for a requests
I was curious if ${HONEYCOMB_API_KEY} was wrong so I manually added
my KEY again...and it WORKED
 
"
[25/Apr/2025 17:33:12] "GET / HTTP/1.1" 404 -
[25/Apr/2025 17:33:19] "GET /api/activities/home HTTP/1.1" 200 -
"
Checked Honeycomb, and I am getting data

Now the question is, WHY did ${HONEYCOMB_API_KEY} fail to read the API Key that I had as an Environmental Variable?

Then I noticed that when I checked the Environmental
variable it had...changed; I didn't try to change it; I had it correct

so I saved the incorrect Key as APIKEY_TESTER then corrected my HONEYCOMB_API_KEY
Then I Compose Down
Checked, nothing was altered
Then I Compose Up
Checked, nothing was altered
Added back as the Header: x-honeycomb-team=${HONEYCOMB_API_KEY}
Then I Compose Down
Checked, nothing was altered 
Then I Compose Up
Checked, nothing was altered
Then I accessed the backend via 4567 URL /api/activities/home
to see if I could send data just fine
AND...
"
192.168.23.138 - - [25/Apr/2025 17:49:18] "GET / HTTP/1.1" 404 -
Failed to export batch code: 401, reason: =unknown API key - check your credentials, region, and API URL
192.168.23.138 - - [25/Apr/2025 17:49:23] "GET /api/activities/home HTTP/1.1" 200 -
Failed to export batch code: 401, reason: =unknown API key - check your credentials, region, and API URL
"
Checked the Environmental Variables to find...
Nothing had changed, they were not altered
Yet when I checked my Gitpod account’s Variable I say that HONEYCOMB_API_KEY was correct

So then I thought to check Honeycomb to see if my API Key was
Altered, but that was not the issue; the API Key had not changed in Honeycomb

Manually added the key back to the Header
compose Down
compose Up
And I was able to send Data just fine

Then I did some research into Docker YML files & Interpolation
The Syntax appears correct and SHOULD be working just fine

I put the header back as "x-honeycomb-team=${HONEYCOMB_API_KEY}"
Then committed the code as is so far

I suspect how the environment loaded  may have something to do with this;
so I have made the changes; committed them; and now will close this workspace
then stand up a new one to see if the issues persist

Tore down and deleted the Workspace
Then stood up a new Workspace and started over

1st thing I did was verify the API KEY, it was correct in my account settings 
and it was correct when I pulled it from the Terminal

2nd NPM install for Frontend & install requirements.txt for Backend

3rd Compose Up

Results...

IT WORKED!!!

"
192.168.144.202 - - [25/Apr/2025 19:18:23] "GET / HTTP/1.1" 404 -
192.168.144.202 - - [25/Apr/2025 19:18:24] "GET /favicon.ico HTTP/1.1" 404 -
192.168.144.202 - - [25/Apr/2025 19:18:42] "GET /api/activities/home HTTP/1.1" 200 -
"

FINALLY!!! Something was up with GITPOD; it was allowing me to change the 
variable in the workspace but it was not actually changing the Variable on a global 
Level (when when exporting) so when Docker Compose read the YML file it kept seeing the wrong API Key (likely what the Shell was holding onto) every time it attempted Interpolation for the line 
```
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
``` 



# XRay
__A: Installing SDK & testing dependencies__

adding to my requirements.txt file
```
# XRay --->
aws-xray-sdk
# <---
```

__B: Adding to ../aws-bootcamp-crudder-2023/backend-flask
/app.py:

```
# XRay --->
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
# <---

app = Flask(__name__)

# XRay to Configure the XRay Recorder & Middleware --->
xray_url = os.getenv("AWS_XRAY_URL")

xray_recorder.configure( service='backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
#  <---
```

__C:  Creating xray.json  to contain my Sampling Rules__

../aws-bootcamp-crudder-2023/aws/json
/xray.json:
```
{
"SamplingRule": {
        "RuleName": "Cruddur_SamplingRule",
        "ResourceARN": "*",
        "Priority": 9000,
        "FixedRate": 0.1,
        "ReservoirSize": 5, 
        "ServiceName": "backend-flask",
        "ServiceType": "*",
        "Host": "*",
        "HTTPMethod": "*",
        "URLPath": "*",
        "Version": 1
    }
}
```

__D: add to Docker Compose YML file for the backend-flask’s environment variables__

```
# Define XRay's URLPath & the Daemon's Address --->
AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
# <---
```

__E: Add to Docker Compose YML file__

```
 # Creates the XRay Daemon as a Docker Container w/in the Environment --->
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "${MY_AWS_REGION}"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - "2000:2000/udp"
  # <---		

networks:
  internal-network:
    driver: bridge
    name: cruddur
```

__F: I run the following commands, only once__
```
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```
to install the Sampling Rule creating in the JSON file

It worked, creating the sampling-rule

![created_xray_sampling rule](https://github.com/user-attachments/assets/0a22d0bd-361b-49f9-8728-a034b03a7097)


__G:	Run 1 time, from /workspace/aws-bootcamp-cruddur-2023/backend-flask
to create the XRay Group for this Project__
```
aws xray create-group \
	--group-name "Cruddur" \
	--filter-expression "service(\"backend-flask\")"
```

it worked, creating a Trace Group for XRay 

![created xray trace group](https://github.com/user-attachments/assets/c7f92f86-7bbf-4ecc-bfdd-e11d4af4f06b)


__H: added for XRay Segments to backend-flask activities:__

1.  ../aws-bootcamp-crudder-2023/backend-flask/services
/user_activities.py

```
# Xray -->
from aws_xray_sdk.core import xray_recorder
# <---
class UserActivities:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }
```

then further down

```
     }]
      model['data'] = results
      
    # Xray --->
    try:
      segment = xray_recorder.begin_segment('user_activities')

      subsegment =xray_recorder.begin_subsegment('mock-data')

      dict = {
        "now": now.isoformat(),
        "results-size": len(odel['data'])
      }

      subsegment.put_metadata('key',dict,'namespace')

    finally:
      xray_recorder.end_subsegment()
      xray_recorder.end_segment()
    # <---
    return model
```

__I: Opened up the Application off port 3000 and clicked around; checked the XRay Daemon's Logs and saw it was successfully sending Segments; Checked XRay, Traces were received successfully.__

![successful segment sent to xray](https://github.com/user-attachments/assets/ac048a5d-ffc5-43f6-98d3-aa33f35ea28d)

__J: Instructions & in the Tutorial I saw that for any specific activities we wanted to track, we can add the following:__

```
@xray_recorder.capture('name-of-activity')
```
I did not add any of this; I will if I need to do any tracking or troubleshooting in the future.



# WatchTower
using code from Watchtower
https://pypi.org/project/watchtower/


__1st] Add to requirement.txt__

```
# Cloudwatch Logs using Watchtower --->
watchtower
# <---
```

__2nd] added to app.py, right beneath__

```
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
# <---

# For Cloudwatch Logs --->
import watchtower
import	logging
from time import strftime
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
```

__3rd] add to app.py__
```
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since",
  methods="OPTIONS,GET,HEAD,POST"
)

# When an Error occurs, this will create a Report/Log for Cloudwatch-->
@app.after_request
@xray_recorder.capture('Error Testing')
def after_request( response ):
	timestamp = strftime('[%Y-%b-%d %H:%M]')
	LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
	return response
# <---
```

__4th] added to Docker Compose YML file__

inside the Backend-flask environment variables
```
AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
```

__5th] Tested Cloudwatch and found Logs receieved__

![cloudwatchlogs](https://github.com/user-attachments/assets/cb1df8a4-80e3-472b-ad72-213ef18c5568)



# Rollbar
__1st] I Setup My Rollbar Account__

__2nd] Add to Backend’s Requirements.txt__
```
# Rollbar -->
blinker
rollbar
# <---
```

__3rd] Grab my Rollbar Access Token, then__

run
```
/workspace $ export ROLLBAR_ACCESS_TOKEN="[my access token]"
```

I pasted my Access Token where I have "[my access token]"; I am just not
including it here in my journal.

__4th] Add to app.py__

```
#  Rollbar --->
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
# <---
```

__5th] Add further down in app.py__

Make sure to place this in the section of code containing all @app behaviors have been defined

!!
Originally Andrew shows the use of some code that is now depreciated
@app.before_first_request has been depreciated
So I replaced it app.app_context():
```
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since",
  methods="OPTIONS,GET,HEAD,POST"
)


# Rollbar --->
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
with app.app_context():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name - any string, like 'production' or 'development'
        'development',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)
    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
# <---
```

__6th] Further down in app.py, add__
This is for sending test data to Rollbar when the Backend is launched
```
# Test Rollbar --->
@app.route('/rollbar/test')
def rollbar_test():
	rollbar.report_message('Hello World!', 'warning')
	return "Hello World!"
# <---
```

__7th] Added to Docker Compose, backend-flask environment variables__
```
ROLLBAR_ACCESS_TOKEN: "${ROLLBAR_ACCESS_TOKEN}"
```

__8th: Compose Up and found the data reaching Rollbar__

![Rollbar](https://github.com/user-attachments/assets/8a055fc9-1f0b-4874-9b75-9fb9f48fd0fb)

