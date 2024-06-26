import { Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';


import './App.css';

import { AppContext } from '../../contexts/AppContext';

function App() {
  let isLoggedInInitially = false;
  if (localStorage.getItem("jwt")) {
    isLoggedInInitially = true;
  }
  const [isLoggedIn, setIsLoggedIn] = useState(true);


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

            </main>
            <Footer />
          </>
        } />
      </Routes>
    </div>
    </AppContext.Provider>
  );
}

export default App;
