import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './app/main/home';
import Register from './app/main/register';
import LoginPage from './app/main/login';
import CapsuleStorage from './app/main/capsule-storage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register/>} />
        <Route path="/login" element={<LoginPage/>} />
        <Route path='/capsule-storage' element={<CapsuleStorage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
