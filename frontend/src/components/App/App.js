import { Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';
import Navigation from '../Navigation/Navigation'
import Main from '../Main/Main'
import Login from '../Login/Login';
import Register from '../Register/Register';
import Profile from '../Profile/Profile';

import ProtectedRouteElement from '../ProtectedRoute/ProtectedRoute'


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

  return (
    <AppContext.Provider value={{
      isLoggedIn,
      userData, 
      setIsLoggedIn,
      setUserData, 
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
      </Routes>
    </div>
    </AppContext.Provider>
  );
}

export default App;
