import React from 'react';
import { useNavigate } from 'react-router-dom';

const HeroSection: React.FC = () => {
  const navigate = useNavigate(); // Хук для навигации

  return (
    <section className="flex flex-col items-center justify-center text-white py-20">
      <img
        src="/public/logo.png"
        alt="Logo"
        className="w-[400px] h-auto mb-5"
      />
      <h1 className="text-4xl md:text-6xl font-bold text-cyan-300 drop-shadow-[0_0_20px_rgba(0,255,255,1)]">
        Time Capsule
      </h1>
      <p className="text-lg md:text-xl mt-5 mb-8">
        Keep the moment, let time reveal it.
      </p>
      <button
        onClick={() => navigate('/register')} // Перенаправление на страницу регистрации
        className="px-10 py-4 text-lg font-semibold rounded-full bg-gradient-to-r from-orange-500 to-pink-600 text-white shadow-md transition-all duration-300 hover:from-pink-600 hover:to-orange-500 hover:shadow-lg active:scale-95"
      >
        Get Started
      </button>
    </section>
  );
};

export default HeroSection;
