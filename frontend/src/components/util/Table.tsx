import React, { useState } from 'react';


export interface Column<T> {
  header: string;
  accessor: keyof T;
  render?: (row: T) => React.ReactNode;
}
  
interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
  className?: string;
}
  
  
const Table = <T extends object>({ data, columns, className }: TableProps<T>) => {
  const [sortBy, setSortBy] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');

  const handleSort = (accessor: keyof T) => {
    if (sortBy === accessor) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(accessor);
      setSortDirection('asc');
    }
  };

  const sortedData = sortBy
    ? [...data].sort((a, b) => {
        const valueA = a[sortBy];
        const valueB = b[sortBy];
        if (valueA === valueB) return 0;
        return sortDirection === 'asc' ? (valueA > valueB ? 1 : -1) : valueA < valueB ? 1 : -1;
      })
    : data;

  return (
    <div className={`table-container ${className || ''}`}>
      <table className='table'>
        <thead>
          <tr>
            {columns.map((column, index) => (
              <th key={index} onClick={() => column.accessor && handleSort(column.accessor)}>
                {column.header} {sortBy === column.accessor && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, rowIndex) => (
            <tr key={rowIndex} className='table-list-item'>
              {columns.map((column, colIndex) => (
                <td key={colIndex}>
                  {column.render ? column.render(row) : String(row[column.accessor])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;