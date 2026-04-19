import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router";

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div data-testid="app">
          <h1 className="text-2xl font-bold">Webapp</h1>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
