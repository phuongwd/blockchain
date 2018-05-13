import _ from 'lodash'

import React from 'react'
import pageMiddleware from '../lib/page_middleware'
import { Button } from 'reactstrap'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faForward from '@fortawesome/fontawesome-free-solid/faForward'
import faBackward from '@fortawesome/fontawesome-free-solid/faBackward'

import Block from '../components/Block'
import Actions from '../state/actions'
import Transaction from '../components/Transaction'

const Index = ({ blockIdx, blocks, prevBlock, nextBlock }) => {
  let block = null
  const numBlocks = blocks.length
  if(numBlocks > blockIdx) {
    block = blocks[blockIdx]
  }

  if(!block) {
    return (
      <div className='container'>
        <div className='row'>
          <h1 className='col text-center'>
            Block
          </h1>
        </div>

        <div className='row'>
          <h6 className='col text-center'>
            {!block && 'No blocks found. Refresh.'}
          </h6>
        </div>
      </div>
    )
  }

  return (
    <div className='container'>
      <div className='row'>
        <h1 className='col text-center'>
          Block
        </h1>
      </div>

      <div className='row'>
        <h6 className='col text-center'>
          {numBlocks && `${blockIdx + 1}/${numBlocks}`}
        </h6>
      </div>

      <div className='row'>
        <div className='col-sm-2'>
          <Button color='default' onClick={prevBlock} className='fill-parent'>
            <span>
              <FontAwesomeIcon icon={faBackward}/>
              {' Prev'}
            </span>
          </Button>
        </div>

        <div className='col-sm-8'>
          <div className='row'>
            <Block block={block}/>
          </div>
        </div>

        <div className='col-sm-2'>
          <Button color='default' onClick={nextBlock} className='fill-parent'>
            <span>
              <FontAwesomeIcon icon={faForward}/>
              {' Next'}
            </span>
          </Button>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-8 offset-sm-2">
          <div className='row'>
            <h5 className='col text-center'>
              {'Transactions:'}
            </h5>
          </div>

          {
            block && block.transactions &&
            block.transactions.map((transaction, i) => (
              <div key={i} className='row'>
                <Transaction transaction={transaction}/>
              </div>
            ))
          }
        </div>
      </div>
    </div>
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

