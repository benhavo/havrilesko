import { useRouteError, isRouteErrorResponse } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  let errorMessage: string;

  // TODO: Only display detailed error info in development mode
  if (isRouteErrorResponse(error)) {
    // TypeScript now knows 'error' is of type 'ErrorResponse'
    errorMessage = error.statusText;
  } else if (error instanceof Error) {
    // General JavaScript error
    errorMessage = error.message;
  } else {
    // Fallback for other unknown cases
    errorMessage = "An unknown error occurred";
  }

  return (
    <div id="error-page">
      <h1>Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p>
        <i>{errorMessage}</i>
      </p>
    </div>
  );
}
