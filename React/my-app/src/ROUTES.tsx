export const ROUTES = {
	HOME: "/",
	ROUTER: "/router",
	ROUTERS: "/routers",
	APPROUTER: "/application_router",
};
export const ROUTE_LABELS: {
	[key in RouteKeyType]: string;
} = {
	HOME: "Главная",
	ROUTERS: "Список роутеров",
	ROUTER: "Роутер",
	APPROUTER: "Нагрузка",
};
