import './App.css';

import HomeFeedPage from './pages/HomeFeedPage';
import NotificationsFeedPage from './pages/NotificationsFeedPage';
import UserFeedPage from './pages/UserFeedPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';
import React from 'react';

// Cognito --->
import { Amplify, Auth } from 'aws-amplify';
// <---

import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";

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

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomeFeedPage />
  },
  {
    path: "/notifications",
    element: <NotificationsFeedPage />
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />
  },
  {
    path: "/messages/:message_group_uuid",
    element: <MessageGroupPage />
  },
  {
    path: "/signup",
    element: <SignupPage />
  },
  {
    path: "/signin",
    element: <SigninPage />
  },
  {
    path: "/confirm",
    element: <ConfirmationPage />
  },
  {
    path: "/forgot",
    element: <RecoverPage />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;