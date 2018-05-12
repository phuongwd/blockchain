import React from 'react'

import {
  Paper,
  Table,
  TableBody,
  TableRow,
  TableCell,
  TableHead,
} from 'material-ui'


const TableOfBlock = ({ block }) => {
  return (
    <Paper className={''}>
      <Table className={''}>
        <TableHead>
          <TableRow>
            <TableCell>Data</TableCell>
            <TableCell>Value</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell numeric>{'Version'}</TableCell>
            <TableCell numeric>{block.version}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell numeric>{'Num transactions'}</TableCell>
            <TableCell numeric>{block.transactions.length}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Paper>
  )
}

export default TableOfBlock
