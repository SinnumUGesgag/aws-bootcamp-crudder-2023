import { Auth } from 'aws-amplify';

export async function getAccessToken(access_token){
  Auth.currentSession().then((cognito_user_session)=>{
      console.log('cognito_user_session', cognito_user_session);
      localStorage.setItem("access_token", cognito_user_session.accessToken.jwtToken);
      access_token(cognito_user_session.accessToken.jwtToken)
  }).catch((err) => console.log(err));
};


export async function checkAuth(setUser){
    Auth.currentAuthenticatedUser({
      //optional, by default is false.
      //if set to true, this call will send a 
      //request to Cognito to get the latest user data
      bypassCache: false
    }).then((cognito_user)=>{
      console.log('cognito_user', cognito_user);
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
      return Auth.currentSession()
    }).then((cognito_user_session) => {
      console.log('cognito_user_session', cognito_user_session);
      localStorage.setItem("access_token", cognito_user_session.accessToken.jwtToken);
    }).catch((err) => console.log(err));
};
