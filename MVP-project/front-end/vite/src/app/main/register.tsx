import Footer from '@/components/Footer';
import RegisterForm from '@/components/RegisterForm';

const RegisterPage = () => {
  return (
        <div className="flex  flex-col items-center w-max">
            <RegisterForm />
            <Footer />
        </div>
    );
};

export default RegisterPage;
