import React, { useContext, useState, useEffect } from 'react';
import AuthInput from '../AuthInput/AuthInput';
import AuthPage from '../AuthPage/AuthPage';
import { authorize } from '../../utils/MainApi';
import { AppContext } from '../../contexts/AppContext';
import { useNavigate } from 'react-router-dom';

import { 
  LOGIN_TEXTS, 
  EMPTY_FIELD_LOGIN_ERROR_TEXT,
  EMAIL_ERROR_TEXT,
  STANDART_ERROR_TEXT,
 } from '../../utils/constants';

var validator = require("email-validator");

const Login = () => {
  const context = useContext(AppContext);
  const navigate = useNavigate();
  const [formValue, setFormValue] = useState({
    email: '',
    password: '',
  });

  const [errorClass, setErrorClass] = useState('auth-page__error-message');

  const [errorText, setErrorText] = useState(STANDART_ERROR_TEXT)
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);

  useEffect(() => {
    if(localStorage.getItem('jwt')) {
      navigate('/vacancy-search', {replace: true});
    }
  }, [navigate])

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormValue(formValue => {
      const newFormValue = {
        ...formValue,
        [name]: value,
      }
      if (validator.validate(newFormValue.email) && (newFormValue.password !== '')) {
        setIsButtonDisabled(false)
        setErrorClass('auth-page__error-message');
      } else {
        setIsButtonDisabled(true)
        if (!validator.validate(newFormValue.email)) {
          setErrorText(EMAIL_ERROR_TEXT)
        }
        if (newFormValue.password === '') {
          setErrorText(EMPTY_FIELD_LOGIN_ERROR_TEXT)
        }
        setErrorClass('auth-page__error-message auth-page__error-message_active');
      }
      return newFormValue;
    })
  }

  function handleSubmitClick(e) {
    e.preventDefault();
    if (!formValue.email || !formValue.password) { 
      return;
    }
    const { email, password } = formValue;
    authorize(email, password)
      .then(data => {
        if(data.token) {
          setFormValue({
            email: '',
            password: '',
          })
          context.setIsLoggedIn(true);
          navigate('/vacancy-search', {replace: true});
          setErrorClass('auth-page__error-message');
        } else {
          setErrorClass('auth-page__error-message auth-page__error-message_active');
        }
      })
      .catch(err => {
        console.log(err)
        setErrorClass('auth-page__error-message auth-page__error-message_active');
      })
  }

  return (
    <AuthPage 
      texts={LOGIN_TEXTS} 
      handleSubmitClick={handleSubmitClick} 
      errorClass={errorClass} 
      isButtonDisabled={isButtonDisabled}
      errorText={errorText}
    >
      <AuthInput 
        value={formValue.name}
        onChange={handleChange}
        name='email' 
        title='E-mail' 
        type='email' 
        min={6}
        max={24}
      />
      <AuthInput 
        value={formValue.name}
        onChange={handleChange}
        name='password' 
        title='Пароль' 
        type='password' 
        min={6}
        max={24}
      />
    </AuthPage>
  )
}

export default Login