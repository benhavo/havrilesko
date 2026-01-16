import { Outlet } from "react-router-dom";
import TopNav from "./TopNav";
import { ROUTES } from "@/constants/routes";

const NAV_ITEMS = ROUTES.map((route) => ({
  path: route.path,
  label: route.label,
}));

export default function Layout() {
  return (
    <>
      <header className="w-full">
        <TopNav items={NAV_ITEMS} />
      </header>
      <main className="flex-1">
        <Outlet />
      </main>
    </>
  );
}
