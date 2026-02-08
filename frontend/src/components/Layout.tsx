import { Outlet } from "react-router-dom";
import TopNav from "./TopNav";
import { ROUTES } from "@/constants/routes";
import { cn } from "@/lib/utils";

const NAV_ITEMS = ROUTES.map((route) => ({
  path: route.path,
  label: route.label,
}));

const contentClasses = "mx-auto w-full flex-1 px-6 lg:px-10 lg:max-w-screen-lg";

export default function Layout() {
  return (
    <>
      <header className="w-full">
        <div className={cn(contentClasses, "pt-6")}>
          <TopNav items={NAV_ITEMS} />
        </div>
      </header>
      <main className={cn(contentClasses)}>
        <Outlet />
      </main>
    </>
  );
}
