import React from 'react';
// import portfolioImagePath from '../../images/portfolio_image.png';
import './AboutProject.css'

const AboutProject = () => {
  return (
    <section id='about-project' className='about-project'>
      <h2 className='about-project__header'>О проекте</h2>
      <div className='about-project__content'>
        <h3 className='about-project__name'>JobHub</h3>
        <p className='about-project__description'>Поиск работы для студентов МГТУ им. Н.Э. Баумана</p>
        <p className='about-project__story'>
        Добро пожаловать на наш сайт, посвященный поиску работы для студентов и выпускников МГТУ им. Н. Э. Баумана!
        </p>
        <p className='about-project__story'>
          <span className='about-project__story_bold-text'>Цель проекта</span>: Создание удобной и эффективной платформы, которая связывает студентов и выпускников нашего университета с ведущими работодателями, предлагающими стажировки и рабочие места.
        </p>
        <h4 className='about-project__subtitle'>Кому это интересно:</h4>
        <ul className='about-project__list'>
          <li className='about-project__story'>
          <span className='about-project__story_bold-text'>Студентам и выпускникам</span>: Возможность найти первую работу или стажировку, соответствующую их навыкам и амбициям.
          </li>
          <li className='about-project__story'>
          <span className='about-project__story_bold-text'>Работодателям</span>: Шанс найти талантливых молодых специалистов из одного из ведущих технических вузов страны.
          </li>
        </ul>
        <a 
          href='https://github.com/ArtyomKuteynikov/ProjectDC' 
          target="_blank" 
          rel="noreferrer" 
          className='about-project__link'
        >Github</a>
      </div>
    </section>
  )
}

export default AboutProject;