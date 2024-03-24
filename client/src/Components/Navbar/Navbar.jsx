import React, { useState } from 'react'
import './Navbar.scss'
import { TiThMenu } from "react-icons/ti";

const Navbar = () => {

  const [hidden,setHidden] = useState(true);
  return (
    <div className='navbar'>
      <div className='content'>
        <h1>CiSTUP</h1>
        <div className='anchors'>
          <a href='#form'>Form</a>
          <a href='#images'>Images</a>
          <a href='#result_content'>Result</a>
        </div>
        <div className='menu'>
          <TiThMenu style={{fontSize:"20px"}} onClick={()=>setHidden(!hidden)}/>
          <div className={hidden === true ? "hidden" : "anchors2"}>
            <a href='#form'>Form</a>
            <a href='#images'>Images</a>
            <a href='#result_content'>Result</a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Navbar