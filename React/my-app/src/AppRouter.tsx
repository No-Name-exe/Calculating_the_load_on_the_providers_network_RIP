import React from 'react';
import { DatabaseAdress } from './CONSTANTS.ts';
import RouterLogo from '/Router.svg'
import './Router.css'


type DataProps = any;
interface DescriptionRouterProps {
  data?: DataProps; // ReactNode включает любой допустимый элемент React
}

interface RouterData {
  id_router: {
    id: number;
    img: string;
    title: string;
    desc: string;
  };
  router_load?: string;
  master_router_id?: number | null;
}

interface Props {
  id: number;
  address?: string;
  total_users?: number;
  tree: any[]; // структура дерева, уточнить структуру
  data?: {
    routers: RouterData[];
  };
  DatabaseAdress: string;
  // можно добавить функции для API-запросов
}

const ApplicationPage: React.FC<Props> = ({
  id,
  address = '',
  total_users = 0,
  tree,
  data,
  DatabaseAdress,
}) => {
  const [routers, setRouters] = React.useState<RouterData[]>(data?.routers || []);

  // Обработчики форм
  const handleDelete = (applicationId: number) => {
    // здесь вызов API для удаления
  };

  const handleAddRouter = (routerId: number) => {
    // вызов API для добавления или обновления роутера
  };

  const handleAddApplication = (e: React.FormEvent) => {
    e.preventDefault();
    // вызов API для добавления приложения
  };

  // Например, можно загрузить данные при монтировании
  // useEffect(() => {
  //   // fetchData()...
  // }, []);

  return (
    <div>
      {/* Заголовок */}
      <h3 className="bigtitle">Расчет нагрузки</h3>
      
      {/* Удаление заявки */}
      <form onSubmit={(e) => { e.preventDefault(); handleDelete(id); }}>
        <input type="hidden" name="application_id" value={id} />
        <button type="submit" className="Delete">Удалить заявку</button>
      </form>

      {/* Форма добавления роутера */}
      <div className="grid">
        <form onSubmit={handleAddApplication}>
          <input
            name="Adress"
            type="text"
            className="text-input"
            placeholder="Адрес"
            defaultValue={address}
          />
          <input
            name="TotalUsers"
            type="text"
            className="text-input"
            placeholder="Количество пользователей"
            defaultValue={total_users}
          />
          <button type="submit" className="Adder">Добавить</button>
          
          {/* скрытые поля */}
          <input type="hidden" name="application_id" value={id} />
          <input type="hidden" name="update_app" value={String(true)} />

          {/* дерево */}
          <ul className="TreeRender">
            {tree.map((root, index) => (
              <TreeComponent key={index} branch={root} />
            ))}
          </ul>
        </form>
      </div>

      {/* Список роутеров */}
      {routers.length > 0 ? (
        routers.map((order) => (
          <span key={order.id_router.id} className="block-deep">
            <a
              href={`/router_url/${order.id_router.id}`}
              className="list"
            >
              <img
                className="image"
                src={`${DatabaseAdress}${order.id_router.img}`}
                width={104}
                height={88}
                alt="Router Image"
              />
              <span className="title">{order.id_router.title}</span>
            </a>
            <span className="desc-deep">{order.id_router.desc}</span>
            
            {/* Обновление router */}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleAddRouter(order.id_router.id);
              }}
            >
              <input type="hidden" name="application_id" value={id} />
              <input type="hidden" name="router_id" value={order.id_router.id} />
              <input type="hidden" name="update_router" value={String(true)} />
              <button type="submit" className="AdderRouter">
                Обновить
              </button>
            </form>
          </span>
        ))
      ) : (
        <div>Список пуст</div>
      )}
    </div>
  );
};

// Пример компонента для дерева
const TreeComponent: React.FC<{ branch: any }> = ({ branch }) => {
  // Тут можно реализовать рендеринг ветви дерева
  return <li>{/* отображение ветви */}</li>;
};

export default ApplicationPage;