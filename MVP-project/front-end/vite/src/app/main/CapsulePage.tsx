import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

type Capsule = {
  id: string;
  name: string;
  unlock_date: string;
  message: string;
  user_id: number;
  create_date: string;
};

export default function CapsulePage() {
  const { id } = useParams();
  const [capsule, setCapsule] = useState<Capsule | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/capsule/${id}`)
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.detail || "Loading capsule failed");
          });
        }
        return response.json();
      })
      .then((data) => {
        setCapsule(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, [id]);

  if (error) {
    return <div className="text-red-500 text-center mt-10">Error: {error}</div>;
  }

  if (!capsule) {
    return <div className="text-center mt-10">Loading capsule...</div>;
  }

  const isLocked = new Date(capsule.unlock_date) > new Date();

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="w-[400px] bg-white/10 p-6 rounded-xl shadow-lg text-white items-center">
        <h1 className="text-2xl font-bold mb-4">🔮 Capsule: {capsule.name}</h1>
        <p><strong>Create date:</strong> {new Date(capsule.create_date).toLocaleDateString()}</p>
        <p><strong>Opening date:</strong> {new Date(capsule.unlock_date).toLocaleString()}</p>
        <div className="mt-6">
          <strong>Message:</strong>
          <div className="mt-2 text-gray-700">
            {isLocked ? (
              <em>The message will be available after this date: {new Date(capsule.unlock_date).toLocaleString()}</em>
            ) : (
              <p>{capsule.message}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
