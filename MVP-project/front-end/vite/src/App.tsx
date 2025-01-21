import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './app/main/home';
import Register from './app/main/register';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register/>} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
