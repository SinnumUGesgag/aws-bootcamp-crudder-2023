# Week 3 — Decentralized Authentication

	Cognito & Amplify for Decentralized Authentication
	JWT Server Side Verify
	Corrections


__Cognito & Amplify for Decentralized Authentication__

I logged into AWS & utilized Cognito to create a User Group then I began configuring the Application:

_Configuring Frontend for Amplify_

_1._ Installed correct Libariries from the CLI while within ../frontend-react-js
```
npm install aws-amplify@^5 @aws-amplify/ui-react@^5
```
then after it's completed check /frontend-react-js/package.json for dependencies to make sure that "aws-amplify" is listed


_2._  Created a Cognito User Pool


_3._  I created 2 Global Enviroment Variables so I can keep my client ID & User Pool Id private

MY_COGNITO_USER_POOLS_ID 
MY_COGNITO_CLIENT_ID


_4._ Update Frontend Enviromental variables in the Docker Compose YML file:

 ```
# Cognito --->
REACT_APP_AWS_PROJECT_REGION: "${My_AWS_REGION}"
REACT_APP_AWS_COGNITO_REGION: "${My_AWS_REGION}"
REACT_APP_AWS_USER_POOLS_ID: "${MY_COGNITO_USER_POOLS_ID}"
REACT_APP_CLIENT_ID: "${MY_COGNITO_CLIENT_ID}"
# <---
 ```


_5._ Update .../App.js

i. updated the imports:
```
// Cognito --->
import { Amplify, Auth } from 'aws-amplify';
// <---
```

ii. updated the Amplify.configure method:
```
// Amplify Cognito --->
Amplify.configure( {
	"AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
	"aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
	"aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
	"aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
	
	Auth: {
		// REQUIRED - Amazon Cognito Region
		region: process.env.REACT_APP_AWS_COGNITO_REGION,

		// OPTIONAL - Amazon Cognito User Pool ID
		userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,

		// OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
		userPoolWebClientId: process.env.REACT_APP_CLIENT_ID,

		// OPTIONAL - Enforce user authentication prior to accessing AWS resources or not
		//mandatorySignIn: false,

		// OPTIONAL - This is used when autoSignIn is enabled for Auth.signUp
		// 'code' is used for Auth.confirmSignUp, 'link' is used for email link verification
		signUpVerificationMethod: 'code', 
	}
});

// You can get the current config object
const currentConfig = Auth.configure();

// <---
```


_6._ Testing
TESTED UI, worked
CHECK Logs from Frontend Container, no Errors were triggered
Commited Changes


_7._ Update ../HomeFeedPage.js

i. add to imports
```
// Cognito --->
import { Auth } from 'aws-amplify';
// <---
```

ii. Update checkAuth
```
// Cognito for the User Name & Preferred Name that'll be displayed --->
		// check if we are authenicated
const checkAuth = async () => {
	Auth.currentAuthenticatedUser({
		//optional, by default is false.
		//if set to true, this call will send a 
		//request to Cognito to get the latest user data
		bypassCache: false
	}).then((user)=>{
		console.log('user',user);
		return Auth.currentAuthenticatedUser()
	}).then((cognito_user) => {
		setUser({
			display_name: cognito_user.attributes.name,
			handle: cognito_user.attributes.preferred_name
		})
	}).catch((err) => console.log(err));
};
// <---
``` 


_8._  Update ../ProfileInfo.js
 
 i. Update imports
 ```
// Cognito --->
import { Auth } from 'aws-amplify';
// <---
```

ii. update signOut
```
// Cognito --->
const signOut = async () => {
	try {
		await Auth.signOut({ global: true });
		window.location.href = "/"
	} catch (error) {
		console.log('error signing out: ', error);
	}
}
// <---
```

_9._ Update .../SigninPage.js

i. update imports
```
// Cognito --->
import { Auth } from 'aws-amplify';
// <---
```

ii. update signIn
```
// Cognito --->
async function signIn() {
  try {
    const user = await Auth.signIn(username, password);
  } catch (error) {
    console.log('error signing in', error);
  }
}


const onsubmit = async (event) => {
	setErrors('')
	event.preventDefault();
	Auth.signIn(email, password)  // here we're using the email as the 'username' for the function, since the API calls email entries 'username'
	.then(user => {
		localStorage.setItem("access_token", user.signInUserSession.access_token.jwtT)
		window.location.href = "/"
	}).catch(errors => {
		if(errors.code === 'UserNotConfirmedException') {
			window.location.href = "/confirm"
		}
		setErrors(errors.message)
	})
	return false
}

// <---
```

_10._ Testing Again
Docker Compose up
Logs only minor warnings, no failed builds
Tested UI worked just fine
No committing yet; moving on to next instructions


_11._ Update .../SignupPage.js

i. update imports
```
// Cognito --->
import { Auth } from 'aws-amplify';
// <---
```

ii. update singUp function:
```
  // Congito --->
  const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();

    Auth.signUp({
      username: email,
      password: password,
      attributes: {
        email: email,
        username: username,
        preferred_username: name,
        name: name,
        },
      autoSignIn: {
        // optional - enables auto sign in after user is confirmed
        enabled: true
      }
      })
    .then(user => {
      console.log(user);
      console.log('no error; user registration successful');
      window.location.href = "/confirm?email=${email}"
    })
    .catch(errors => {
      console.log('error signing up:', errors);
      setErrors(errors.code + " : " + errors.message)
    });
	return false
  }
  // <---
```

iii. updated so it redirects to a Confirmation Page
```
window.location.href = "/confirm"
```

_12._ Testing Again
Docker Compose up
Logs only minor warnings, no failed builds
Tested UI worked just fine
Attempted to Sign up and got nothing to populate on the page, yet when troubleshooting I did found the following error: 
"error signing up: InvalidParameterException: Username should be either an email or a phone number."

so I had to go back and correct the User template for Sign up; then;  now all of it works; I even was able to register a new user

HOWEVER, I was not redirected to the Verification page
I checked my email, I got the verificaiton code
Commited the changes


_13._ updated confirmationPage.js

i. imports
```
// Cognito --->
import { Auth } from 'aws-amplify';
// <---
```

ii. updated onsubmit
```
  // Cognito --->
  const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();

    console.log('ConfirmationPage.onsubmit');

    Auth.confirmSignUp(email,code)
    .then(user => {
		  //localStorage.setItem("access_token", user.signInUserSession.access_token.jwtT)
		  window.location.href = "/"
      console.log('redirect: ', errors);
      //setErrors('redirect: ' + errors)
	  })
    .catch(errors => {
      console.log('confirmation invalid:', errors);
      setErrors(errors.code + " : " + errors.message)
    })
  }
  // < ---
```

iii. Update Resend_Code:

```
// Cognito --->
const resend_code = async (event) => {
	setErrors("")
	try {
		await Auth.resendSignUp(email);
		console.log('code resent successfully');
		sentCodeSent(true)
	} catch (err) {
		// does not return a code
		console.log(err)
		if (err.message === "Username cannot be empty"){
			setErrors("You need to provide an email in order to send Resend Activation Code")
		} else if (err.message === "Username/client id cobination not found."){
			setErrors("Email is invalid or cannot be found.")
		}
	}
}

// <---
```


_14._.  Updated Recovery Page.js

i. update imports

```
// Cognito --->
import { Auth } from 'aws-amplify';
// <---
```


ii.  update onsubmit_send_code

```
// Cognito --->
const onsubmit_send_code = async (event) => {
	event.preventDefault();
	setErrors("")
	Auth.forgotPassword(username)
	.then((data) => setFormState("confirm_code"))
	.catch((err) => setErrors(err.message));
	return false
}
// <---
```


iii. update onsubmit_confirm_code

```
// Cognito --->
const onsubmit_confirm_code = async (event) => {
	event.preventDefault();
	setErrors("")
	if (password == passwordAgain){
		Auth.forgotPasswordSubmit(username, code, password)
		.then((data) => setFormState("success"))
		.catch((err) => setErrors(err.message));
	} else {
		setErrors("Passwords do not match")
	}
	return false
}
// <---
```


_15._ Updated HomeFeedPage.js to communicate with the Backend for Cognito

i.  add into the loadData function

```
const loadData = async () => {
	try {
		const backend_url = '${process.env.REACT_APP_BACKEND_URL}/api/acitivities/home'
		const res = await fetch(backend_url, {
			//send token to backend for verification of user ->
			headers:{
				Authorization: 'Bearer ${localStorage.getItem("access_token")}'
			},
			//<-
			method: "GET"
		});
		let resJson = await res.json();
```

Move on to now setup Backend



_Configuring Backend for Amplify_

_1._ update app.py

i. replace CORS

was:
```
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since",
  methods="OPTIONS,GET,HEAD,POST"
)
```

with:
```
Cors = CORS(
	app,
	resources= {r"/api*": {"origins": origins}},
	headers= ['Content-Type', 'Authorization'],
	expose_headers= 'Authorization',
	methods= "OPTIONS,GET,HEAD,POST"
)
```

ii. def data_home():
```
@aws_auth.authentication_required
def data_home():
	# accepting a header from the frontend -->
	
	app.logger.debug("AUTH HEADER")
	app.logger.debug( requesst.headers.get('Authorization') ) #for debugging if the token is being passed along or not
	
	print(  
		requesst.headers.get('Authorization')
	)
	# <--
	data = HomeActivites.run()
	claims = aws.auth.claims
	app.logger.debug("claims: ", claims)
	return data, 200
```


_2._ creating under ../backend-flask

i. created a new folder "lib"

ii. created within the folder "cognito_token_verification.py 

```
import time
import requests
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode
from flask_awscognito.exceptions import FlaskAWSCognitoError, TokenVerifyError


class CogitoTokenVerification:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        self.region = region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.claims = None
        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client
        self._load_jwk_keys()

    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        try:
            response = self.request_client(keys_url)
            self.jwk_keys = response.json()["keys"]
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e

    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    def _find_pkey(self, headers):
        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")
        return self.jwk_keys[key_index]

    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            # construct the public key
            public_key = jwk.construct(pkey_data)
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")

    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # probably another exception

    def _check_audience(self, claims):
        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")

    def verify(self, token, current_time=None):
        """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
        if not token:
            raise TokenVerifyError("No token provided")

        headers = self._extract_headers(token)
        pkey_data = self._find_pkey(headers)
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims
```
	

_3._ add to ../backend-flask/requirments.txt
```
Flask-AWSCognito
```
then installed the requirements 


_4._ update Docker Compose YML file

i. updating Backend Enviromental Variables:

```
# Cognito --->
AWS_COGNITO_DOMAIN: `mycognitodomain
AWS_COGNITO_USER_POOL_ID: `userpoolID
AWS_COGNITO_USER_POOL_CLIENT_ID: `myuserpoolsclientID
AWS_COGNITO_USER_POOL_CLIENT_SECRET: `myuserpoolsclientsecret
AWS_COGNITO_REDIRECT_URL: `conitoredirecturl
# <---
```


_5._ update app.py

i. app = flask...

```
app = Flask(__name__)

# Cognito --->
app.config['AWS_COGNITO_USER_POOL_ID'] = os.getenv("AWS_COGNITO_USER_POOL_ID")
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")

aws_auth = AWSCognitoAuthentication(app)
# <---
```


_6._ Adding exceptions to cognitoToken.py

```
class FlaskAWSCognitoError(Exception):
    pass


class TokenVerifyError(Exception):
    pass
```


_7._ Updated App.py 

i. import the function from cognitoToken.py into app.py

```
from lib.cognitoToken import CogitoTokenVerification
```

ii. adding the funciton into the app within app.py

```
app = Flask(__name__)

cognitoToken = CogitoTokenVerification(
  self, 
  user_pool_id='AWS_COGNITO_USER_POOL_ID', 
  user_pool_client_id='AWS_COGNITO_USER_POOL_CLIENT_ID', 
  region='AWS_DEFAULT_REGION', 
  request_client=None
)
```
		
_Corrections for Amplify_

_1._ Added Required Attributes


_2._ Updated SignUp Page's Code
i. Replaced import cookies with...
```
// Coginto --->
import { Auth } from "aws-amplify";
// <---
```

ii. Replaced onsubmit with...
```
const [cognitoErrors, setErrors] = React.useState('');

// Coginto --->
const onsubmit = async (event) => {
	event.preventDefault();
	setErrors('')
	try {
		const { user } = await Auth.signUp({
			username: email,
			password: password,
			attributes: { // these need to match the Coginto User Pool's Attributes
				name: name,
				email: email,
				preferred_username: username,
			},
			autoSignIn: { //optional - enables auto sign in after user is confirmed
				enable: true,
			}
			
		});
		console.log(user);
		window.location.href = '/confirm?email=${email}'
	} catch (errors) {
		console.log(errors);
		setErrors(errors.message)
	}
	return false
}
if (cognitoErrors){
	errors = <div className='errors'>{cognitoErrors}</div>;
}

//  before submit component
{errors}
// <---
```


_3._ Updated Confirmation Page:

i. replaced cookies...
```
import { Auth } from "aws-amplify";
```

ii. replaced resend_code with...
```
// Cognito --->
const resend_code = async (event) => {
	setErrors('')
	try {
		await Auth.resendSignUp(email);
		console.log('code resent successfully');
		setCodeSent(true)
	} catch (errors) {
		console.log(errors)
		if (errors.message == 'Username cannot be empty'){
			setErrors("You need to provide an email in order to send Resend Activation Code")
		} else if (errors.message == "Username/client id combination not found."){
			setErrors("Email is invalid or cannot be found.")
		}
	}
}
// <---
```

iii. replaced onsubmit with...
```
// Coginto --->
const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('');
    try {
      await Auth.confirmSignUp(email, code);
      window.location.href = "/"
    } catch (error) {
      setErrors(error.message)
    }
    return false
  }
// <---
```


_4._ Update Recovery Page with...

i. added...
```
// Coginto --->
import { Auth } from 'aws-amplify';
// <---
```

ii. Replaced onsubmit_send_code with...
```
// Cognito --->
const onsubmit_send_code = async (event) => {
	event.preventDefault();
	setErrors('')
	Auth.forgotPassword(username)
	.then((data) => setFormState('confirm_code') )
	.catch((err) => setErrors(err.message) );
	return false
}
// <---
```

iii. Replaced onsubmit_confirm_code with...
```
// Coginto --->
const onsubmit_confirm_code = async (event) => {
	event.preventDefault();
	setErrors('')
	if( password == passwordAgain){
		Auth.forgotPasswordSubmit(username, code, password)
		.then((data) => setFormState('success') )
		.catch((err) => setErrors(err.message) );
	} else {
		setErrors('Passwords do not match')
	}
	return false
}
// <---
```

_5._ Update HeadFeedPage.js by adding the following to 
```
js
	headers: {
		Authorization: 'Bearer ${localStorage.getItem("access_token")}'
	}
```

_JWT Server Side Verify_

_1._ Docker Compose YML: backend variables

```
# Cognito --->
AWS_COGNITO_DOMAIN: `mycognitodomain
AWS_COGNITO_USER_POOL_ID: "${MY_COGNITO_USER_POOLS_ID}"
AWS_COGNITO_USER_POOL_CLIENT_ID: "${MY_COGNITO_CLIENT_ID}"
AWS_COGNITO_USER_POOL_CLIENT_SECRET: `myuserpoolsclientsecret
AWS_COGNITO_REDIRECT_URL: `conitoredirecturl
# <---
```


_2._ App.py

i. update Imports
```
# Customized Token Verification Solution w/ Cognito --->
  # Referenced for ideas: https://github.com/cgauge/Flask-AWSCognito/blob/master/flask_awscognito/plugin.py
from lib.cognitoToken import CogitoTokenVerification, extract_access_token, TokenVerifyError, FlaskAWSCognitoError
# <---
```

ii. update App
```
app = Flask(__name__)

# Cognito --->
app.config['AWS_COGNITO_USER_POOL_ID'] = os.getenv("AWS_COGNITO_USER_POOL_ID")
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")
app.config['AWS_DEFAULT_REGION'] = os.getenv("AWS_DEFAULT_REGION")

cognitoToken = CogitoTokenVerification(
  self, 
  user_pool_id='AWS_COGNITO_USER_POOL_ID', 
  user_pool_client_id='AWS_COGNITO_USER_POOL_CLIENT_ID', 
  region='AWS_DEFAULT_REGION', 
  request_client=None
)

aws_auth = AWSCognitoAuthentication(app)
# <---
```


iii. Updated the CORS
```

Cors = CORS(
	app,
	resources= {r"/api*": {"origins": origins}},
	headers= ['Content-Type', 'Authorization'],
	expose_headers= 'Authorization',
	methods= "OPTIONS,GET,HEAD,POST"
)

```

iv. updated def data_home
```
@app.route("/api/activities/home", methods=['GET'])
@aws_auth.authentication_required
def data_home():
  access_token = extract_access_token(request.headers)
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
```


_3._ requirments.txt

```
# Cognito --->
Flask-AWSCognito
# <---
```

then ran installation of the requirments


_4._  inside backend, created lib folder then created file "cognitoToken", then gave it the following code:

```
import time
import requests
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode


class FlaskAWSCognitoError(Exception):
    pass


class TokenVerifyError(Exception):
    pass


# additionally, I am seeing the use of "_" in the code that we copied from the Repo we're referencing in the video
#   I have NO idea why they have that placeholder; I'll investigate Later on to learn more
def extract_access_token(request_headers):
    access_token = None
    auth_header = request_headers.get("Authorization")
    if auth_header and " " in auth_header:
        _,access_token = auth_header.split()
    return access_token


class CogitoTokenVerification:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        self.region = region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.claims = None
        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client
        self._load_jwk_keys()

    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        try:
            response = self.request_client(keys_url)
            self.jwk_keys = response.json()["keys"]
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e

    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    def _find_pkey(self, headers):
        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")
        return self.jwk_keys[key_index]

    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            # construct the public key
            public_key = jwk.construct(pkey_data)
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")

    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # probably another exception

    def _check_audience(self, claims):
        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")

    def verify(self, token, current_time=None):
        """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
        if not token:
            raise TokenVerifyError("No token provided")

        headers = self._extract_headers(token)
        pkey_data = self._find_pkey(headers)
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims
        return claims
```


_5._ added to ProfileInfo.js for the Frontend

```
// Cognito --->
const signOut = async () => {
	try {
	  await Auth.signOut({ global: true });
	  window.location.href = "/"
	  localStorage.removeItem("access_token")
	} catch (error) {
	  console.log('error signing out: ', error);
	}
}
// <---

```


_6._ Testing Again & Corrections

I have found the following Errors:
a. Signing In gets this error: "Cannot read properties of undefined (reading 'jwtT')"
b. Once Logged in, if I go to the Home Page, nothing populates

I Investigated the Frontend Container's logs and found:

"
Browserslist: caniuse-lite is outdated. Please run:
  npx update-browserslist-db@latest
"
I also found errors stating
"
React Scripts not found
"

so I ran the command in ../workspace/aws-bootcamp-crudder-2023/frontend-react-js
```
npx update-browserslist-db@latest
```
then I ran
```
npm install --save react@latest
```

Result: Docker Compose Up again and the application worked just fine
 
I am able to register a new User, Confirm that user with the Confirmation Code that's emailed;
additionally, I am able to log in and remain logged in until I sign out.

