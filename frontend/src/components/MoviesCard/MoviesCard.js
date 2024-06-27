import React from 'react';
import './MoviesCard.css';

const MoviesCard = ({ movie, title, duration, imagePath, isSavedCards, savedImagePath }) => {
  // const context = useContext(AppContext);
  // const [isFavourite, setIsFavourite] = useState(false);


  // const { savedMovieList, setSavedMovieList } = context;
  // const { setIsVisiblePreloader } = context;
  // useEffect(() => {
  //   // проверка на то, есть ли в массиве лайкнутых этот фильм
  //   setIsFavourite(savedMovieList.find((savedMovie) => savedMovie.movieId === movie.id || savedMovie.movieId === movie.movieId ))
  //   // первое для вкладки movies, второе для вкладки saved-movies
  // }, [movie.id, movie.movieId, savedMovieList]);


  // function addToFavourites() {
  //   setIsVisiblePreloader(true)
  //   addToSavedMovies(movie)
  //     .then(() => {
  //       setIsFavourite(true);
  //     })
  //     .finally(() => {
  //       setIsVisiblePreloader(false)
  //     })
  // }

  // function deleteFromFavourites() {
  //   setIsVisiblePreloader(true)

  //   if (!isSavedCards) {
  //     getSavedMovies()
  //       .then(savedMovies => {
  //         movie._id = savedMovies.find(film => film.movieId === movie.id)._id;
  //         removeFromFavourites(movie._id)
  //           .then(() => {
  //             setIsFavourite(false)
  //             setSavedMovieList(savedMovieList.filter((item) => item._id !== movie._id));
  //           })
  //       })
  //       .finally(() => {
  //         setIsVisiblePreloader(false)
  //       })
  //   } else {
  //     removeFromFavourites(movie._id)
  //       .then(() => {
  //         setIsFavourite(false)
  //         setSavedMovieList(savedMovieList.filter((item) => item._id !== movie._id));
  //       })
  //       .finally(() => {
  //         setIsVisiblePreloader(false)
  //       })
  //   }
  // }

  return (
    <li className='card'>
      <a href={movie.trailerLink} target='_blank' rel="noreferrer" className='card__link'>
      <img alt={title} src={imagePath} className='card__image'/>
      <div className='card__text'>
        <h2 className='card__title'>{title}</h2>
        <p className='card__duration'>{duration}</p>
      </div>
      </a>
      {/* {
        isSavedCards && (<button type='button' className='card__delete-button' onClick={ deleteFromFavourites }></button>)
      }{
      !isFavourite ? (<>
          <button type='button' className='card__save-button' onClick={ addToFavourites }>Сохранить</button>
          <div className='card__saved-icon'></div>
        </>)
        : (!isSavedCards && <>
          <button type='button' className='card__saved-button' onClick={ deleteFromFavourites }></button>
        </>)
      } */}
    </li>
  )
}

export default MoviesCard