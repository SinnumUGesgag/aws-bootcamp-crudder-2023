import './ConfirmationPage.css';
import React from "react";
//import { useParams } from 'react-router-dom';
import {ReactComponent as Logo} from '../components/svg/logo.svg';

// Cognito --->
import { Auth } from 'aws-amplify';
// <---

export default function ConfirmationPage() {
  const [email, setEmail] = React.useState('');
  const [code, setCode] = React.useState('');
  const [errors, setErrors] = React.useState('');
  const [codeSent, CodeResent] = React.useState(false);

  //const params = useParams();

  const code_onchange = (event) => {
    setCode(event.target.value);
  }
  const email_onchange = (event) => {
    setEmail(event.target.value);
  }

  // Cognito --->
  const resend_code = async (event) => {
    setErrors("")
    try {
      await Auth.resendSignUp(email);
      console.log('code resent successfully');
      CodeResent(true)
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

 
/* for when the correct confirmation code is enterd; I'll add this after i've finished fixing & troubleshooting the JWST token issues
function listenToAutoSignInEvent() {

}
*/

  let el_errors;
  if (errors){
    el_errors = <div className='errors'>{errors}</div>;
  }


  let code_button;
  if (codeSent){
    code_button = <div className="sent-message">A new activation code has been sent to your email</div>
  } else {
    code_button = <button className="resend" onClick={resend_code}>Resend Activation Code</button>;
  }

  /* Use of this code is unclear for now, so I am commenting it out
  React.useEffect(()=>{
    if (params.email) {
      setEmail(params.email)
    }
  }, [])
  */

  return (
    <article className="confirm-article">
      <div className='recover-info'>
        <Logo className='logo' />
      </div>
      <div className='recover-wrapper'>
        <form
          className='confirm_form'
          onSubmit={onsubmit}
        >
          <h2>Confirm your Email</h2>
          <div className='fields'>
            <div className='field text_field email'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange} 
              />
            </div>
            <div className='field text_field code'>
              <label>Confirmation Code</label>
              <input
                type="text"
                value={code}
                onChange={code_onchange} 
              />
            </div>
          </div>
          {el_errors}
          <div className='submit'>
            <button type='submit'>Confirm Email</button>
          </div>
        </form>
      </div>
      {code_button}
    </article>
  );
}