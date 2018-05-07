import React from 'react'
import { Button } from 'material-ui'

import pageMiddleware from '../lib/page_middleware'
import Actions from '../state/actions'

import TableOfNodes from '../components/TableOfNodes'


const Index = ({ refresh, nodes, transactions, blocks }) => {
  return (
    <>
      <h1>
        Hello, Blockchain!
      </h1>

      <TableOfNodes nodes={nodes}/>

      <Button variant={'raised'} color={'secondary'} onClick={refresh}>
        Update
      </Button>
    </>
  )
}

const mapStateToProps = state => ({
  ...state,
})

const mapDispatchToProps = dispatch => {
  return {
    refresh: () => dispatch(Actions.refresh()),
  }
}

export default pageMiddleware(Index, {
  mapStateToProps,
  mapDispatchToProps,
})

