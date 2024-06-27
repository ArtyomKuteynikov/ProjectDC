import React from 'react';
import './FindEmployer.css';
import { NavLink } from 'react-router-dom';

const FindEmployer = () => {
  return (
    <section id='find-employer' className='find-employer'>
      <h2 className='place-vacancy__header'>Найти работодателя</h2>
      <div className='place-vacancy__description'>
        <h3 className='place-vacancy__subtitle'>Почему стоит выбрать нас?</h3>
        <div><p className='place-vacancy__text'>
          <span className='place-vacancy__bold-text'>Широкий выбор вакансий</span>: Регулярно обновляемые предложения.
        </p>
        <p className='place-vacancy__text'>
          <br/><span className='place-vacancy__bold-text'>Удобный поиск</span>: Простые фильтры для быстрого нахождения нужных вакансий.
        </p>
        <p className='place-vacancy__text'>
          <br/><span className='place-vacancy__bold-text'>Целевая аудитория</span>: Вакансии для студентов и выпускников МГТУ им. Н. Э. Баумана.
        </p>
        </div>
        <h3 className='place-vacancy__subtitle'>Как это работает?</h3>
        <div>
        <p className='place-vacancy__text'>
          1. Создайте профиль.
        </p>
        <p className='place-vacancy__text'>
          <br/>2. Найдите вакансии по своим критериям.
        </p>
        <p className='place-vacancy__text'>
          <br/>3. Откликайтесь на интересующие предложения.
        </p>
        </div>
      </div>
      <div className="place-vacancy__button-area">
        <NavLink to="/vacancy-search" className="place-vacancy__sign-button place-vacancy__sign-button_type_signin">Начать карьеру ➤</NavLink>
      </div>
    </section>
  );
}

export default FindEmployer