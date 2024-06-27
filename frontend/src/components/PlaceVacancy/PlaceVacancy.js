import React from 'react'
import './PlaceVacancy.css'
import { NavLink } from 'react-router-dom'

const PlaceVacancy = () => {
  return (
    <section id='place-vacancy' className='place-vacancy'>
      <h2 className='place-vacancy__header'>Разместить вакансию</h2>
      <div className='place-vacancy__description'>
        <h3 className='place-vacancy__subtitle'>Почему стоит воспользоваться нашим сервисом?</h3>
        <div><p className='place-vacancy__text'>
          <span className='place-vacancy__bold-text'>Квалифицированные кандидаты</span>: Наши студенты и выпускники – одни из лучших в стране.
        </p>
        <p className='place-vacancy__text'>
          <br/><span className='place-vacancy__bold-text'>Целевая аудитория</span>: Ваше объявление увидят именно те, кто вам нужен.
        </p>
        <p className='place-vacancy__text'>
          <br/><span className='place-vacancy__bold-text'>Простота размещения</span>: Быстро и удобно.
        </p>
        </div>
        <h3 className='place-vacancy__subtitle'>Как это работает?</h3>
        <div>
        <p className='place-vacancy__text'>
          1. Зарегистрируйтесь или войдите в свой аккаунт.
        </p>
        <p className='place-vacancy__text'>
          <br/>2. Заполните форму с деталями вакансии.
        </p>
        <p className='place-vacancy__text'>
          <br/>3. Опубликуйте объявление.
        </p>
        </div>
      </div>
      <div className="place-vacancy__button-area">
        <NavLink to="/create-vacancy" className="place-vacancy__sign-button place-vacancy__sign-button_type_signin">Разместить вакансию ➤</NavLink>
      </div>
    </section>
  )
}

export default PlaceVacancy