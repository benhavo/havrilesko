import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { ROUTES } from "./routes";
import Layout from "@/components/Layout";
import ErrorPage from "@/pages/error-page";

export const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<Layout />} errorElement={<ErrorPage />}>
      {ROUTES.map((route) => (
        <Route key={route.path} path={route.path} element={route.element} />
      ))}
      <Route path="*" element={<ErrorPage />} />
    </Route>
  )
);
