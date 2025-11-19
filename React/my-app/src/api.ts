import type * as Interfaces from "./interfaces"
import * as DummyData from "./mocks"

const serverAdress='http://127.0.0.1:8080'
const ApiAdress='/api/api'
const serverAPIAdress=ApiAdress


export const getRouter = async (id = '1'): Promise<Interfaces.RouterResult> => {
  return fetch(`${serverAPIAdress}/Routers/${id}/`)
    .then((response) => {
      console.log('Response:', response);
      return response.json();
    })
    .then((data) => {
      console.log('Parsed JSON:', data);
      return data;
    })
    .catch((err) => {
      console.log('Error or fallback:', err);
      console.log("Подстановка заглушки");
      return DummyData.ROUTER_MOCK;
    });
}

export const getRouters = async (name = ''): Promise<Interfaces.RouterResult[]> =>{
  return fetch(`${serverAPIAdress}/Routers/filter/${name}/`)
      .then((response) => response.json())
      .catch(()=> ( DummyData.ROUTERS_MOCK ))
}

export const getIcons = async (): Promise<Interfaces.IconsRouter> =>{
  return fetch(`${serverAPIAdress}/AppRouters/icon/`)
      .then((response) => response.json())
      .catch(()=> ( DummyData.ICON_MOCK ))
}

export const getApp = async (id: number = 8): Promise<Interfaces.AppRouterResult> =>{
  return fetch(`${serverAPIAdress}/AppRouters/${id}/`)
      .then((response) => {
        if (!response.ok) {
          // Если статус не успешен, возвращаем заглушку
          // Можно добавить условия для 401, 403, 500 и т.п.
          return Promise.reject('Ошибка статуса: ' + response.status);
        }
        return response.json()
      })
      .catch(()=> ( DummyData.APPROUTERS_MOCK ))
}

export const putApp = async (id: number = 8): Promise<Interfaces.AppRouterResult> =>{
  return fetch(`${serverAPIAdress}/AppRouters/put/${id}/`)
      .then((response) => {
        if (!response.ok) {
          // Если статус не успешен, возвращаем заглушку
          // Можно добавить условия для 401, 403, 500 и т.п.
          return Promise.reject('Ошибка статуса: ' + response.status);
        }
        return response.json()
      })
      .catch(()=> ( DummyData.APPROUTERS_MOCK ))
}

export const putAppRouter = async (
  applicationId: string | number,
  data: Interfaces.putAppRouter
): Promise<Interfaces.AppRouter> => {
  return fetch(`${serverAPIAdress}/AppRouters/put/${applicationId}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  .then(res => {
    if (!res.ok) {
      throw new Error('Network response was not ok');
    }
    return res.json();
  })
  .catch(() => {
    // при ошибке можно вернуть мок или выбросить ошибку
    return DummyData.APPROUTERS_MOCK;
  });
};