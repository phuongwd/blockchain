import React from 'react'

import { Link, Router } from '../next.routes'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faSync from '@fortawesome/fontawesome-free-solid/faSync'
import faCube from '@fortawesome/fontawesome-free-solid/faCube'
import faDollarSign from '@fortawesome/fontawesome-free-solid/faDollarSign'
import faStream from '@fortawesome/fontawesome-free-solid/faStream'

import componentMiddleware from '../lib/component_middleware'

import Actions from '../state/actions'
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem, Button,
} from 'reactstrap'


const links = [
  {
    text: 'Blocks',
    href: '/',
    icon: faCube,
  },
  {
    text: 'Transactions',
    href: '/transactions',
    icon: faDollarSign,
  },
  {
    text: 'Nodes',
    href: '/nodes',
    icon: faStream,
  },
]

class Navigation extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      activeTab: 0,
    }
  }

  toggleTab = (tab) => {
    console.log(tab)
    if(this.state.activeTab !== tab) {
      this.setState({
        activeTab: tab,
      })
      Router.pushRoute(links[tab].href)
    }
  }

  render() {
    const { activeTab } = this.state
    const { refresh } = this.props

    return (
      <>
        <Navbar expand='sm'>
          <NavbarBrand href='/'>
            <img className={''} src={'/static/img/bitcoin.png'}/>
          </NavbarBrand>
          <NavbarToggler onClick={this.toggle}/>

          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav pills>
              {
                links.map((link, i) => (
                  <NavItem key={i}>
                    <NavLink
                      href={link.href}
                      active={activeTab === i}
                      onClick={(e) => {
                        e.preventDefault()
                        this.toggleTab(i)
                      }}>
                      <span>
                        <FontAwesomeIcon icon={link.icon}/>
                        {` ${link.text}`}
                      </span>
                    </NavLink>
                  </NavItem>
                ))
              }
            </Nav>
          </Collapse>
          <Nav>
            <Button color="info" onClick={refresh}>
              <FontAwesomeIcon icon={faSync}/>
            </Button>
          </Nav>
        </Navbar>
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
