import { AppBar, Toolbar, Typography } from "@mui/material";

const AppTopBar = () => {
  
  return (
  <>
    <AppBar
    position="fixed"
    sx={{  zIndex: (theme) => theme.zIndex.drawer + 1 }}
    >
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          Giardino Analytics
        </Typography>
      </Toolbar>
    </AppBar>
  </>);
}

export default AppTopBar