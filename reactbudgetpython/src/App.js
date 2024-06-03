import React, { useContext } from 'react';
import { ThemeProvider, ThemeContext } from './contexts/ThemeContext';
import DarkModeToggle from './components/DarkModeToggle';
import LoginPage from './components/LoginPage';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import './App.css';
import UploadFile from './components/UploadFile';
import { Amplify, Auth } from 'aws-amplify';
import amplifyconfig from './amplifyconfiguration.json';
Amplify.configure(amplifyconfig);

const AppContent = () => {
  const { theme } = useContext(ThemeContext);

  return (
    // <div className={`App ${theme}`}>
    //   <header className="App-header">
    //     {/* <h1 className="title"> Dark Mode Toggle Example</h1>
    //     <DarkModeToggle /> */}
    //     <LoginPage />
    //   </header>
    // </div>
    <Router>
      <Routes>
        <Route exact path="/" component={LoginPage} />
        <Route path="/upload" component={UploadFile} />
      </Routes>
    </Router>
  );
};

const App = () => {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
};

export default App;