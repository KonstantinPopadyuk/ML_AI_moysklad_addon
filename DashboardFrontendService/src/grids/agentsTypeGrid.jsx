import React, { useState, useEffect } from 'react';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import { Box, Typography } from '@mui/material';
import ClientTypeBarChart from '../charts/clientTypeNivo';

const AgentsTypeGrid = () => {
    const [columns, setColumns] = useState([]);
    const [rows, setRows] = useState([]);
    const url = `api/react_data/agents_type_grid`;
    const [chartData, setChartData] = useState([]);


    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(url);
            const data = await response.json();

            
            if (data.length > 0) {
            // Генерируем массив колонок из ключей первого объекта
            const cols = Object.keys(data[0]).map(key => {
                let columnObj = {
                    field: key,
                    headerName: key,
                    width: 130,
                    // editable: true,
                    // resizable: true,
                };
                
                if (typeof data[0][key] === 'number') {
                    columnObj.valueFormatter = (params) => {
                        return `${params.toLocaleString()} ₽`; // форматирование значения рублей
                    };
                } 
                if (key === 'orders_count') {
                    columnObj.valueFormatter = (params) => {
                       return params.toLocaleString(); // форматирование числовых значений
                    };
                }

                return columnObj;
            });

                const preparedData = data.map((item) => ({
                    id: item.companyType,
                    orders_total_sum: item.orders_total_sum,
                    orders_count: item.orders_count,
                    item_mean_price: item.item_mean_price,
                    order_mean_sum: item.order_mean_sum
                }));
                setChartData(preparedData);
            
                
                setColumns(cols);
                setRows(data.map((row, index) => ({ id: index, ...row })));
            }

        };
    fetchData();}, []);

  return (
    <Box sx={{ display: 'flex', height:400}}>
        <Box sx={{ 
            height: 400, 
            width: '50%',
            marginRight: '10px', 
            marginBottom: '30px'
        }}>
            <DataGrid
                rows={rows}
                columns={columns}
                pageSize={5}
                checkboxSelection
                slots={{ toolbar: GridToolbar }}
                density='compact'
                pageSizeOptions={[10, 25, 50, 100]}
                />
        </Box>
        <Box sx={{width: '50%', transform: 'translateY(-50px)'}}>
            {chartData.length > 0 && <ClientTypeBarChart data={chartData} />}
        </Box>    
    </Box>
  );
}

export default AgentsTypeGrid;
