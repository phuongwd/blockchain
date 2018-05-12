import React from 'react'
import pageMiddleware from '../lib/page_middleware'

import TableOfTransactions from '../components/TableOfTransactions'


const TransactionsPage = ({ transactions }) => {
  return (
    <>
      <h1>
        Transactions
      </h1>

      <TableOfTransactions transactions={transactions}/>
    </>
  )
}

const mapStateToProps = state => ({
  ...state,
})

const mapDispatchToProps = dispatch => {
  return {}
}

export default pageMiddleware(TransactionsPage, {
  mapStateToProps,
  mapDispatchToProps,
})

