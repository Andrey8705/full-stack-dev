import { useState, useEffect } from "react";
import { CirclePlus, User, Settings, Menu, LogOut, Laugh } from "lucide-react";
import { Link } from "react-router-dom";

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [user, setUser] = useState<{ avatar: string; email: string } | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      fetch("http://localhost:8000/api/me", {
        method: "GET",
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      })
        .then((res) => res.json())
        .then((data) => setUser(data))
        .catch(() => console.error("Ошибка загрузки пользователя"));
    }
  }, []);

  const menuItems = [
    { name: "Create capsule", icon: <CirclePlus />, path: "/CreateCapsule" },
    { name: "Profile", icon: <User />, path: "/profile" },
    { name: "My capsules", icon: <Settings />, path: "/settings" },
  ];

  return (
    <div className={`h-screen bg-gray-900 text-white ${isCollapsed ? "w-14 sm:w-16" : "w-48 sm:w-64"} fixed left-0 top-0 transition-all duration-300 p-4 flex flex-col`}>
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 flex items-center justify-center"
      >
        <Menu size={24} />
      </button>

      {user && (
        <div className="mt-5 flex items-center space-x-4 p-2">
          <Laugh />
          {!isCollapsed && <span className="text-sm">{user.email}</span>}
        </div>
      )}

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
        <button
          onClick={() => {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("user");
            window.location.href = "/login";
          }}
          className="flex items-center space-x-4 p-2 rounded-lg bg-red-500 hover:bg-red-400 w-full"
        >
          <LogOut />
          {!isCollapsed && <span>Logout</span>}
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
