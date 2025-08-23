import { useState, useEffect } from 'react';
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
      const response = await fetch('http://127.0.0.1:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      console.log(result);

      // reset visualization
      setVisitedNodes([]);
      setPathNodes([]);
      setStats({
        solved: result.stats.solved,
        time: result.stats.time,
        nodesExpanded: 0, // will increment as nodes are displayed
        pathLength: result.stats.pathLength,
      });

      const visitedOrder = result.visited || [];
      const path = result.path || [];

      // animate visited nodes
      visitedOrder.forEach((node, i) => {
        setTimeout(() => {
          setVisitedNodes((prev) => [...prev, node]);
          setStats((prevStats) => ({
            ...prevStats,
            nodesExpanded: prevStats.nodesExpanded + 1,
          }));
        }, i * 5); // 5ms per visited node
      });

      // animate path after all visited nodes
      setTimeout(() => {
        path.forEach((node, i) => {
          setTimeout(() => {
            setPathNodes((prev) => [...prev, node]);
          }, i * 10); // 10ms per path node
        });
      }, visitedOrder.length * 5);

    } catch (error) {
      console.error('Error sending grid to backend:', error);
    }
  };

  const [settings, setSettings] = useState({
    algorithm: "DFS",
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
  const [end, setEnd] = useState({ row: settings.rows - 1, col: settings.cols - 1 });

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

  // ✅ call generateGrid when component mounts
  useEffect(() => {
    generateGrid();
  }, []); // empty dependency array ensures it runs once

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
