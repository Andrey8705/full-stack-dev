import React from 'react';
import { Link } from 'react-router-dom';


const HeroSection = () => {
  return (
    <section
      style={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background:
          'radial-gradient(circle, rgba(63,94,251,1) 0%, rgba(252,70,107,1) 100%)',
      }}
    >
        <img
        src="src/assets/logo.png"
        alt="Logo"
        style={{
            width: '350px',
            height: 'auto',
            marginBottom: '20px',
        }}
        />    
        <h1 style={{ fontSize: '4rem', margin: 0, textShadow: '0 0 20px #00ffff' }}>
            Time Capsule
        </h1>
        <p style={{ fontSize: '1.5rem', margin: '20px 0' }}>
    Keep the moment, let time reveal it.
      </p>
      <Link to="/register">
      <button
        style={{
          padding: '15px 30px',
          fontSize: '1.2rem',
          borderRadius: '50px',
          border: 'none',
          cursor: 'pointer',
          background: 'linear-gradient(90deg, #ff8a00, #da1b60)',
          color: '#fff',
          textShadow: '0 0 5px rgba(0,0,0,0.5)',
        }}
      >
        Get Started
      </button>
      </Link>
    </section>
  );
};

export default HeroSection;
