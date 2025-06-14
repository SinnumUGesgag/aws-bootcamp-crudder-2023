import './ConfirmationPage.css';
import React from "react";
import { useParams } from 'react-router-dom';
import {ReactComponent as Logo} from '../components/svg/logo.svg';

import { Auth } from 'aws-amplify';

export default function ConfirmationPage() {
  const [email, setEmail] = React.useState('');
  const [code, setCode] = React.useState('');
  const [errors, setErrors] = React.useState('');
  const [codeSent, setCodeSent] = React.useState(false);

  const params = useParams();

  const code_onchange = (event) => {
    setCode(event.target.value);
  }
  const email_onchange = (event) => {
    setEmail(event.target.value);
  }

  const resend_code = async (event) => {
    console.log('resend_code')
    // [TODO] Authenication
  }
  

  const onsubmit = async (event) => {
    event.preventDefault();
    console.log('ConfirmationPage.onsubmit')
    Auth.confirmSignUp(email,code);
    //return false
  }

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

  React.useEffect(()=>{
    if (params.email) {
      setEmail(params.email)
    }
  }, [])

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