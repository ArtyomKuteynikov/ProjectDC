import React from 'react'
import { NavLink } from 'react-router-dom'
import './Navigation.css'

const Navigation = ({ isOpen, handleCloseClick }) => {

  function checkIsActive(isActive) {
    if (isActive) {
      return 'navigation__link navigation__link_active'
    }
    return 'navigation__link';
  }

  return (
    <section className={
      isOpen
       ? 'navigation'
       : 'navigation navigation_invisible'
    }>
      
      <div className='navigation__background'></div>
      <nav className='navigation__bar'>
        <NavLink to="/" className={({ isActive }) => checkIsActive(isActive)}>Главная</NavLink>
        <NavLink to="/vacancy-search" className={({ isActive }) => checkIsActive(isActive)}>Поиск вакансий</NavLink>
        <NavLink to="/responses" className={({ isActive }) => checkIsActive(isActive)}>Отклики</NavLink>
       
        <NavLink to="/profile" className="navigation__account-button">Аккаунт</NavLink>
          
      </nav>
      <button 
        type='button'
        onClick={handleCloseClick}
        className='navigation__close-button'
      ></button>
    </section>
  )
}

export default Navigation