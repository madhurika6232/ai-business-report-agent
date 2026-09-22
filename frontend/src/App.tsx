import { AppRouter } from "./app/AppRouter";
import { QueryProvider } from "./app/QueryProvider";


function App() {
  return (
    <QueryProvider>
      <AppRouter />
    </QueryProvider>
  );
}


export default App;