import React from 'react'

import {
  Paper,
  Table,
  TableBody,
  TableRow,
  TableCell,
  TableHead,
} from 'material-ui'


const TableOfNodes = ({ nodes }) => {
  return (
    <Paper className={''}>
      <Table className={''}>
        <TableHead>
          <TableRow>
            <TableCell>Hostname</TableCell>
            <TableCell numeric>Port</TableCell>
            <TableCell numeric>Address</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {
            nodes.map((node, i) => {
              return (
                <TableRow key={i}>
                  <TableCell>{node.host}</TableCell>
                  <TableCell numeric>{node.port}</TableCell>
                  <TableCell numeric>{node.address.slice(0, 7)}</TableCell>
                </TableRow>
              )
            })}
        </TableBody>
      </Table>
    </Paper>
  )
}

export default TableOfNodes
