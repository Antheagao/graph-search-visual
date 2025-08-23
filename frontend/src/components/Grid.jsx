import React, { useState, useEffect } from "react";

function Grid({ rows, cols, gridData, start, end, visitedNodes, pathNodes }) {
  const maxCellSize = 17;
  const [cellSize, setCellSize] = useState(maxCellSize);

  const calculateCellSize = () => {
    const widthSize = Math.floor(window.innerWidth / cols);
    const heightSize = Math.floor(window.innerHeight / rows);
    setCellSize(Math.min(widthSize, heightSize, maxCellSize));
  };

  useEffect(() => {
    calculateCellSize();
    window.addEventListener("resize", calculateCellSize);
    return () => window.removeEventListener("resize", calculateCellSize);
  }, [rows, cols]);

  const visitedSet = new Set(visitedNodes.map(([r, c]) => `${r}-${c}`));
  const pathSet = new Set(pathNodes.map(([r, c]) => `${r}-${c}`));

  return (
    <div className="flex justify-center items-center h-full w-full bg-neutral-900 p-4">
      <div
        className="grid border-2 border-gray-400 rounded-lg shadow-lg"
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
          gap: "1px",
          backgroundColor: "#1f2937", // Tailwind gray-800, subtle behind cells
          padding: "2px", // small padding inside border
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
