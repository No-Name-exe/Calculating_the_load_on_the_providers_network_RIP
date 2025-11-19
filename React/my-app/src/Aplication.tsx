import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { DatabaseAdress } from './CONSTANTS.ts';
import type * as Interfaces from './interfaces.ts';
import * as Api from './api.ts';
import HeadRouter from './HeadRouter.tsx';
import './Router.css'
import { BreadCrumbs } from './BreadCrumbs.tsx';
import { ROUTE_LABELS } from './ROUTES.tsx';

const fallbackImage = '/Modem-Failure-Error.png';


const ApplicationPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [routers, setRouters] = useState<Interfaces.ListRouterItem[]>([]);
  const [address, setAddress] = useState<string>('');
  const [totalUsers, setTotalUsers] = useState<number | undefined>(undefined);
  
  // Загрузка данных при монтировании компонента
  useEffect(() => {
    Api.getApp(Number(id))
      .then(data => {
        setRouters(data.ListRouter);
        // Можно установить остальные поля, если они есть
        setAddress(data.Adress);
        setTotalUsers(data.TotalUsers);
      })
      .catch(err => console.error('Error fetching data', err));
  }, [id]);

  // Обработчик отправки формы добавления роутера
  const handleAddRouter = (e: React.FormEvent) => {
    e.preventDefault();
    // Отправка данных на сервер
    fetch(`/api/application/${id}/add-router`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ address, totalUsers }), // передайте нужные данные
    }).then(res => {
      if(res.ok) {
        // Обновление списка после добавления
        return res.json();
      }
    }).then(newRouter => {
      setRouters(prev => [...prev, newRouter]);
    }).catch(err => console.error('Error adding router', err));
  };

  const handlePUTAppRouter = (e: React.FormEvent) => {
  e.preventDefault();
  // Предполагая, что у вас есть переменная applicationId
  Api.putAppRouter(Number(id), { Adress: address, TotalUsers: totalUsers })
    .then(newApp => {
      // обновляем список роутеров в состоянии
      // setRouters(prev => [...prev, newRouter]);3
      console.log(newApp)
    })
    .catch(err => {
      console.error('Error adding router', err);
    });
};

  return (
    <div>
      <BreadCrumbs crumbs={[{ label: ROUTE_LABELS.APPROUTER }]} />
      <HeadRouter />
      <h3>Расчет нагрузки</h3>
      
      {/* Форма добавления */}
      <form onSubmit={handlePUTAppRouter}>
        <input
          type="text"
          placeholder="Адрес"
          value={address}
          onChange={e => setAddress(e.target.value)}
        />
        <input
          type="text"
          placeholder="Количество пользователей"
          value={totalUsers}
          onChange={e => setTotalUsers(Number(e.target.value))}
        />
        <button type="submit">Добавить</button>
      </form>
      
      {/* Список роутеров */}
      <ul>
        {routers.length > 0 ? (
          routers.map((router) => (
            <li key={router.id_router}>
              <a href={`/router/${router.id_router}`}>
                <img src={`${DatabaseAdress}${router.Router[0].img}`} width="104" height="88" alt="" onError={(e) => {e.currentTarget.src = fallbackImage;}}/>
                {router.Router[0].title}
              </a>
              <p>{router.Router[0].desc}</p>
              {/* Дополнительные действия: редактировать, удалять */}
            </li>
          ))
        ) : (
          <p>Список пуст</p>
        )}
      </ul>
    </div>
  );
};

export default ApplicationPage;