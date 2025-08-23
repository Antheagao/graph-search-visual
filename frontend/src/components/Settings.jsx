import React from "react";

function Settings({ settings, setSettings, onSolve, stats, onResetWalls }) {
  const handleAlgorithmChange = (e) => {
    const { value } = e.target;
    setSettings((prev) => ({ ...prev, algorithm: value }));
  };

  return (
    <div className="w-1/6 bg-neutral-900 p-6 border-r border-gray-700 flex flex-col justify-between">
      
      {/* Top Section: Algorithm & Controls */}
      <div className="flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-white">Settings</h2>
        
        <div className="flex flex-col gap-4">
          <label className="text-gray-200 font-medium">
            Algorithm Type:
            <select
              value={settings.algorithm}
              onChange={handleAlgorithmChange}
              className="mt-1 p-2 rounded-md bg-neutral-800 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option>DFS</option>
              <option>BFS</option>
              <option>Dijkstra</option>
              <option>A*</option>
            </select>
          </label>

          <button
            onClick={onResetWalls}
            className="bg-gray-600 text-white p-2 rounded-md shadow-md transition-transform transform hover:scale-105 hover:bg-gray-500"
          >
            Redo Walls
          </button>

          <button
            onClick={onSolve}
            className="bg-blue-600 text-white p-2 rounded-md shadow-md transition-transform transform hover:scale-105 hover:bg-blue-500"
          >
            Solve
          </button>
        </div>
      </div>

      {/* Bottom Section: Stats */}
      <div className="mt-8">
        <h2 className="text-xl font-bold text-white mb-4">Stats</h2>
        <div className="flex flex-col gap-3 text-gray-200">
          <div className="flex justify-between">
            <span>Solution found:</span>
            <span className={stats.solved ? "text-green-400" : "text-red-400"}>
              {stats.solved ? "Yes" : "No"}
            </span>
          </div>
          <div className="flex justify-between">
            <span>Time taken:</span>
            <span>{stats.time.toFixed(3)} ms</span>
          </div>
          <div className="flex justify-between">
            <span>Nodes expanded:</span>
            <span>{stats.nodesExpanded}</span>
          </div>
          <div className="flex justify-between">
            <span>Path length:</span>
            <span>{stats.pathLength}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
