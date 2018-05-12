import React from 'react'
import pageMiddleware from '../lib/page_middleware'

import TableOfBlock from '../components/TableOfBlock'


const Index = ({ blocks }) => {
  console.log(blocks)
  return (
    <>
      <h1>
        Blocks
      </h1>

      {
        blocks.map((block, i) => {
          return (
            <TableOfBlock key={i} block={block}/>
          )
        })
      }
    </>
  )
}

const mapStateToProps = state => ({
  ...state,
})

const mapDispatchToProps = dispatch => {
  return {}
}

export default pageMiddleware(Index, {
  mapStateToProps,
  mapDispatchToProps,
})

