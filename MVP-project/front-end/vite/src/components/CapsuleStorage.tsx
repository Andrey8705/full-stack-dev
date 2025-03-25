import { authFetch } from "@/app/service/AuthFetch";


const CapsuleStorage = async () => {

    await authFetch("http://127.0.0.1:8000/api/capsule/capsules/my", {
      method: "GET",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    });


  return (
    <div className="flex flex-col items-center mt-10">
        <h1 className="text-3xl font-bold text-[#f5deb3]">My capsules</h1>
    </div>
  );
};

export default CapsuleStorage;
