import React from 'react'
import pageMiddleware from '../lib/page_middleware'

import Transaction from '../components/Transaction'


const TransactionsPage = ({ transactions }) => {
  return (
    <div className='container'>
      <div className='row'>
        <h1 className='col text-center'>
          Transactions
        </h1>
      </div>

      {
        transactions.map((transaction, i) => (
          <div key={i} className='row col-sm-12 p-2'>
            <Transaction transaction={transaction}/>
          </div>
        ))
      }

    </div>
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

