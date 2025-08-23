import React, { useState, useEffect } from "react";

function Grid({ rows, cols, gridData, start, end, visitedNodes, pathNodes }) {
  const maxCellSize = 17;   // Maximum cell size
  const minCellSize = 8;    // Minimum cell size for small screens
  const [cellSize, setCellSize] = useState(maxCellSize);

  const calculateCellSize = () => {
    const sidebarWidth = window.innerWidth * 0.16; // assuming left bar ~16% width
    const containerWidth = window.innerWidth - sidebarWidth - 16; // subtract padding
    const containerHeight = window.innerHeight - 16; // vertical padding

    const widthSize = Math.floor(containerWidth / cols);
    const heightSize = Math.floor(containerHeight / rows);

    // Keep cell within min/max bounds
    setCellSize(Math.max(minCellSize, Math.min(widthSize, heightSize, maxCellSize)));
  };

  useEffect(() => {
    calculateCellSize();
    window.addEventListener("resize", calculateCellSize);
    return () => window.removeEventListener("resize", calculateCellSize);
  }, [rows, cols]);

  const visitedSet = new Set(visitedNodes.map(([r, c]) => `${r}-${c}`));
  const pathSet = new Set(pathNodes.map(([r, c]) => `${r}-${c}`));

  return (
    <div className="flex justify-center items-center h-full w-full bg-neutral-900 p-4 overflow-auto">
      <div
        className="grid border-2 border-gray-400 rounded-lg shadow-lg"
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
          gap: "1px",
          backgroundColor: "#1f2937", // Tailwind gray-800
          padding: "2px",
        }}
      >
        {gridData.map((row, rIdx) =>
          row.map((cell, cIdx) => {
            let cellClass = "bg-gray-200 border border-gray-300"; // default
            if (cell === 1) cellClass = "bg-gray-700 border border-gray-600"; // wall
            if (rIdx === start.row && cIdx === start.col) cellClass = "bg-green-500";
            else if (rIdx === end.row && cIdx === end.col) cellClass = "bg-red-500";
            else if (pathSet.has(`${rIdx}-${cIdx}`)) cellClass = "bg-yellow-400";
            else if (visitedSet.has(`${rIdx}-${cIdx}`)) cellClass = "bg-blue-400";

            return (
              <div
                key={`${rIdx}-${cIdx}`}
                style={{ width: cellSize, height: cellSize }}
                className={cellClass}
              />
            );
          })
        )}
      </div>
    </div>
  );
}

export default Grid;
