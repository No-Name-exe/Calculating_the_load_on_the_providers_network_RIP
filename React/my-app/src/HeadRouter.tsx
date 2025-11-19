import React from 'react';
import { DatabaseAdress } from './CONSTANTS.ts';
import RouterLogo from '/Router.svg'
import './Router.css'


interface HeadRouterProps {
  children?: React.ReactNode; // ReactNode включает любой допустимый элемент React
}

const HeadRouter: React.FC<HeadRouterProps> = ({ children }) => {
  return (
    <div>
	<header className="head">
		<nav className="navbar navbar-expand">
		<div className="container">
			<a href="/">
			<object data={`${DatabaseAdress}router-svgrepo-com.svg`} type="image/svg+xml" className="icon" >
				<img src={RouterLogo} className="icon" alt="Router Icon" />
			</object>
			</a>
		</div>
		</nav>
	</header>
	{/* основной контент */}
	{children}

    </div>
  );
};

export default HeadRouter;