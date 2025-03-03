import { useState } from "react";

const CreateCapsuleForm = () => {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [unlock_date, setUnlockDate] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const newCapsule = { name, message, unlock_date, createdAt: new Date().toISOString() };

    // Отправка данных на сервер
    const response = await fetch("http://127.0.0.1:8000/api/capsule/create-capsule/", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      body: JSON.stringify(newCapsule),
    });

    if (response.ok) {
      alert("Капсула времени создана!");
      setName("");
      setMessage("");
      setUnlockDate("");
    }
    else if (response.status === 422) {
      alert("The capsule opening date cannot be less than the current date.");
    }
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
</div>
  );
};

export default CreateCapsuleForm;
