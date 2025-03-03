import { useEffect, useState } from "react";
import { getMyCapsules } from "../app/service/Service.ts";

interface Capsule {
  id: number;
  name: string;
  create_date: string; // Исправил created_at → create_date
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
    <div>
      <h1>Мои капсулы</h1>
      {capsules.length > 0 ? (
        <ul>
          {capsules.map((capsule) => (
            <li key={capsule.id}>
              {capsule.name} - {formatDate(capsule.create_date)}
            </li>
          ))}
        </ul>
      ) : (
        <p>Нет капсул</p>
      )}
    </div>
  );
};

export default MyCapsules;
