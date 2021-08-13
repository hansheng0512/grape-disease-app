import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from "./layouts/dashboard";
import './App.css'

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          {/*<Route path="users/*" element={<Users />} />*/}
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
