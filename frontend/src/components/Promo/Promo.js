import React from 'react'
import './Promo.css'
import NavTab from '../NavTab/NavTab'

const Promo = () => {
  return (
    <section className='promo'>
      <h1 className='promo__header'>Разместите<br/> вакансию на JobHub</h1>
      <NavTab />
    </section>
  );
}

export default Promo