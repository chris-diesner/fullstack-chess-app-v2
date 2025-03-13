import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/App.css";
import AnimatedRoutes from "./components/AnimatedRoutes";
import { UserProvider } from "./components/hooks/UserHooks";

function App() {
  return (
    <UserProvider>
      <div className="App">
        <AnimatedRoutes />
      </div>
    </UserProvider>
  );
}

export default App;