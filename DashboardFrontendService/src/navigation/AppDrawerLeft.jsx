import {Drawer, Toolbar , Divider, List, ListItem, ListItemButton, ListItemText, Typography} from "@mui/material";
import { Link } from "react-router-dom";

const AppDrawerLeft = () => {
    const drawerWidth = 150;

    return (
    <>
        <Drawer
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            },
          }}
          variant="permanent"
          anchor="left"
        >
          <Toolbar />
          <Divider />
          <List>
            {['Отчеты', 'Графики'].map((text, index) => (
              <ListItem key={text} disablePadding component={Link} to={index === 0 ? '/reports' : '/charts'}>
                <ListItemButton>
                <ListItemText><Typography color="primary">{text}</Typography></ListItemText>
                </ListItemButton>
              </ListItem>
            ))}
          </List>
          <Divider />
          <List>
            {['Datascience'].map((text, index) => (
              <ListItem key={text} disablePadding component={Link} to="/datascience">
                <ListItemButton>
                  {/* <ListItemText primary={text} /> */}
                  <ListItemText><Typography color="primary">{text}</Typography></ListItemText>
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Drawer>
    </>
    );
}

export default AppDrawerLeft    