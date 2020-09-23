import React from 'react'
import Nav from './Nav'
import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="border-b p-3 flex justify-between items-center">
      <span className="font-bold">
        <Link 
          to='/'
        >
          k8-traffic-generator
        </Link>
      </span>
      <Nav />
    </header>
  )
}

export default Header
