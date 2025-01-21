import React from 'react';

interface Feature {
  id: number;
  title: string;
  description: string;
}

const Features: React.FC = () => {
  const features: Feature[] = [
    { id: 1, title: 'Making Time Capsules', description: 'Create time capsules with personal messages, photos, and videos.' },
    { id: 2, title: 'Setting the timer on the capsule', description: 'Set a date and time for the capsule to open at any future event.' },
    { id: 3, title: 'Secure access', description: 'A unique link sent by email, messengers or other communication channels.' },
  ];

  return (
    <section className="bg-gray-900 text-wheat py-12 px-4 rounded-xl text-center">
      <h2 className="text-4xl text-[#f5deb3] mb-8">Features</h2>
      <div className="flex justify-center gap-8">
        {features.map((feature) => (
          <div
            key={feature.id}
            className="bg-gray-800 p-6 rounded-xl w-72 shadow-xl hover:shadow-2xl transition-all duration-300"
          >
            <h3 className="text-[#f5deb3] pb-3.5 text-xl">{feature.title}</h3>
            <p className="text-white">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Features;
