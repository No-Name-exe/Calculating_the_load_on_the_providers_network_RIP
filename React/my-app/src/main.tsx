import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// import './index.css'
import App from './App.tsx'

import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import React from 'react'
import ReactDOM from 'react-dom/client'

import HeadRouter from './HeadRouter.tsx'
import DescriptionRouter from './DescriptionRouter.tsx'
import AppRouter from './AppRouter.tsx'
import AppRouter2 from './Aplication.tsx'
import PageMainRouter from './PageMainRouter.tsx'
import MainPage from './MainPage.tsx'

import type * as Interfaces from "./interfaces.ts"
import  * as DummyData from "./mocks.ts"


import 'bootstrap/dist/css/bootstrap.min.css'
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';

import { BreadCrumbs } from "./BreadCrumbs.tsx";
import { ROUTES, ROUTE_LABELS } from "./ROUTES.tsx";


const router = createBrowserRouter([
  {
    path: '/',
    element: <PageMainRouter />
  },
  {
    path: '/routers',
    element: <MainPage />
  },
  {
    path: '/application_router/:id',
    element: <AppRouter2 id={3} />
  },
  {
    path: '/router/:id',
    element: <DescriptionRouter />
  },
  {
    path: '/list',
    element: <MainPage 
    // routers={routers}
    // requestCount={requestCount}
    // requestData={requestData}
    />
  }
])

createRoot(document.getElementById('root')!).render(
  // <StrictMode>
  //   <App />
  // </StrictMode>,
  <React.StrictMode>
    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand href="/">Роутеры</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/routers">Список</Nav.Link>
            <Nav.Link href="/application_router/2/">Расчет нагрузки</Nav.Link>
            <NavDropdown title="страницы роутеров" id="basic-nav-dropdown">
              <NavDropdown.Item href="/router/1">роутер компании</NavDropdown.Item>
              <NavDropdown.Item href="/router/2">роутер школы</NavDropdown.Item>
              <NavDropdown.Item href="/router/3">роутера домашний</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>

    

    <RouterProvider router={router} />
  </React.StrictMode>,
)
