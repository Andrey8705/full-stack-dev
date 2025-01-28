import Footer from "@/components/Footer";
import LoginForm from "@/components/login-form";

const LoginPage = () => {
  return (
        <div className="flex flex-col items-center w-max">
            <LoginForm/>
            <Footer/>
        </div>
    );
};

export default LoginPage;
