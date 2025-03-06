import { Typography, Paper } from '@mui/material';
import StockPredsGrid from '../grids/stockPredsGrid';
import StockPredsDaysGrid from '../grids/stockPredsDaysGrid';


const StockPredsPage = () => {

    return (
        <>
            <Typography sx={{mt: 10}} variant='h2' color="primary" >Прогнозирование закупок</Typography>

            {/* <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Отчет по типу клиентов</Typography>
                <AgentsTypeGrid></AgentsTypeGrid>
            </Paper> */}

            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Сводбная таблица по всем товарам</Typography>
                <StockPredsGrid></StockPredsGrid>
            </Paper>

            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Товары закончатся через 7 дней</Typography>
                <StockPredsDaysGrid days={7}></StockPredsDaysGrid>
            </Paper>

            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Товары закончатся через 30 дней</Typography>
                <StockPredsDaysGrid days={30}></StockPredsDaysGrid>
            </Paper>

            <Paper elevation={2} sx={{p:1, m:1, marginBottom:3}}>
                <Typography variant="h5" color="primary" gutterBottom sx={{paddingTop: 3, paddingBottom: 1}}>Товары закончатся через 60 дней</Typography>
                <StockPredsDaysGrid days={60}></StockPredsDaysGrid>
            </Paper>

        
        </>
    );
}

export default StockPredsPage;
        

        
        

        
        
        
