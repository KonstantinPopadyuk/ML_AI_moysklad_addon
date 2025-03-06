import React, { useState, useEffect } from 'react';
import { DataGrid, GridToolbar  } from '@mui/x-data-grid';
import { Box, Typography } from '@mui/material';

const StockPredsDaysGrid = ({ days }) => {
    const [columns, setColumns] = useState([]);
    const [rows, setRows] = useState([]);
    const url = `api/react_data/preds/stock_days/${days}`;

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
                        width: 300,
                        // editable: true,
                        // resizable: true,
                    };
                    
                    if (typeof data[0][key] === 'number') {
                        columnObj.valueFormatter = (params) => {
                            return `${params.toLocaleString()} шт.`; // форматирование числовых значений
                        };
                    } 
                    
                    return columnObj;
                });
                
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
            autosizeOptions={{
                columns: ['name'],
                includeOutliers: true,
                includeHeaders: true,
              }}
            />
    </Box>
  );
}

export default StockPredsDaysGrid;
