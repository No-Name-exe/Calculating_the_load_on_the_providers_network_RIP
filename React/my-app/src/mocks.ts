import type { RouterResult } from "./interfaces.ts"
export const ROUTERS_MOCK: RouterResult[] = [
	{
		id: 1,
		title: "Маршрутизатор провайдера",
		desc: "Роутер TP-Link Archer C7 — высокопроизводительный роутер с поддержкой Gigabit Ethernet и мощным процессором",
		img: "1.png",
		status: "действует"
	},
	{
		id: 2,
		title: "Маршрутизатор промежуточный",
		desc: "Роутер Asus RT-AC66U — надёжный роутер среднего класса с двумя диапазонами и функцией Mesh.",
		img: "2.png",
		status: "действует"
	},
	{
		id: 3,
		title: "Маршрутизатор жилого дома",
		desc: "Роутер D-Link DIR-615 — компактный и недорогой роутер для домашнего использования с базовыми функциями",
		img: "3.png",
		status: "действует"
	},
	{
		id: 4,
		title: "Маршрутизатор запасной",
		desc: "Роутер Netgear R6220 — резервный роутер с простым управлением и стабильной работой.",
		img: "4.jpg",
		status: "действует"
	},
	{
		id: 5,
		title: "Маршрутизатор школы",
		desc: "Роутер Cisco RV340 — корпоративное устройство с усиленной безопасностью и поддержкой VPN.",
		img: "5.png",
		status: "действует"
	},
	{
		id: 6,
		title: "Маршрутизатор почты",
		desc: "Роутер MikroTik hAP ac2 — роутер со встроенным файерволом и возможностями контроля трафика.",
		img: "6.jpg",
		status: "действует"
	}
]

import type { AppRouterResult } from "./interfaces.ts"
export const APPROUTERS_MOCK: AppRouterResult = {
	id: 5,
	creator: "root",
	moderator: null,
	status: "удалено",
	date_create: "2025-09-24",
	date_modific: null,
	date_end: "2025-10-06",
	Adress: "школа №7",
	TotalUsers: 90,
	ListRouter: [
		{
		id_router: 3,
		master_router_id: null,
		router_load: 20,
		Router: [
			{
			title: "Маршрутизатор жилого дома",
			desc: "Роутер D-Link DIR-615 — компактный и недорогой роутер для домашнего использования с базовыми функциями",
			img: "3.png"
			}
		]
		},
		{
		id_router: 4,
		master_router_id: 3,
		router_load: 20,
		Router: [
			{
			title: "Маршрутизатор запасной",
			desc: "Роутер Netgear R6220 — резервный роутер с простым управлением и стабильной работой.",
			img: "4.jpg"
			}
		]
		}
	]
}

export const ROUTER_MOCK: RouterResult = {
	id: 1,
	title: "Маршрутизатор провайдера",
	desc: "Роутер TP-Link Archer C7 — высокопроизводительный роутер с поддержкой Gigabit Ethernet и мощным процессором",
	img: "1.png",
	status: "действует"
}

import type { IconsRouter } from "./interfaces.ts"
export const ICON_MOCK: IconsRouter = {
	routers_count: 1,
	id_application: 5
}