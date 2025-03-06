import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Routes, Navigate, useNavigate } from 'react-router-dom';
import { Typography, Box, Divider} from '@mui/material';

import AppTopBar from './navigation/AppTopBar';
import AppDrawerLeft from './navigation/AppDrawerLeft';
import ReportsPage from './pages/ReportsPage';
import StockPredsPage from './pages/StockPredsPage';
import SignInSide from './pages/SignInWithPhoto';
import PlotsPage from './pages/PlotsPage';



const PrivateRoute = ({ element, isAuthenticated }) => {
  return isAuthenticated ? element : <><Navigate to="/auth" /></>;
}

const App = () => {
  console.log('On app top')
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  useEffect(() => {
    if (localStorage.getItem('token') && localStorage.getItem('token') !== null) {
      const token = localStorage.getItem('token');
      fetch('api/auth/validate_token', {
          method: 'GET',
          headers: {
              'Authorization': `Bearer ${token}`
          }
      })
      .then(response => {
          if (response.ok) {
              setIsAuthenticated(true);
          } else {
              setIsAuthenticated(false);

          }
      })
      .catch(error => {
          setIsAuthenticated(false);
      });
    } else {
      setIsAuthenticated(false);
    }
  }, []); 


  return (
    <BrowserRouter>
      <Routes>
        <Route path='/auth' element={<SignInSide setIsAuthenticated={{isAuthenticated , setIsAuthenticated}} />}></Route>


        <Route path='/*' element={
          <PrivateRoute isAuthenticated={isAuthenticated} element={
              <>             
                <Box sx={{ display: 'flex'}}>
                    <AppTopBar />
                    <AppDrawerLeft />
                    <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', width: '90%' }}>
                      <Routes>
                        <Route path='/reports' element={<ReportsPage/>}></Route>
                        <Route path='/charts' element={<PlotsPage></PlotsPage>}></Route>
                        <Route path='/datascience' element={<StockPredsPage/>}></Route>
                        <Route path='/*' element={<>
                          <Typography sx={{ mt: 10 }}   variant="h5" style={{ wordWrap: "break-word" }}>Hello mr. Anderson</Typography>
                          <Typography sx={{ mt: 1 }}   variant="h5" style={{ wordWrap: "break-word" }}>Matrix has you</Typography>
                          <Divider />
                          <Typography sx={{ mt: 4 }}   variant="h6" style={{ wordWrap: "break-word" }}>Probably here is no available content, please try another url</Typography>
                        </>}></Route>
                      </Routes>
                    </Box>
                </Box>  
               </>
            }></PrivateRoute>
        }></Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;
