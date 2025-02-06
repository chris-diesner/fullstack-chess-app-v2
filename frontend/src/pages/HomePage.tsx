import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div>
      <h1>Willkommen auf der Startseite!</h1>
      <nav>
        <ul>
          <li><Link to="/game">Zum Schachbrett</Link></li> 
        </ul>
      </nav>
    </div>
  );
}
