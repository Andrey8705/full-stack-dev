import Features from "@/components/Features"
import Footer from "@/components/Footer"
import HeroSection from "@/components/HeroSection"

export default function Home() {
  return (
    
    <div>
        <div className="flex mb-36 flex-col items-center w-max max-w-sm">
            <HeroSection/>
        </div>
        <div className="flex  flex-col items-center w-max max-w-sm">
            <Features/>
        </div>
        <div className="flex  flex-col content-center items-center">
            <Footer/>
        </div>
      
    </div>
  )
}
