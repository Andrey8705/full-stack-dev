import { useEffect, useState } from "react";
import { getMyCapsules } from "../app/service/Service.ts";

interface Capsule {
  id: number;
  name: string;
  create_date: string;
  unlock_date: string;
  message?: string;
}

const MyCapsules = () => {
  const [capsules, setCapsules] = useState<Capsule[]>([]);

  useEffect(() => {
    getMyCapsules().then((data) => {
      setCapsules(data);
    });
  }, []);

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return "Неизвестная дата";

const parsedDate = Date.parse(dateString);
  if (isNaN(parsedDate)) return "Неверный формат даты";

  return new Date(parsedDate).toLocaleDateString();
};

  return (
    <div className="flex flex-col items-center mt-10">
      <h1 className="text-3xl font-bold text-[#f5deb3]">Мои капсулы</h1>
        <div className="flex flex-col w-[57vh] bg-center bg-size bg-no-repeat items-center gap-4 mt-5 rounded-full p-6 from-gray-900 to-black opacity-90 text-[#ffe4c4]">
          {capsules.length > 0 ? (
            <ul className="text-left">
              {capsules.map((capsule) => (
                <li key={capsule.id} className="w-[400px] bg-white/10 p-6 rounded-xl shadow-lg text-white">
                  <h2 className="text-xl font-semibold mb-2">Title: {capsule.name}</h2>
                  <p className="text-gray-300">Created at: {new Date(capsule.create_date).toLocaleDateString()}</p>
                  <p className="text-gray-300">Unlock date: {formatDate(capsule.unlock_date)}</p>
                  {capsule.message && (
        <p className="mt-2 text-lg text-[#ffd700]">Message: {capsule.message}</p>
      )}
                </li>
              ))}
            </ul>
          ) : (
            <p>Нет капсул</p>
          )}
      </div>
    </div>
  );
};

export default MyCapsules;
