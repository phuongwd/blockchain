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
    <Paper>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Data</TableCell>
            <TableCell>Value</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>{'Hash'}</TableCell>
            <TableCell className={'mono'}>{block.hash.slice(0, 7)}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>{'Hash prev.'}</TableCell>
            <TableCell className={'mono'}>{block.hash_prev.slice(0, 7)}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>{'Num transactions'}</TableCell>
            <TableCell>{block.transactions.length}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>{'Difficulty'}</TableCell>
            <TableCell>{block.difficulty}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>{'Nonce'}</TableCell>
            <TableCell>{block.nonce}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>{'Merkkle root'}</TableCell>
            <TableCell className={'mono'}>{block.merkle_root.slice(0, 7)}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Paper>
  )
}

export default TableOfBlock
