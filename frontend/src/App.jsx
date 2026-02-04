import { useState, useEffect } from 'react';
import Settings from './components/Settings';
import Grid from './components/Grid';

function App() {
  const API_BASE =
    (import.meta.env.VITE_API_URL ?? "").replace(/\/+$/, "") || // e.g. https://graph-search-visual.onrender.com
    (window.location.hostname === "localhost" ? "http://127.0.0.1:8000" : ""); // same-origin fallback

  const solve = async () => {
    const payload = {
      algorithm: settings.algorithm,
      grid: gridData,
      start,
      end,
      rows: settings.rows,
      cols: settings.cols,
    };

    // Reset visualization before solving
    setVisitedNodes([]);
    setPathNodes([]);
    setStats({
      solved: false,
      time: 0,
      nodesExpanded: 0,
      pathLength: 0,
    });

    try {
      const response = await fetch(`${API_BASE}/solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      // Check if response is ok
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();

      // Validate response structure
      if (!result.stats || !Array.isArray(result.visited) || !Array.isArray(result.path)) {
        throw new Error('Invalid response format from server');
      }

      // Update stats immediately
      setStats({
        solved: result.stats.solved,
        time: result.stats.time,
        nodesExpanded: 0, // will increment as nodes are displayed
        pathLength: result.stats.pathLength,
      });

      const visitedOrder = result.visited || [];
      const path = result.path || [];

      // Animate visited nodes
      visitedOrder.forEach((node, i) => {
        setTimeout(() => {
          setVisitedNodes((prev) => [...prev, node]);
          setStats((prevStats) => ({
            ...prevStats,
            nodesExpanded: prevStats.nodesExpanded + 1,
          }));
        }, i * 5); // 5ms per visited node
      });

      // Animate path after all visited nodes
      setTimeout(() => {
        path.forEach((node, i) => {
          setTimeout(() => {
            setPathNodes((prev) => [...prev, node]);
          }, i * 10); // 10ms per path node
        });
      }, visitedOrder.length * 5);

    } catch (error) {
      console.error('Error solving pathfinding problem:', error);
      // Update stats to show error state
      setStats((prevStats) => ({
        ...prevStats,
        solved: false,
      }));
      // Optionally show user-friendly error message
      alert(`Failed to solve: ${error.message}. Please check your connection and try again.`);
    }
  };

  const [settings, setSettings] = useState({
    algorithm: "A*",
    rows: 50,
    cols: 50,
  });

  const [stats, setStats] = useState({
    solved: false,
    time: 0,
    nodesExpanded: 0,
    pathLength: 0,
  });

  const [start, setStart] = useState({ row: 0, col: 0 });
  const [end, setEnd] = useState({ row: 49, col: 49 }); // Default to 50x50 grid

  const [gridData, setGridData] = useState(
    Array(settings.rows)
      .fill(0)
      .map(() => Array(settings.cols).fill(0))
  );

  const [visitedNodes, setVisitedNodes] = useState([]);
  const [pathNodes, setPathNodes] = useState([]);

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
    setStats({ solved: false, time: 0, nodesExpanded: 0, pathLength: 0 });
    setVisitedNodes([]);
    setPathNodes([]);
  };

  const redoWalls = generateGrid;

  // Update end position when grid dimensions change
  useEffect(() => {
    setEnd({ row: settings.rows - 1, col: settings.cols - 1 });
    generateGrid();
  }, [settings.rows, settings.cols]); // Regenerate grid when dimensions change

  return (
    <div className="h-screen w-screen flex">
      <Settings
        settings={settings}
        setSettings={setSettings}
        onGenerate={generateGrid}
        stats={stats}
        onResetWalls={redoWalls}
        onSolve={solve}
      />

      <Grid
        rows={settings.rows}
        cols={settings.cols}
        gridData={gridData}
        start={start}
        end={end}
        visitedNodes={visitedNodes}
        pathNodes={pathNodes}
      />
    </div>
  );
}

export default App;
