import { Link } from "react-router-dom"


export function Navigation() {
  return (
    <nav className="bg-blue-600  shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4 w-full ">
            <h1>Perfumes</h1>
            <div className="hidden md:flex space-x-6">
                <Link to="/Home" className="text-white hover:text-gray-200">Home</Link>
                <br/>
                <Link to="/Menu" className="text-white hover:text-gray-200">Menu</Link>
                <br/>
                <Link to="/AboutUs" className="text-white hover:text-gray-200">About Us</Link>
            </div>
        </div>
      </div>
    </nav>
  )
}