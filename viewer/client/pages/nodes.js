import React from 'react'
import pageMiddleware from '../lib/page_middleware'

import TableOfNodes from '../components/TableOfNodes'


const NodesPage = ({ nodes }) => {
  return (
    <>
      <h1>
        Nodes
      </h1>

      <TableOfNodes nodes={nodes}/>
    </>
  )
}

const mapStateToProps = state => ({
  ...state,
})

const mapDispatchToProps = dispatch => {
  return {}
}

export default pageMiddleware(NodesPage, {
  mapStateToProps,
  mapDispatchToProps,
})

