import Footer from "@/components/Footer";
import Sidebar from "@/components/Sidebar";

const CapsuleStorageContainer = () => {
    return (
          <div className="flex h-full w-full">
            <div className="flex flex-col w-xs h-full">
                <Sidebar/>
            </div>
            <div className="flex flex-col items-center w-full flex-none h-full">
                <div className="grow"></div>
                <div className="flex-none">
                    <Footer/>
                </div>
            </div>
          </div>
      );
  };
  
  export default CapsuleStorageContainer;
  