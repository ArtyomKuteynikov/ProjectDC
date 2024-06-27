import React from 'react';
import './NavTab.css'

const NavTab = () => {
  return (
    <nav>
      <ul className='navtab'>
        <li className='navtab__list-item'>
          <a href='#place-vacancy' className='navtab__link'>Разместить вакансию</a>
        </li>
        <li className='navtab__list-item'>
          <a href='#find-employer' className='navtab__link'>Найти работодателя</a>
        </li>
        <li className='navtab__list-item'>
          <a href='#about-project' className='navtab__link'>О проекте</a>
        </li>
      </ul>
    </nav>
  )
}

export default NavTab