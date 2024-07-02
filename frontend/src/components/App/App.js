import { Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';
import Navigation from '../Navigation/Navigation'
import Main from '../Main/Main'
import Login from '../Login/Login';
import Register from '../Register/Register';
import Profile from '../Profile/Profile';
import Movies from '../Movies/Movies'

import PageNotFound from '../PageNotFound/PageNotFound'

import ProtectedRouteElement from '../ProtectedRoute/ProtectedRoute'


import { checkToken } from '../../utils/MainApi';
import './App.css';

import { AppContext } from '../../contexts/AppContext';

function App() {
  let isLoggedInInitially = false;
  if (localStorage.getItem("jwt")) {
    isLoggedInInitially = true;
  }

  // FIXME: isLoggedInInitially instead of boolean
  const [isLoggedIn, setIsLoggedIn] = useState(true);

  const [userData, setUserData] = useState({
    name: '',
    email: '',
  });

  function tokenCheck() {
    const jwt = localStorage.getItem('jwt');
    if(jwt) {
      checkToken(jwt)
        .then(res => {
          if (res) {
            const userData = { name: res.name, email: res.email };
            setIsLoggedIn(true);
            setUserData(userData);
            // navigate('/', { replace: true });
          }
        })
    }
  }

  useEffect(() => {
    tokenCheck();
  }, [isLoggedIn])

  const [isNavigationOpen, setIsNavigationOpen] = useState(false);
  function handleCloseNavigationClick() {
    setIsNavigationOpen(false);
  }
  function handleOpenNavigationClick() {
    setIsNavigationOpen(true);
  }

  const [isVisiblePreloader, setIsVisiblePreloader] = useState(false); 

  return (
    <AppContext.Provider value={{
      isLoggedIn,
      userData, 
      isVisiblePreloader,
      setIsLoggedIn,
      setUserData, 
      setIsVisiblePreloader,
     }}>
    <div className="App">
      <Routes>
        <Route path="/" element={
          <>
            <Header 
              handleNavigationClick={handleOpenNavigationClick}
            />
            <main>
              <Navigation 
                isOpen={isNavigationOpen}
                handleCloseClick={handleCloseNavigationClick}
              />
              <Main />
            </main>
            <Footer />
          </>
        } />
        <Route path="/vacancy-search" element={
          <>
            <Header 
              handleNavigationClick={handleOpenNavigationClick}
            />
            <main>
              <Navigation 
                isOpen={isNavigationOpen}
                handleCloseClick={handleCloseNavigationClick}
              />
              {/* <Movies /> */}
              <ProtectedRouteElement element={Movies} />
            </main>
            <Footer />
          </>
        } />
        <Route path="/profile" element={
          <>
            <Header 
              handleNavigationClick={handleOpenNavigationClick}
            />
            <main>
              <Navigation 
                isOpen={isNavigationOpen}
                handleCloseClick={handleCloseNavigationClick}
              />
              <ProtectedRouteElement element={Profile} />
              {/* <Profile /> */}
            </main>
            
          </>
        } />
        <Route path="/signin" element={<Login />} />
        <Route path="/signup" element={<Register />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </div>
    </AppContext.Provider>
  );
}

export default App;
