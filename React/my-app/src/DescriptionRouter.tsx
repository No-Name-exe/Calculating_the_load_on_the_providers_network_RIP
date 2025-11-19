import React from 'react';
import { useParams } from 'react-router-dom';
import { DatabaseAdress } from './CONSTANTS.ts';
import './Router.css'
import type * as Interfaces from './interfaces.ts';
import * as Api from './api.ts';
import HeadRouter from './HeadRouter.tsx';
import { ROUTE_LABELS, ROUTES } from './ROUTES.tsx';
import { BreadCrumbs } from './BreadCrumbs.tsx';

const fallbackImage = '/Modem-Failure-Error.png';


type DataProps = any;
interface DescriptionRouterProps {
  data?: DataProps; // ReactNode включает любой допустимый элемент React
}

const DescriptionRouter: React.FC<DescriptionRouterProps> = ({ data }) => {

  const { id } = useParams<{ id: string }>();

  // const [searchRouter, setSearchRouterId] = React.useState('')
  // const [RouterFound, setRouter] = React.useState<Interfaces.RouterResult>()
  const [routerDetails, setRouterDetails] = React.useState<Interfaces.RouterResult | null>(null);

  const [loading, setLoading] = React.useState(false)

   const [imgSrc, setImgSrc] = React.useState<string>('');

  // const handleSearch = async () =>{
  //   setLoading(true)
  //   const result  = await Api.getRouter(searchRouter)
  //   console.log(result)
  //   setRouter(result)
  //   setLoading(false)
  // }

  React.useEffect(() => {
    if (id) {
      setLoading(true);
      Api.getRouter(id)
        .then((result) => {
          console.log(result)
          setRouterDetails(result);
          setImgSrc(`${DatabaseAdress}${result.img}`);
        })
        .finally(() => setLoading(false));
    }
  }, [id]);

  if (loading) return <div>Загрузка...</div>;

  return routerDetails ? (
    <>
    <BreadCrumbs crumbs={[{ label: ROUTE_LABELS.ROUTERS, path: ROUTES.ROUTERS},{ label: routerDetails.title || "Роутер" },]} />
    <HeadRouter />
    <div>
      {/* Заголовок */}
      <h3 className="bigtitle">Информация о маршрутизаторе</h3>
      
      {/* Основной блок с изображением и описанием */}
      <span className="block-deep">
        <img
          className="image"
          src={imgSrc}
          width={104}
          height={88}
          alt="Router Image"
          onError={() => setImgSrc(fallbackImage)}
        />
        <span className="title">{routerDetails.title}</span>
        <span className="desc-deep-rev">{routerDetails.desc}</span>
      </span>
    </div>
  </>
  ): null;
};

export default DescriptionRouter;