import * as React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './app/main/home';
import Register from './app/main/register';
import LoginPage from './app/main/login';
import CapsuleStorageContainer from './app/main/CapsuleStorageContainer';
import CreateCapsule from './app/main/CreateCapsule';
import UserProfile from './app/main/UserProfile';
import CapsulePage from './app/main/CapsulePage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register/>} />
        <Route path="/login" element={<LoginPage/>} />
        <Route path="/My-Capsules" element={<CapsuleStorageContainer />} />
        <Route path="/CreateCapsule" element={<CreateCapsule />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/capsule/:id" element={<CapsulePage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
