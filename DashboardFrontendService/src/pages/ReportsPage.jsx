import { Typography, Box, Button, ButtonGroup, Paper, Drawer, Toolbar, Divider, List, ListItem, ListItemButton, ListItemText, ListItemIcon, AppBar} from '@mui/material';
import AgentsTypeGrid from '../grids/agentsTypeGrid';
import AgentsNameGrid from '../grids/agentsNameGrid';
import ItemTypeGrid from '../grids/itemTypeGrid';
import VolumeTypeGrid from '../grids/volumesTypeGrid';
import CityGrid from '../grids/cityGrid';

const ReportsPage = () => {

    return (
        <>
            <Paper elevation={0} sx={{p:1, marginTop: 8}}>
                <ButtonGroup variant="outlined" aria-label="Basic button group">
                <Button>Today</Button>
                <Button>Yesterday</Button>
                <Button>Week</Button>
                <Button>Month</Button>
                <Button>Year</Button>
                </ButtonGroup>
            </Paper>

            <Paper elevation={0} sx={{display:'flex'}}>
                
                <Paper elevation={2} sx={{p:1, m:1, width: '25%', height: 100}}>
                    <Typography variant="h6" gutterBottom>Выручка: 100к рублей (+10%)</Typography>
                </Paper>
                <Paper elevation={2} sx={{p:1, m:1, width: '25%', height: 100}}>
                    <Typography variant="h6" gutterBottom>Продажи: 55 заказов (+30%)</Typography>
                </Paper>
                <Paper elevation={2} sx={{p:1, m:1, width: '25%', height: 100}}>
                    <Typography variant="h6" gutterBottom>Средний чек: 9.800 рублей(+3%)</Typography>
                </Paper>
                <Paper elevation={2} sx={{p:1, m:1, width: '25%', height: 100}}>
                    <Typography variant="h6" gutterBottom>Еще какая-то важная цифра (-1%)</Typography>
                </Paper>
                
            </Paper>

            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Отчет по типу клиентов</Typography>
                <AgentsTypeGrid></AgentsTypeGrid>
            </Paper>
            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Отчет клиентам</Typography> 
                <AgentsNameGrid></AgentsNameGrid>
            </Paper>
            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Отчет типу товара</Typography>
                <ItemTypeGrid></ItemTypeGrid>
            </Paper>
            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Отчет по объемам товаров</Typography>
                <VolumeTypeGrid></VolumeTypeGrid>
            </Paper>
                <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Отчет по городам</Typography>
                <CityGrid></CityGrid>
            </Paper>

        
        </>
    );
}

export default ReportsPage;
        

        
        

        
        
        
