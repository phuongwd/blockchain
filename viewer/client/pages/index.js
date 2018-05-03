import React from 'react'

import Layout from '../components/Layout'

import pageMiddleware from '../lib/page_middleware'
import Actions from '../state/actions'

const Index = ({ refresh, nodes, transactions, blocks }) => {
  const onclick = () => {
    refresh()
  }

  return (
    <>
      <Layout>
        <h1>
          Hello, Blockchain!
        </h1>

        <p>
          Bitcoins and stuff...
        </p>

        <p>
          { JSON.stringify(nodes) }
        </p>

        <button onClick={onclick}>
          Send message!
        </button>

      </Layout>
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

