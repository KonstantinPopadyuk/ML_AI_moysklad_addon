import React, { useState } from 'react';
import { ResponsiveBar } from '@nivo/bar';
import { Box, FormControl, InputLabel, MenuItem, Select } from '@mui/material';

const ClientTypeBarChart = ({ data }) => {

    const [parametr, setParametr] = useState('orders_total_sum');

    const handleChange = (event) => {
        setParametr(event.target.value);
    };

    return (
        <Box sx={{height:400, display: 'flex', flexDirection:'column' }}>
            <Box sx={{ width: 180, height: 50}}>
                <FormControl variant="standard" size='small' sx={{ m: 1, minWidth: 120}}>
                    <InputLabel sx={{ color: 'primary'}}>Parametr</InputLabel>
                    <Select
                    value={parametr}
                    label="Parametr"
                    onChange={handleChange}
                    >
                    <MenuItem value="orders_count">Заказано позиций</MenuItem>
                    <MenuItem value="item_mean_price">Средняя цена товара</MenuItem>
                    <MenuItem value="order_mean_sum">Средний чек</MenuItem>
                    <MenuItem value="orders_total_sum">Общая сумма заказов</MenuItem>
                    </Select>
                </FormControl>
            </Box>
            <ResponsiveBar
                data={data}
                keys={[parametr]} // Используем выбранное значение
                indexBy="id"
                margin={{ top: -20, right: 50, bottom: 50, left: 100 }}
                padding={0.3}
                layout="horizontal"
                colors={{ scheme: 'category10' }}
                borderColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
                labelTextColor='white'//{{ from: 'color', modifiers: [['darker', 1.6]] }} // Изменяем цвет подписей данных на барах
                axisTop={null}
                axisRight={null}
                axisBottom={{
                    tickValues: 5,
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: parametr,
                    legendPosition: 'middle',
                    legendOffset: 32,
                }}
            />
        </Box>
    );
};

export default ClientTypeBarChart;
