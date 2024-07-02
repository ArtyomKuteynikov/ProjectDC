import React from 'react';
import './MoviesCardList.css'
import MoviesCard from '../MoviesCard/MoviesCard';

const MoviesCardList = ({ films, isSavedCards }) => {

  const normalizeDuration = duration => !Math.floor(duration/60) 
    ? `${duration%60}м` 
    : `${Math.floor(duration/60)}ч ${duration%60}м`
  
    
  return (
    <div className='card-container'>
      <ul className='card-container__list'>
        {films.map(film => (
          <MoviesCard 
            movie={film}
            key={film.nameRU}
            title={film.nameRU} 
            duration={normalizeDuration(film.duration)} 
            imagePath={!isSavedCards ? `https://api.nomoreparties.co/${film.image.url}` : film.image} 
            isSavedCards={isSavedCards}
            description={film.description}
          />
        ))}
      </ul>
    </div>
  )
}

export default MoviesCardList