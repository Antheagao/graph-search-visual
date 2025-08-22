import { useState } from 'react';
import './App.css';
import Settings from './components/Settings';
import Grid from './components/Grid';

function App() {
  const solve = async () => {
    const payload = {
      algorithm: settings.algorithm,
      grid: gridData,
      start,
      end,
      rows: settings.rows,
      cols: settings.cols,
    };

    try {
      const response = await fetch('http://localhost:5000/solve', { // Replace with your backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      // For now, just log the response
      const result = await response.json();
      console.log(result);

      // Example: update stats if backend responds
      if (result.stats) {
        setStats(result.stats);
      }
    } catch (error) {
      console.error('Error sending grid to backend:', error);
    }
  };

  const [settings, setSettings] = useState({
    algorithm: "DFS",
    rows: 50,
    cols: 90,
  });

  const [stats, setStats] = useState({
    solved: false,
    time: 0,
    nodesExpanded: 0,
    pathLength: 0,
  });

  // Start and End nodes
  const [start, setStart] = useState({ row: 0, col: 0 });
  const [end, setEnd] = useState({ row: settings.rows - 1, col: settings.cols - 1 });

  const [gridData, setGridData] = useState(
    Array(settings.rows)
      .fill(0)
      .map(() => Array(settings.cols).fill(0))
  );

  const generateGrid = () => {
    const newGrid = Array(settings.rows)
      .fill(0)
      .map(() =>
        Array(settings.cols)
          .fill(0)
          .map(() => (Math.random() > 0.7 ? 1 : 0))
      );

    // Ensure start and end are open
    newGrid[start.row][start.col] = 0;
    newGrid[end.row][end.col] = 0;

    setGridData(newGrid);

    setStats({
      solved: false,
      time: 0,
      nodesExpanded: 0,
      pathLength: 0,
    });
  };

  const redoWalls = () => {
    const newGrid = Array(settings.rows)
      .fill(0)
      .map(() =>
        Array(settings.cols)
          .fill(0)
          .map(() => (Math.random() > 0.7 ? 1 : 0)) // random walls
      );

    // Ensure start and end are open
    newGrid[start.row][start.col] = 0;
    newGrid[end.row][end.col] = 0;

    setGridData(newGrid);
    setStats({
      solved: false,
      time: 0,
      nodesExpanded: 0,
      pathLength: 0,
    });
  };

  return (
    <div className="h-screen w-screen flex">
      {/* Settings panel */}
      <Settings
        settings={settings}
        setSettings={setSettings}
        onGenerate={generateGrid}
        stats={stats}
        onResetWalls={redoWalls}
        onSolve={solve}
      />

      {/* Grid panel */}
      <Grid
        rows={settings.rows}
        cols={settings.cols}
        gridData={gridData}
        start={start}
        end={end}
      />
    </div>
  );
}

export default App;
