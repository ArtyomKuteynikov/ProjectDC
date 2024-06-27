import React, { useContext, useEffect, useState } from 'react'
import SearchForm from '../SearchForm/SearchForm';
import MoviesCardList from '../MoviesCardList/MoviesCardList';

import './Movies.css'
import { getFilms } from '../../utils/MoviesApi';
import Preloader from '../Preloader/Preloader'
import { AppContext } from '../../contexts/AppContext';


const Movies = ({ windowWidth }) => {
  const SHORT_DURATION = 60; // FIXME: delete it

  const addButtonParams = { // >769px
    first: 6,
    additional: 3,
  }
  let foundFilms = []
  if (JSON.parse(localStorage.getItem("foundFilms"))) {
    foundFilms = JSON.parse(localStorage.getItem("foundFilms")).slice(0, addButtonParams.first) 
  }

  let initialIsShort = false;
  if (localStorage.getItem('isShort') === 'true') {
    initialIsShort = true;
  }

  const [movies, setMovies] = useState(JSON.parse(localStorage.getItem("foundFilms")) || []);
  const [inputValue, setInputValue] = useState(localStorage.getItem('inputValue') || '');
  const [isShort, setIsShort] = useState(initialIsShort || false);
  const [visibleMovies, setVisibleMovies] = useState(foundFilms);
  const [isMoviesNotFound, setIsMoviesNotFound] = useState(false);
  const [isEmptySearch, setIsEmptySearch] = useState(false);
  const [isErrorSearch, setIsErrorSearch] = useState(false);

  const [visibleFilmsNumber, setVisibleFilmsNumber] = useState(visibleMovies.length)

  const { isVisiblePreloader, setIsVisiblePreloader } = useContext(AppContext);

  useEffect(() => {
    setVisibleFilmsNumber(addButtonParams.first)
  }, [windowWidth, addButtonParams.first])

  useEffect(() => {
    setVisibleMovies(movies.slice(0, visibleFilmsNumber))
  }, [movies, visibleFilmsNumber])

  function handleSubmit(evt) {
    evt.preventDefault();
    setIsVisiblePreloader(true);
    setVisibleMovies([])
    localStorage.setItem('inputValue', inputValue);
    getFilms()
      .then(films => {
        setVisibleFilmsNumber(prev => addButtonParams.first);  // depending on the screen size
        if(!inputValue) {
          setVisibleMovies([])
          setIsEmptySearch(true)
          setIsMoviesNotFound(false)
          setIsErrorSearch(false)
        } else {
          const foundFilms = films.filter(film => {
            if (film.nameRU.toLowerCase().search(inputValue.toLowerCase()) === -1
              && film.nameEN.toLowerCase().search(inputValue.toLowerCase()) === -1
            ) {
              return false;
            }
            if (isShort && film.duration > SHORT_DURATION) {
              return false
            }
            return true;
          });
          if (foundFilms.length === 0) {
            setIsMoviesNotFound(true)
            setVisibleMovies([])
          } else {
            setIsMoviesNotFound(false)
          }
          setIsEmptySearch(false)
          setIsErrorSearch(false)
          setMovies(foundFilms)
          localStorage.setItem("foundFilms", JSON.stringify(foundFilms));
        }
      })
      .catch((err) => {
        console.log(err)
        setVisibleMovies([])
        setIsErrorSearch(true)
      })
      .finally(() => setIsVisiblePreloader(false))
  }

  function addVisibleFilms() {
    setVisibleFilmsNumber(prev => prev + addButtonParams.additional) // depending on screen size
    setVisibleMovies(movies.slice(0, visibleFilmsNumber)) 
  }  

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  }

  const handleCheckboxChange = (e) => {
    e.preventDefault();
    setIsVisiblePreloader(true);
    setIsShort((prev) => {
      localStorage.setItem('isShort', e.target.checked);
      setVisibleMovies([])
      localStorage.setItem('inputValue', inputValue);
      getFilms()
        .then(films => {
          setVisibleFilmsNumber(prev => addButtonParams.first);  // depending on the screen size
          if(!inputValue) {
            setVisibleMovies([])
            setIsEmptySearch(true)
            setIsMoviesNotFound(false)
            setIsErrorSearch(false)
          } else {
            const foundFilms = films.filter(film => {
              if (film.nameRU.toLowerCase().search(inputValue.toLowerCase()) === -1
                && film.nameEN.toLowerCase().search(inputValue.toLowerCase()) === -1
              ) {
                return false;
              }
              if (!prev && film.duration > SHORT_DURATION) {
                return false
              }
              return true;
            });
            if (foundFilms.length === 0) {
              setIsMoviesNotFound(true)
              setVisibleMovies([])
            } else {
              setIsMoviesNotFound(false)
            }
            setIsEmptySearch(false)
            setIsErrorSearch(false)
            setMovies(foundFilms)
            localStorage.setItem("foundFilms", JSON.stringify(foundFilms));
          }
        })
        .catch((err) => {
          console.log(err)
          setVisibleMovies([])
          setIsErrorSearch(true)
        })
        .finally(() => setIsVisiblePreloader(false))
        return e.target.checked;
    })
  }

  return (
    <div className='movies'>
      <SearchForm
        handleSubmit={handleSubmit} 
        inputValue={inputValue} 
        onInputChange={handleInputChange}
        isShort={isShort}
        onCheckboxChange={handleCheckboxChange}  
      />
      <Preloader isVisible={isVisiblePreloader} />
      <MoviesCardList films={visibleMovies} isSavedCards={false} />
      {isEmptySearch && <span className='movies__not-found'>Нужно ввести ключевое слово</span>}
      {isErrorSearch && <span className='movies__not-found'>Во время запроса произошла ошибка. Возможно, проблема с соединением или сервер недоступен. Подождите немного и попробуйте ещё раз</span>}
      {isMoviesNotFound && <span className='movies__not-found'>Ничего не найдено</span>}
      {!isVisiblePreloader 
        && !isEmptySearch
        && !isErrorSearch
        && !isMoviesNotFound 
        && visibleFilmsNumber < movies.length
        && movies.length !== 0
        && <button type="button" className='movies__button' onClick={addVisibleFilms}>Ещё</button>}
    </div>
  )
}

export default Movies