import React from "react"; 

function Settings({ settings, setSettings, onSolve, stats, onResetWalls }) {
  const handleAlgorithmChange = (e) => {
    const { value } = e.target;
    setSettings((prev) => ({ ...prev, algorithm: value }));
  };

  return (
    <div className="w-1/6 bg-neutral-900 p-4 border-r border-gray-300 h-full flex flex-col">
      
      {/* Top Half: Algorithm & Controls */}
      <div className="flex-1 flex flex-col">
        <h2 className="text-xl font-bold mb-4">Settings</h2>
        <div className="flex flex-col gap-4">
          <label>
            Algorithm Type:
            <select
              value={settings.algorithm}
              onChange={handleAlgorithmChange}
              className="border bg-neutral-900 p-1 w-full mt-1"
            >
              <option>DFS</option>
              <option>BFS</option>
              <option>Dijkstra</option>
              <option>A*</option>
            </select>
          </label>
          
          <button
            onClick={onResetWalls}
            className="bg-gray-500 text-white p-2 rounded mt-2 transition-transform transform hover:scale-103"
          >
            Redo Walls
          </button>

          <button
            onClick={onSolve}
            className="bg-blue-500 text-white p-2 rounded mt-2 transition-transform transform hover:scale-103"
          >
            Solve
          </button>
        </div>
      </div>

      {/* Bottom Half: Stats */}
      <div className="flex-1 flex flex-col mt-6 overflow-y-auto">
        <h2 className="text-xl font-bold mb-2">Stats</h2>
        <div className="flex flex-col gap-2 text-gray-200">
          <div>Solved? {stats.solved ? "Yes" : "No"}</div>
          <div>Time taken: {stats.time} ms</div>
          <div>Nodes expanded: {stats.nodesExpanded}</div>
          <div>Path length: {stats.pathLength}</div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
