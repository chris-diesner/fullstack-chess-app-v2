import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/App.css";
import AnimatedRoutes from "./components/AnimatedRoutes";
import { UserProvider } from "./components/hooks/UserHooks";
import { GameProvider } from "./components/hooks/GameHooks";

function App() {
  return (
    <UserProvider>
      <GameProvider>
        <div className="App">
          <AnimatedRoutes />
        </div>
      </GameProvider>
    </UserProvider>
  );
}

export default App;