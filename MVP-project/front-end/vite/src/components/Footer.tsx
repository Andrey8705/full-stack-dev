import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white px-1 mt-12 border-t-2 border-cyan-400 rounded-xl text-center">
      <div>
        <p className="my-2">
          © {new Date().getFullYear()} OneOfTwins Time Capsule. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
