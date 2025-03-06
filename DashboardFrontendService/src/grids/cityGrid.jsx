import React, { useState, useEffect } from 'react';
import { DataGrid, GridToolbar  } from '@mui/x-data-grid';
import { Box, Typography } from '@mui/material';

const CityGrid = () => {
    const [columns, setColumns] = useState([]);
    const [rows, setRows] = useState([]);
    const url = `api/react_data/city_grid`;

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.length > 0) {
            // Генерируем массив колонок из ключей первого объекта
                const cols = Object.keys(data[0]).map(key => ({
                    field: key,
                    headerName: key,
                    width: 150,
                }));
                
                setColumns(cols);
                setRows(data.map((row, index) => ({ id: index, ...row })));
            }
        };
    fetchData();}, []);

  return (
    <Box sx={{ 
        height: 350, 
        width: '100%',  
    }}>
        <DataGrid
            rows={rows}
            columns={columns}
            pageSize={5}
            slots={{ toolbar: GridToolbar }}
            density='compact'
            pageSizeOptions={[10, 25, 50, 100]}
            checkboxSelection
            />
    </Box>
  );
}

export default CityGrid;
