import React from 'react'
import RouterLogo from '/Router.svg'
import './Router.css'
import HeaderRouter from './HeadRouter.tsx'
import { Helmet } from 'react-helmet';

function PageMainRouter() {
  const [count, setCount] = React.useState(0)

  return (
	<>
	<HeaderRouter />
	  <div>
		<a href="/routers">
			<h1>Роутеры для расчета нагрузки</h1>
		</a>
	  </div>
	</>
  )
}

export default PageMainRouter