import React from 'react'

import {
  Paper,
  Table,
  TableBody,
  TableRow,
  TableCell,
  TableHead,
} from 'material-ui'


const TableOfTransactions = ({ transactions }) => {
  return (
    <Paper className={''}>
      <Table className={''}>
        <TableHead>
          <TableRow>
            <TableCell>Extra nonce</TableCell>
            <TableCell numeric>Num inputs</TableCell>
            <TableCell numeric>Num outputs</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {
            transactions.map((transaction, i) => {
              return (
                <TableRow key={i}>
                  <TableCell numeric>{transaction.extra_nonce}</TableCell>
                  <TableCell numeric>{transaction.inputs.length}</TableCell>
                  <TableCell numeric>{transaction.outputs.length}</TableCell>
                </TableRow>
              )
            })}
        </TableBody>
      </Table>
    </Paper>
  )
}

export default TableOfTransactions
