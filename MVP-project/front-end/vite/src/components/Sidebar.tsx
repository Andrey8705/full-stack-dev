import { useState } from "react";
import { CirclePlus, User, Settings, Menu, LogOut } from "lucide-react";

import { Link, useHref } from "react-router-dom";

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const menuItems = [
    { name: "Create capsule", icon: <CirclePlus />, path: "/CreateCapsule" },
    { name: "Profile", icon: <User />, path: "/profile" },
    { name: "My capsules", icon: <Settings />, path: "/settings" },
  ];

  return (
    <div className={`h-screen bg-gray-900 text-white ${isCollapsed ? "w-16" : "w-64"} fixed left-0 top-0 transition-all duration-300 p-4 flex flex-col`}> 
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 flex items-center justify-center"
      >
        <Menu size={24} />
      </button>
      <nav className="mt-10 flex-1">
        {menuItems.map((item, index) => (
          <Link
            key={index}
            to={item.path}
            className="flex items-center space-x-4 p-2 rounded-lg hover:bg-gray-700 transition-all"
          >
            {item.icon}
            {!isCollapsed && <span>{item.name}</span>}
          </Link>
        ))}
      </nav>
      <div className="mt-auto">
        <button className="flex items-center space-x-4 p-2 rounded-lg bg-red-500 hover:bg-red-400 w-full">
          <LogOut />
          {!isCollapsed && <span>Logout</span>}
        </button>
      </div>
    </div>
  );
};

export default Sidebar;