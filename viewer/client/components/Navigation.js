import React from 'react'

import Link from 'next/link'
import { AppBar, Toolbar, Button, Typography, Tabs, Tab } from 'material-ui'
import componentMiddleware from '../lib/component_middleware'

import Actions from '../state/actions'


class Navigation extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }

  render() {
    const { refresh } = this.props

    return (
      <>
        <AppBar position='static'>
          <Toolbar>
            <Typography variant="title" color="inherit">
              Blockchain
            </Typography>

            <Tabs>

              <Link href={'/'}>
                <Tab label="Blocks"/>
              </Link>

              <Link href={'/transactions'}>
                <Tab label="Transactions"/>
              </Link>

              <Link href={'/nodes'}>
                <Tab label="Nodes"/>
              </Link>

            </Tabs>

            <Button variant={'flat'} color={'secondary'} onClick={refresh}>
              Update
            </Button>

          </Toolbar>
        </AppBar>
      </>
    )
  }
}


const mapStateToProps = state => ({
  ...state,
})

const mapDispatchToProps = dispatch => {
  return {
    refresh: () => dispatch(Actions.refresh()),
  }
}

export default componentMiddleware(Navigation, {
  mapStateToProps,
  mapDispatchToProps,
})
