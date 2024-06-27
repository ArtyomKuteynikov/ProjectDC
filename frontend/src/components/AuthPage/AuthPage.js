import React from 'react';
import { NavLink } from 'react-router-dom';
import logoPath from '../../images/logo.svg';
import './AuthPage.css';

const AuthPage = ({
    texts, 
    children, 
    handleSubmitClick, 
    errorClass, 
    isButtonDisabled, 
    errorText
  }) => {
  const {
    greeting,
    buttonText,
    suggestionText,
    linkText,
    linkTo
  } = texts;
  
  return (
    <main className='auth-page'>
      <NavLink to="/" className='auth-page__logo'>
        <img alt='логотип' src={logoPath} />
      </NavLink>

      <h1 className='auth-page__title'>{greeting}</h1>
      <form 
        action="/" 
        onSubmit={handleSubmitClick} 
        name="search-form" 
        noValidate 
        className="auth-page__form"
      >
          {children}
          <span className={errorClass}>{errorText}</span>
          {isButtonDisabled ? 
            <button 
              type="submit" 
              className="auth-page__button auth-page__button_disabled"
              disabled
            >{buttonText}</button>
          : <button 
              type="submit" 
              className="auth-page__button"
            >{buttonText}</button>
          }
      </form>
      <div className='auth-page__suggestion'>
        <p className='auth-page__question'>{suggestionText}</p>
        <NavLink to={linkTo} className='auth-page__link' >{linkText}</NavLink>
      </div>
    </main>
  )
}

export default AuthPage