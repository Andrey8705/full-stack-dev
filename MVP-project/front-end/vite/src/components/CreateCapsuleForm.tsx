import { useState } from "react";
import { authFetch } from "@/app/service/AuthFetch";
import { FileUploader } from "@/components/FileUpload"; // Путь к компоненту загрузки файлов

const CreateCapsuleForm = () => {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [unlock_date, setUnlockDate] = useState("");
  const [capsuleId, setCapsuleId] = useState<number | null>(null); // ID капсулы
  const [isModalOpen, setIsModalOpen] = useState(false); // Состояние для модального окна
  const [showFileUploadModal, setShowFileUploadModal] = useState(false); // Состояние для показа загрузки файлов

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newCapsule = { name, message, unlock_date, createdAt: new Date().toISOString() };

    // Отправка данных на сервер для создания капсулы
    const response = await authFetch("http://127.0.0.1:8000/api/capsule/create-capsule/", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      body: JSON.stringify(newCapsule),
    });

    if (response.ok) {
      const data = await response.json();
      const newCapsuleId = data.id; // Получаем ID капсулы
      setCapsuleId(newCapsuleId);
      alert("Капсула времени создана!");
      setName("");
      setMessage("");
      setUnlockDate("");
      setIsModalOpen(true); // Открыть модальное окно после создания капсулы
    } else if (response.status === 422) {
      alert("The capsule opening date cannot be less than the current date.");
    }
  };

  const closeModal = () => {
    setIsModalOpen(false); // Закрыть модальное окно
    setShowFileUploadModal(false); // Закрыть окно загрузки файлов
  };

  return (
    <div className="flex flex-col items-center mt-10">
      <h1 className="text-3xl font-bold text-[#f5deb3]">Create Capsule</h1>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col w-[57vh] bg-[url('/public/logo.png')] bg-center bg-size bg-no-repeat items-center gap-4 mt-5 rounded-full p-6 border border-[#f5deb3] from-gray-900 to-black opacity-90 text-[#ffe4c4] shadow-lg"
      >
        {/* Title Input */}
        <input
          type="text"
          placeholder="Title"
          className="w-40 p-3 rounded-t-3xl bg-[#f5deb3cf] text-black text-center placeholder-black focus:ring-2 focus:ring-[#f5deb3] outline-none transition-all"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        {/* Message Input */}
        <textarea
          placeholder="Message"
          className="w-60 h-28 p-3 rounded-xl bg-[#f5deb3cf] text-black text-center placeholder-black focus:ring-2 focus:ring-[#f5deb3] outline-none transition-all resize-none"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
        />

        {/* Date Picker */}
        <h2 className="text-lg text-black bg-white font-semibold">Unlock Date</h2>
        <input
          type="date"
          className="w-60 p-3 rounded-xl bg-[#f5deb3cf] text-black text-center placeholder-black focus:ring-2 focus:ring-[#f5deb3] outline-none transition-all"
          value={unlock_date}
          onChange={(e) => setUnlockDate(e.target.value)}
          required
        />

        {/* Submit Button */}
        <button
          type="submit"
          className="w-28 p-3 rounded-b-3xl bg-[#f5deb3] text-black font-semibold uppercase tracking-wide hover:bg-[#ffe4c4] transition-all shadow-md"
        >
          Create Capsule
        </button>
      </form>

      {/* Модальное окно для загрузки файлов */}
      {isModalOpen && (
        <div className="fixed inset-0 flex justify-center items-center bg-gray-900 bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl mb-4">Add files to your capsule?</h2>

            {/* Загрузка файлов */}
            {showFileUploadModal && capsuleId !== null && (
              <FileUploader
                label="Upload files"
                accept={['image/*', 'application/pdf']}
                uploadUrl={`http://127.0.0.1:8000/api/capsule/${capsuleId}/upload/`} // Передаем URL с ID капсулы
                maxFiles={5}
                multiple={true}
                onUploadSuccess={(result: { filename: string }) => {
                  console.log("File uploaded successfully", result);
                  closeModal(); // Закрываем модальное окно после успешной загрузки
                }}
                capsuleId={capsuleId} // Передаем ID капсулы
              />
            )}

            <div className="mt-4 flex justify-between">
              <button onClick={closeModal} className="px-4 py-2 bg-gray-500 text-white rounded">No, Thanks</button>
              <button onClick={() => setShowFileUploadModal(true)} className="px-4 py-2 bg-blue-500 text-white rounded">Yes, Upload</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CreateCapsuleForm;
