import React from 'react'
import { Table } from 'reactstrap'


const KeyValueTable = ({ fields, header }) => {
  return (
    <Table hover bordered size="sm">
      <thead>
        {
          header &&
          <tr>
            <th className={'table-cell-key'}>{'Name'}</th>
            <th className={'table-cell-value'}>{'Value'}</th>
          </tr>
        }
      </thead>
      <tbody>
        {
          fields.map((field, i) => (
            <tr key={i}>
              <td className={'table-cell-key'}>{field.key}</td>
              <td className={'table-cell-value'}>{field.value}</td>
            </tr>
          ))
        }
      </tbody>
    </Table>
  )
}

export default KeyValueTable
