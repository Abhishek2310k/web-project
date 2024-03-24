import React from 'react'
import './Footer.scss'
import { FaGithub } from "react-icons/fa";
import { SiLeetcode } from "react-icons/si";
import { SiCodeforces } from "react-icons/si";
import { SiCodechef } from "react-icons/si";




export const Footer = () => {
  return (
    <div className='footer'>
        <div className='content'>
            <div className='madeby'>
                <span>Made By:-</span>
                <h1>Abhishek Kumar</h1>
                <div className='links'>
                    <a href='https://github.com/Abhishek2310k'><FaGithub/></a>
                    <a href='https://leetcode.com/abhishek_0040/'><SiLeetcode/></a>
                    <a href='https://codeforces.com/profile/AbhishekKu_AK47/'><SiCodeforces/></a>
                    <a href='https://www.codechef.com/users/abhishek_2310a'><SiCodechef/></a>
                </div>
            </div>
            <div className='brands'>
                <span>Thanks to:-</span>
                <h1>CiSTUP</h1>
                <h1>Dr. Punit Rathore</h1>
                <h1>RBCCPS, IISc</h1>
            </div>
        </div>
    </div>
  )
}
