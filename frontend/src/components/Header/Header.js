import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';

import './Header.css'

import logoPath from '../../images/logo.svg';
import { AppContext } from '../../contexts/AppContext';

const Header = ({ handleNavigationClick }) => {
  const context = useContext(AppContext);
  
  return (
    <header className='header'>
      <NavLink to="/" className='header__logo'>
        <img alt='логотип' src={logoPath} />
      </NavLink>

      {context.isLoggedIn  && (
        <div className='header__navigation'>
          <NavLink to="/vacancy-search" className="header__navigation-link">Поиск вакансий</NavLink>
          <NavLink to="/responses" className="header__navigation-link">Отклики</NavLink>
        </div>
      )}
      
      {
        context.isLoggedIn 
        ? <NavLink to="/profile" className="header__account-button">Аккаунт</NavLink>
        : (
          <div className='header__sign-buttons'>
            <NavLink to="/signup" className="header__sign-button">Регистрация</NavLink>
            <NavLink to="/signin" className="header__sign-button header__sign-button_type_signin">Войти</NavLink>
          </div>
        )
      }

      {
        context.isLoggedIn  && (
          <button 
            type='button'
            onClick={handleNavigationClick}
            className='header__navigation-button'
          ></button>
        )
      }
      

    </header>
  )
}

export default Header;