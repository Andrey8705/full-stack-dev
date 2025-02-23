import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white px-4 py-3 sm:py-4 mb-[1vh] border-t-2 mt-4 
      border-cyan-400 rounded-xl text-center w-full text-[0.5rem] sm:text-xs">
      <div>
        <p className="my-1 sm:my-2">
          © {new Date().getFullYear()} OneOfTwins Time Capsule. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
