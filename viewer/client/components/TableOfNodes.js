import React from 'react'
import { Table } from 'reactstrap'


const TableOfNodes = ({ nodes }) => {
  return (
    <Table hover striped bordered size="sm">
      <thead>
        <tr>
          <th className={'table-cell-key'}>{'Hostname'}</th>
          <th className={'table-cell-value'}>{'Port'}</th>
          <th className={'table-cell-value'}>{'Address'}</th>
        </tr>
      </thead>
      <tbody>
        {
          nodes.map((node, i) => (
            <tr key={i}>
              <td className={'table-cell-key'}>{node.host}</td>
              <td className={'table-cell-value'}>{node.port}</td>
              <td className={'table-cell-value'}>{node.address.slice(0, 7)}</td>
            </tr>
          ))
        }
      </tbody>
    </Table>
  )
}

export default TableOfNodes
