import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';

interface UserProfile {
  name: string;
  email: string;
  role: string;
}

const ShowUserProfile: React.FC = () => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/me', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Ошибка при получении данных');
        }

        const data: UserProfile = await response.json();
        setUser(data);
      } catch (error) {
        console.error(error);
        toast.error('Не удалось загрузить данные пользователя');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <p className="text-center py-10">Loading data...</p>;
  }

  if (!user) {
    return <p className="text-center text-red-500">Profile loading error</p>;
  }

  return (
    <div className="w-[400px] bg-white/10 p-6 rounded-xl shadow-lg text-white">
      <h2 className="text-3xl font-bold text-[#f5deb3] text-center">Your profile</h2>
      <div>
        <p><span className="font-medium text-gray-600">Name:</span> {user.name}</p>
        <p><span className="font-medium text-gray-600">Email:</span> {user.email}</p>
        <p><span className="font-medium text-gray-600">Role:</span> {user.role}</p>
      </div>
    </div>
  );
};

export default ShowUserProfile;
