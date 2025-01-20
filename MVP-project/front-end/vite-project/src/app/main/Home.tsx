import React from 'react';
import HeroSection from '../../components/HeroSection';
import Features from '../../components/Features';
import Footer from '../../components/Footer';
import { Link } from 'react-router-dom';  // Для переходов между страницами

const Home = () => {
  return (
    <div>
        <HeroSection />
        <Features />
        <Footer />
    </div>
  );
};

export default Home;