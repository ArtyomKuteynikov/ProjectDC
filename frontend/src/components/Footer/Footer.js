import React from 'react';
import './Footer.css'

const Footer = () => {
  return (
    <footer className='footer'>
      <p className='footer__text'>Дипломная работа Цифровой Кафедры МГТУ им. Н.Э. Баумана</p>
      <p className='footer__text'>Артем Кутейников × Тимур Гафаров × Глеб Шилинг × Малик Хаписов</p>
      <div className='footer__info'>
        <span className='footer__year'>© 2024</span>
        <ul className='footer__links'>
          <li className='footer__link-item'>
            <a 
              href='https://dc.bmstu.ru/' 
              target='_blank'
              rel="noreferrer"
              className='footer__link'
            >Цифровая Кафедра</a>
          </li>
          <li className='footer__link-item'>
            <a 
              href='https://github.com/ArtyomKuteynikov/ProjectDC' 
              target='_blank'
              rel="noreferrer"
              className='footer__link'
            >Github</a>
          </li>
        </ul>
      </div>
    </footer>
  )
}

export default Footer