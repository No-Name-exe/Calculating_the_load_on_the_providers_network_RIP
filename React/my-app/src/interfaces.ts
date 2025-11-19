export interface RouterResult {
  id: number;
  title: string;
  desc: string;
  img: string;
  status: string;
}

export interface RouterAppDetails {
  title: string;
  desc: string;
  img: string;
}

export interface ListRouterItem {
  id_router: number;
  master_router_id: number | null;
  router_load: number;
  Router: RouterAppDetails[];
}

export interface AppRouterResult {
  id: number;
  creator: string;
  moderator: string | null;
  status: string;
  date_create: string;
  date_modific: string | null;
  date_end: string;
  Adress: string;
  TotalUsers: number;
  ListRouter: ListRouterItem[];
}

export interface IconsRouter {
  routers_count: number;
  id_application: number;
}

export interface putAppRouter {
  Adress: string| undefined;
  TotalUsers: number | undefined;
}

export interface AppRouter {
  id: number;
  creator: string;
  moderator: string | null;
  status: string;
  date_create: string;
  date_modific: string | null;
  date_end: string;
  Adress: string;
  TotalUsers: number;
}