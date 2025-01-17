import React from 'react';

const Features = () => {
  const features = [
    { id: 1, title: 'Making Time Capsules', description: 'Create time capsules with personal messages, photos, and videos.' },
    { id: 2, title: 'Setting the timer on the capsule', description: 'Set a date and time for the capsule to open at any future event.' },
    { id: 3, title: 'Secure access', description: 'A unique link sent by email, messengers or other communication channels.' },
  ];

  return (
    <section
      style={{
        padding: '50px 20px',
        textAlign: 'center',
        background: '#111',
      }}
    >
      <h2 style={{ fontSize: '2.5rem', marginBottom: '20px' }}>Features</h2>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
        {features.map((feature) => (
          <div
            key={feature.id}
            style={{
              background: '#1c1c1e',
              padding: '20px',
              borderRadius: '10px',
              width: '300px',
              boxShadow: '0 0 15px rgba(0, 255, 255, 0.3)',
            }}
          >
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Features;
