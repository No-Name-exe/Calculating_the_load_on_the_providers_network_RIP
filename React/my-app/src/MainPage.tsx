import React from 'react';
import HeadRouter from './HeadRouter';
import { DatabaseAdress } from './CONSTANTS';
import RouterLogo from '/Router.svg';
import magnifier from '/magnifier.svg';
import './Router.css';
import * as DummyData from "./mocks"
import * as Api from './api.ts';
import type * as Interfaces from './interfaces.ts';
import { BreadCrumbs } from "./BreadCrumbs.tsx";
import { ROUTES, ROUTE_LABELS } from "./ROUTES.tsx";

const fallbackImage = '/Modem-Failure-Error.png';

interface RouterData {
  id: number | string;
  title: string;
  desc: string;
  img: string;
}

// Предположим, что данные получаем через props или API
interface MainPageProps {
  routers: RouterData[];
  requestCount: number;
  requestApp: number;
  requestData: string; // значение из формы поиска
}

const MainPage: React.FC<MainPageProps> = ({ requestCount=DummyData.ICON_MOCK.routers_count, requestApp=DummyData.ICON_MOCK.id_application, requestData='' }) => {

  const [search, setSearch] = React.useState<string>('');
  const [routers, setRouters] = React.useState<Interfaces.RouterResult[]>(DummyData.ROUTERS_MOCK);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  };

  const handleSearchSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('seacrch нажат')
    try {
      const result = await Api.getRouters(search);
      setRouters(result);
    } catch (error) {
      console.error('Ошибка при получении роутеров:', error);
      // Можно оставить старый список или сбросить
    }
    
    // здесь можно реализовать отправку формы или навигацию
  };

    React.useEffect(() => {

        Api.getRouters()
          .then((result) => {
            console.log(result)
            setRouters(result);
          })
    }, []);

  return (
    <div>
      <BreadCrumbs crumbs={[{ label: ROUTE_LABELS.ROUTERS }]} />
      {/* Шапка */}
      <HeadRouter />

      {/* Информационный блок о запросах */}
      <div
        className="requests"
        style={{ display: routers.length === 0 ? 'none' : 'block' }}
      >
        <span className="circle">
          <span className="requests_number">{requestCount}</span>
        </span>
        <a
          className="Link"
          href={`/application_router/${requestApp}`}
        >
          <img
            src={`${DatabaseAdress}list.svg`}
            className="requests"
            alt="Requests"
            onError={(e) => {
              e.currentTarget.src = "/list.svg";
            }}
          />
        </a>
      </div>

      {/* Заголовок */}
      <h2 className="bigtitle">Список маршрутизаторов</h2>

      {/* Поиск */}
      <div className="grid" style={{ marginTop: 40 }}>
        <form
          onSubmit={handleSearchSubmit}
        >
          {/* CSRF токен можно вставлять через специальный механизм */}
          {/* здесь предполагается, что CSRF реализовано или отключено */}
          <div className="text-input">
            <input
              name="search"
              type="text"
              className="text-input"
              placeholder="Поиск Маршрутизатора"
              value={search}
              onChange={handleSearchChange}
            />
            <button type="submit" className="search">
              <img
                src={magnifier}
                alt="Поиск"
                width={20}
                height={20}
              />
            </button>
          </div>
        </form>
      </div>

      {/* Контент с маршрутизаторами */}
      <div id="meteo_grid" className="content">
        {routers.length > 0 ? (
          routers.map((RouterData) => (
            <span className="block" key={RouterData.id}>
              <a
                href={`/router/${RouterData.id}`}
                className="list"
              >
                <img
                  className="image"
                  src={`${DatabaseAdress}${RouterData.img}`}
                  width={104}
                  height={88}
                  alt={RouterData.title}
                  onError={(e) => {
                    e.currentTarget.src = fallbackImage;
                  }}
                />
                <span className="title">{RouterData.title}</span>
                <span className="desc">{RouterData.desc}</span>
              </a>
              {/* Форма добавления маршрутизатора */}
              <form method="post" action={`/router/add/${RouterData.id}`}>
                {/* В React лучше обрабатывать через fetch/axios, но по вашему примеру */}
                {/* CSRF токен нужно вставить так или так */}
                <input
                  type="hidden"
                  name="router_id"
                  value={RouterData.id}
                  className="Deeper"
                />
                <input
                  type="submit"
                  value="Добавить"
                  className="Deeper"
                />
              </form>
            </span>
          ))
        ) : (
          <p>Список пуст</p>
        )}
      </div>
    </div>
  );
};

export default MainPage;