import { useState, useEffect } from "react";
import { CirclePlus, User, Sparkles, Menu, LogOut } from "lucide-react";
import { Link } from "react-router-dom";
import { authFetch } from "@/app/service/AuthFetch";
 // путь к компоненту

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [user, setUser] = useState<{ avatar_url: string; email: string } | null>(null);

  useEffect(() => {
  const fetchUser = async () => {
    try {
      const res = await authFetch("http://localhost:8000/api/me");
      const data = await res.json();

      if (data.avatar_url && data.avatar_url.startsWith("/")) {
        data.avatar_url = `http://localhost:8000${data.avatar_url}`;
      }

      setUser(data);
    } catch (err) {
      console.error("Ошибка загрузки пользователя", err);
    }
  };

    fetchUser();
  }, []);

  const menuItems = [
    { name: "Create capsule", icon: <CirclePlus />, path: "/CreateCapsule" },
    { name: "Profile", icon: <User />, path: "/profile" },
    { name: "My capsules", icon: <Sparkles />, path: "/My-Capsules" },
  ];

  return (
    <div className={`h-screen bg-gray-900 z-10 text-white ${isCollapsed ? "w-14 sm:w-16" : "w-48 sm:w-64"} fixed left-0 top-0 transition-all duration-300 p-4 flex flex-col`}>
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 flex items-center justify-center"
      >
        <Menu size={24} />
      </button>
    
      {user && (
        <div className="mt-5 flex items-center space-x-4 p-2">
          {user.avatar_url ? (
            <img
              src={user.avatar_url}
              alt="avatar"
              className={`object-cover border border-white shadow-md rounded-full w-12 h-12 mt-5 ${isCollapsed ? "hidden" : "block"}`}
            />
          ) : null}
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
