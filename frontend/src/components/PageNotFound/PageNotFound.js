import React from 'react'
import { Link } from 'react-router-dom';
import './PageNotFound.css'

const PageNotFound = () => {
  return (
    <main className='page-not-found'>
      <h1 className='page-not-found__number'>404</h1>
      <p className='page-not-found__text'>Страница не найдена</p>
      <Link to='/' className='page-not-found__link'>Назад</Link>
    </main>
  )
}

export default PageNotFound