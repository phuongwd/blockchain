import React from 'react'

import KeyValueTable from './KeyValueTable'


const Transaction = ({ transaction }) => {
  const fields = [
    {
      key: 'Hash',
      value: transaction.hash.slice(0, 7),
    },
    {
      key: 'Extra nonce',
      value: transaction.extra_nonce,
    },
    {
      key: 'Num. inputs',
      value: transaction.inputs.length || 0,
    },
    {
      key: 'Num. outputs',
      value: transaction.outputs.length || 0,
    },
  ]


  return <KeyValueTable fields={fields}/>
}

export default Transaction
