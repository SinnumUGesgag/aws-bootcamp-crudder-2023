import './SignupPage.css';
import React from "react";
import {ReactComponent as Logo} from '../components/svg/logo.svg';
import { Link } from "react-router-dom";

// Cognito --->
import { Auth } from 'aws-amplify';
// <---

export default function SignupPage() {

  // Username is Eamil
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [preferred_username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');

  // Congito --->
  const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();

    Auth.signUp({
      username: email,
      password: password,
      attributes: {
        email: email,
        preferred_username: preferred_username,
        name: name
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
  }
  // <---

  const name_onchange = (event) => {
    setName(event.target.value);
  }
  const email_onchange = (event) => {
    setEmail(event.target.value);
  }
  const username_onchange = (event) => {
    setUsername(event.target.value);
  }
  const password_onchange = (event) => {
    setPassword(event.target.value);
  }

  let el_errors;
  if (errors){
    el_errors = <div className='errors'>{errors}</div>;
  }

  return (
    <article className='signup-article'>
      <div className='signup-info'>
        <Logo className='logo' />
      </div>
      <div className='signup-wrapper'>
        <form 
          className='signup_form'
          onSubmit={onsubmit}
        >
          <h2>Sign up to create a Cruddur account</h2>
          <div className='fields'>
            <div className='field text_field name'>
              <label>Name</label>
              <input
                type="text"
                value={name}
                onChange={name_onchange} 
              />
            </div>

            <div className='field text_field email'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange} 
              />
            </div>

            <div className='field text_field username'>
              <label>Username</label>
              <input
                type="text"
                value={preferred_username}
                onChange={username_onchange} 
              />
            </div>

            <div className='field text_field password'>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={password_onchange} 
              />
            </div>
          </div>
          {el_errors}
          <div className='submit'>
            <button type='submit'>Sign Up</button>
          </div>
        </form>
        <div className="already-have-an-account">
          <span>
            Already have an account?
          </span>
          <Link to="/signin">Sign in!</Link>
        </div>
      </div>
    </article>
  );
}