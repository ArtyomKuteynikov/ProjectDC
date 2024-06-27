import React from 'react';

import Promo from '../Promo/Promo';
import PlaceVacancy from '../PlaceVacancy/PlaceVacancy';
import FindEmployer from '../FindEmployer/FindEmployer';
import AboutProject from '../AboutProject/AboutProject';
import Portfolio from '../Articles/Articles';

const Main = () => {
  return (
    <>
      <Promo />
      <PlaceVacancy />
      <FindEmployer />
      <AboutProject />
      <Portfolio />
    </>
  )
}

export default Main