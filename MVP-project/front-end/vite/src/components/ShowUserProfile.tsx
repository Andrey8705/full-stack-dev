import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import { FileUploader } from '@/components/FileUpload';
import { authFetch } from '@/app/service/AuthFetch';
import { API_BASE_URL } from '@/app/service/AuthFetch';

interface UserProfile {
  name: string;
  email: string;
  role: string;
  avatar: string;
}

const ShowUserProfile: React.FC = () => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUserData = async () => {
    try {
      const response = await authFetch('http://127.0.0.1:8000/api/me', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (!response.ok) throw new Error('Ошибка при получении данных');

      const data: UserProfile = await response.json();
      setUser(data);
    } catch (error) {
      console.error(error);
      toast.error('Не удалось загрузить данные пользователя');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUserData();
  }, []);

  const handleAvatarUpload = async (files: File[]) => {
    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const response = await fetch("http://localhost:8000/api/upload-avatar", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: formData,
      });

      if (!response.ok) throw new Error("Ошибка при загрузке файла");

      const result = await response.json();
      toast.success("Аватар обновлён!");
      setUser((prev) => prev ? { ...prev, avatar: result.avatar_url } : prev);
    } catch (error) {
      console.error(error);
      toast.error("Не удалось загрузить аватар");
    }
    
  };

  if (loading) return <p className="text-center py-10">Loading data...</p>;
  if (!user) return <p className="text-center text-red-500">Profile loading error</p>;

  return (
    <div className="w-[400px] bg-white/10 p-6 rounded-xl shadow-lg text-white">
      <h2 className="text-3xl font-bold text-[#f5deb3] text-center mb-4">Your profile</h2>

      {user.avatar && (
        <div className="flex justify-center mb-4">
          <img
            src={`http://localhost:8000${user.avatar}`}
            alt="Avatar"
            className="w-24 h-24 rounded-full object-cover border border-white shadow-md"
          />
        </div>
      )}

      <p><span className="font-medium text-gray-400">Name:</span> {user.name}</p>
      <p><span className="font-medium text-gray-400">Email:</span> {user.email}</p>
      <p><span className="font-medium text-gray-400">Role:</span> {user.role}</p>

      <div className="mt-6">
      <FileUploader
        label="Upload your avatar"
        accept={['image/*']}
        maxFiles={1}
        multiple={false}
        uploadUrl={`${API_BASE_URL}upload-avatar`}
        capsuleId={1} // Provide a valid capsuleId value
        onUploadSuccess={(result: { avatar_url: string }) => {
          toast.success("Аватар обновлён!");
          setUser((prev) => prev ? { ...prev, avatar: result.avatar_url } : prev);
        }}
      />
      </div>
    </div>
  );
};

export default ShowUserProfile;
