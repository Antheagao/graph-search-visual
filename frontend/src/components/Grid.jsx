import React, { useState, useEffect } from "react";

function Grid({ rows, cols, gridData, start, end }) {
  const [cellSize, setCellSize] = useState(20);

  const calculateCellSize = () => {
    const containerWidth = window.innerWidth * 0.75;
    const containerHeight = window.innerHeight;
    const widthSize = Math.floor(containerWidth / cols);
    const heightSize = Math.floor(containerHeight / rows);
    setCellSize(Math.min(widthSize, heightSize));
  };

  useEffect(() => {
    calculateCellSize();
    window.addEventListener("resize", calculateCellSize);
    return () => window.removeEventListener("resize", calculateCellSize);
  }, [rows, cols]);

  return (
    <div className="w-5/6 bg-neutral-900 p-4 border-gray-300 h-full overflow-hidden">
      <h2 className="text-xl font-bold mb-4 text-white">Grid</h2>
      <div
        className="grid"
        style={{
          gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
          gap: "1px",
        }}
      >
        {gridData.map((row, rIdx) =>
          row.map((cell, cIdx) => {
            let cellClass = "bg-gray-200 border border-gray-300";

            if (cell === 1) {
              cellClass = "bg-gray-700 border border-gray-300"; // wall
            }

            if (rIdx === start.row && cIdx === start.col) {
              cellClass = "bg-green-500"; // start node
            }

            if (rIdx === end.row && cIdx === end.col) {
              cellClass = "bg-red-500"; // end node
            }

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
