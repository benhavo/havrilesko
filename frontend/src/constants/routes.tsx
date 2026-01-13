import Home from "../pages/Home";
import ErrorPage from "../pages/error-page";

export const ROUTES = [
  {
    path: "/",
    label: "Home",
    element: <Home />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/page1",
    label: "Page 1",
    element: <div />,
  },
];
