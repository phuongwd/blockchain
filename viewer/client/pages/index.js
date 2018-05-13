import _ from 'lodash'

import React from 'react'
import pageMiddleware from '../lib/page_middleware'

import TableOfBlock from '../components/TableOfBlock'
import { Button } from 'material-ui'
import Actions from '../state/actions'


const Index = ({ blockIdx, blocks, prevBlock, nextBlock }) => {

  let block = null
  if(blocks.length > blockIdx) {
    block = blocks[blockIdx]
  }

  return (
    <>
      <h1>
        Blocks
      </h1>

      <h3>
        {`current: ${blockIdx + 1}`}
      </h3>

      <h3>
        {`total: ${blocks.length || 0}`}
      </h3>

      <Button variant={'raised'} color={'primary'} onClick={prevBlock}>
        {'<- Previous'}
      </Button>

      <Button variant={'raised'} color={'primary'} onClick={nextBlock}>
        {'Next -> '}
      </Button>

      {block && <TableOfBlock block={block}/>}
    </>
  )
}

Index.getInitialProps = ({ query }) => {
  const blockIdx = _.get(query, 'block', 0)
  return { blockIdx }
}


const mapStateToProps = state => ({
  ...state,
})

const mapDispatchToProps = dispatch => {
  return {
    prevBlock: () => dispatch(Actions.prevBlock()),
    nextBlock: () => dispatch(Actions.nextBlock()),
    setBlock: (blockIdx) => dispatch(Actions.setBlock(blockIdx)),
  }
}

export default pageMiddleware(Index, {
  mapStateToProps,
  mapDispatchToProps,
})

