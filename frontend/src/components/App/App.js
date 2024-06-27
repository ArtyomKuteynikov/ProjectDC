import { Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';
import Navigation from '../Navigation/Navigation'
import Main from '../Main/Main'
import Login from '../Login/Login';
import Register from '../Register/Register';


import './App.css';

import { AppContext } from '../../contexts/AppContext';

function App() {
  let isLoggedInInitially = false;
  if (localStorage.getItem("jwt")) {
    isLoggedInInitially = true;
  }

  // FIXME: isLoggedInInitially instead of boolean
  const [isLoggedIn, setIsLoggedIn] = useState(false);

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
      setIsLoggedIn, 
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
        <Route path="/signin" element={<Login />} />
        <Route path="/signup" element={<Register />} />
      </Routes>
    </div>
    </AppContext.Provider>
  );
}

export default App;
