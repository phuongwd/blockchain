import React from 'react'
import pageMiddleware from '../lib/page_middleware'

import TableOfNodes from '../components/TableOfNodes'


const NodesPage = ({ nodes }) => {
  return (
    <div className='container'>
      <div className='row'>
        <h1 className='col text-center'>
          Transactions
        </h1>
      </div>

      <TableOfNodes nodes={nodes}/>
    </div>
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

