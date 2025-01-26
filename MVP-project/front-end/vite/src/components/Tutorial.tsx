import { Button } from "@/components/ui/button"; // Импортируем кнопку из вашего компонента
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useNavigate } from "react-router-dom"; // Для навигации на другую страницу

const Tutorial = () => {
  const navigate = useNavigate(); // Хук для навигации

  const handleCreateCapsule = () => {
    navigate("/create-capsule"); // Перенаправление на страницу создания капсулы
  };

  return (
    <div className="flex justify-center items-center h-screen p-4">
      <img src="/public/logo.png" alt="logo" className="fixed top-auto left-auto opacity-30 -z-5 size-[60%]" />
      <Card className="rounded-xl border bg-black opacity-80 text-[#ffe4c4] shadow max-w-[50%] ">
        <CardHeader>
          <CardTitle className="text-2xl text-center">Welcome to Capsule Tutorial</CardTitle>
        </CardHeader>
        <CardContent>
          <CardDescription className="text-center text-white mb-6">
          This app helps you create and manage time capsules. Each capsule can contain text, images, and other data you want to save for the future. Start creating your capsule today and share your memories with others!
          </CardDescription>
          <div className="flex justify-center">
            <Button onClick={handleCreateCapsule} className="bg-blue-500 text-white w-full">
              Proceed to creating a capsule
            </Button>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl text-center">1.</CardTitle>
        </CardHeader>
      </Card>
    </div>
  );
};

export default Tutorial;
