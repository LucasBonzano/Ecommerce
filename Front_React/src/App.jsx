import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Navigation } from './Components/Navbar';
import { Toaster } from 'react-hot-toast';
import { Home } from './Pages/Home';
import { Menu } from './Pages/Menu';
import { AboutUs } from './Pages/AboutUs';
import './index.css';

function App(){
  return(
      <BrowserRouter>
      <Navigation/>
      <Routes>
        <Route path="/Home" element={<Home/>}/>
        <Route path="/Menu" element={<Menu/>}/>
        <Route path="/AboutUs" element={<AboutUs/>}/>
      </Routes>
      <Toaster/>
      </BrowserRouter>
  )
}


export default App;