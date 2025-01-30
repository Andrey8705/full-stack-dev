import CreateCapsuleForm from "@/components/CreateCapsuleForm";
import Footer from "@/components/Footer";
import Sidebar from "@/components/Sidebar";


const CreateCapsule= () => {
  return (
    
    <div className="flex h-full w-full">
    <div className="flex flex-col h-full">
        <Sidebar/>
    </div>
    <div className="flex flex-col w-full items-center flex-none h-full">
      <CreateCapsuleForm/>
        <div className="grow"></div>
        <div className="flex-none">
            <Footer/>
        </div>
    </div>
  </div>
  )
}

export default CreateCapsule