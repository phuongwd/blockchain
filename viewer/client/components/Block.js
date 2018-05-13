import React from 'react'

import KeyValueTable from './KeyValueTable'


const Block = ({ block }) => {

  const fields = [
    {
      key: 'Hash',
      value: block.hash.slice(0, 7),
    },
    {
      key: 'Hash prev.',
      value: block.hash_prev.slice(0, 7),
    },
    {
      key: 'Num. transactions',
      value: block.transactions.length || 0,
    },
    {
      key: 'Difficulty',
      value: block.difficulty,
    },
    {
      key: 'Nonce',
      value: block.nonce,
    },
    {
      key: 'Merkle root',
      value: block.merkle_root.slice(0, 7),
    },
  ]


  return <KeyValueTable fields={fields} header={true}/>
}

export default Block
