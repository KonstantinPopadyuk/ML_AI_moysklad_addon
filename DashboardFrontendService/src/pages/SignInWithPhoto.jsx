import * as React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import {Avatar, Button, CssBaseline, TextField, FormControlLabel, Checkbox, Paper, Box, Grid, Typography} from '@mui/material/';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { createTheme, ThemeProvider } from '@mui/material/styles';



const defaultTheme = createTheme();


export default function SignInSide( { setIsAuthenticated } ) {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  
  const navigate = useNavigate();

  useEffect(() => {
      if (setIsAuthenticated.isAuthenticated) {
        console.log('we think, that auth true, probably should rerender')
        navigate("/reports");
      }
    }, [setIsAuthenticated.isAuthenticated]);


  const handleSubmit = (event) => {
    event.preventDefault();

    if (!login || !password) {
      setError(true);
    }

    const data = new FormData(event.currentTarget);
    const user_login = data.get('login')
    const user_pass = data.get('password')

    const formDetails = {
      'username': user_login,
      'password': user_pass,
    };

    const url = `/api/auth/token`;

    const fetchData = async () => {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'accept': 'application/json', 
                  'Content-Type': 'application/json'},
        body: JSON.stringify(formDetails),
      });
      const data = await response.json();
      
      if (data['error'] != "Invalid credentials") { 
        localStorage.setItem('token', data['access_token'])
        setIsAuthenticated.setIsAuthenticated(true);
        navigate("/reports"); }
      else {
        localStorage.setItem('token', 0)
        setIsAuthenticated.setIsAuthenticated(false);
        setError(true);
        setLogin("")
        setPassword("")
        navigate("/auth")
      }
    };

    fetchData()

  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Grid container component="main" sx={{ height: '100vh' }}>
        <CssBaseline />
        <Grid item xs={false} sm={4} md={7}
          sx={{
            backgroundImage: 'url(https://avatars.mds.yandex.net/get-altay/7754763/2a00000183a87bdd7db822bcc3926aee3c68/XXXL)',
            backgroundRepeat: 'no-repeat',
            backgroundColor: (t) =>
              t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}/>
          
        <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
          <Box sx={{my: 8, mx: 4, display: 'flex', flexDirection: 'column', alignItems: 'center',}}>
          
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}> <LockOutlinedIcon /></Avatar>
            <Typography component="h1" variant="h5">Giardino Analytics</Typography>              

            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>

              <TextField margin="normal" required fullWidth id="login" name="login" autoFocus label="Login" autoComplete="login"
                      error={error && !login}
                      onChange={(e) => setLogin(e.target.value)}
                      value={login}
                      helperText={error && !login && "Enter login"}
                      />
              <TextField margin="normal" required fullWidth name="password" id="password" type="password" label="Password" autoComplete="current-password"
                      error={error && !password}
                      onChange={(e) => setPassword(e.target.value)}
                      value={password}
                      helperText={error && !password && "Enter password"}
                      />

              <FormControlLabel control={<Checkbox value="remember" color="primary" />} label="Remember me"/>

              <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>Sign In</Button>

              {error && !login && !password && <p style={{ color: "red" }}>You have entered an invalid username or password. Please try again.</p>}

            </Box>
            <Typography component="h1" variant="h5">{}</Typography>
          </Box>
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}