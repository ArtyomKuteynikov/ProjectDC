import React, { useState, useCallback, useContext, useEffect } from 'react';
import AuthInput from '../AuthInput/AuthInput';
import AuthPage from '../AuthPage/AuthPage';
import { register, authorize } from '../../utils/MainApi';
import { useNavigate } from 'react-router-dom';
import { AppContext } from '../../contexts/AppContext';

import { 
  REGISTER_TEXTS, 
  EMPTY_FIELD_ERROR_TEXT,
  EMAIL_ERROR_TEXT,
  NAME_ERROR_TEXT,
  STANDART_ERROR_TEXT,
 } from '../../utils/constants';

var validator = require("email-validator");

const Register = () => {
  const context = useContext(AppContext);

  const navigate = useNavigate();

  const [isButtonDisabled, setIsButtonDisabled] = useState(true);

  const [errorClass, setErrorClass] = useState('auth-page__error-message');

  const [formValue, setFormValue] = useState({
    name: '',
    email: '',
    password: '',
  });

  const [errorText, setErrorText] = useState(STANDART_ERROR_TEXT)

  useEffect(() => {
    if(localStorage.getItem('jwt')) {
      navigate('/vacancy-search', {replace: true});
    }
  }, [navigate])


  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    const regex = /[\wа-я\s\-ё]/gi;
    setFormValue(formValue => {
      const newFormValue = {
        ...formValue,
        [name]: value,
      }
      if (regex.test(newFormValue.name)
        && validator.validate(newFormValue.email)
        && (newFormValue.name !== '')
        && (newFormValue.password !== '')
      ) {
        setIsButtonDisabled(false)
        setErrorClass('auth-page__error-message');
      } else {
        setIsButtonDisabled(true)
        if (!regex.test(newFormValue.name)) {
          setErrorText(NAME_ERROR_TEXT)
        }
        if (!validator.validate(newFormValue.email)) {
          setErrorText(EMAIL_ERROR_TEXT)
        }
        if (newFormValue.name === '' || newFormValue.password === '') {
          setErrorText(EMPTY_FIELD_ERROR_TEXT)
        }
        setErrorClass('auth-page__error-message auth-page__error-message_active');
      }
        return newFormValue;
    })
    
  }, [])

  function handleSubmitClick(e) {
    e.preventDefault();
      const { name, email, password } = formValue;
      register(name, email, password)
        .then(res => {
          navigate('/signin', { replace: true });
          setErrorClass('auth-page__error-message');
        })
        .then(() => {
          authorize(email, password)
            .then(data => {
              if(data.token) {
                // setFormValue({
                //   email: '',
                //   password: '',
                // })
                context.setIsLoggedIn(true);
                navigate('/vacancy-search', {replace: true});
                setErrorClass('auth-page__error-message');
              } else {
                setErrorClass('auth-page__error-message auth-page__error-message_active');
              }
            })
        })
        .catch(e => {
          setErrorClass('auth-page__error-message auth-page__error-message_active');
          console.log(e)
        })
  }

  return (
    <AuthPage 
      texts={REGISTER_TEXTS}
      handleSubmitClick={handleSubmitClick} 
      errorClass={errorClass}
      isButtonDisabled={isButtonDisabled}
      errorText={errorText}
    >
      <AuthInput 
        value={formValue.name}
        onChange={handleChange}
        name='name' 
        title='Имя' 
        type='text'
        min={6}
        max={24} 
      />
      <AuthInput 
        value={formValue.email}
        onChange={handleChange}
        name='email' 
        title='E-mail' 
        type='email'
        min={6}
        max={24} 
      />
      <AuthInput 
        value={formValue.password}
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

export default Register