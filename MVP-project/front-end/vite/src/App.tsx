import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './app/main/home';
import Register from './app/main/register';
import LoginPage from './app/main/login';
import CapsuleStorageContainer from './app/main/CapsuleStorageContainer';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register/>} />
        <Route path="/login" element={<LoginPage/>} />
        <Route path='/capsule-storage' element={<CapsuleStorageContainer />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
