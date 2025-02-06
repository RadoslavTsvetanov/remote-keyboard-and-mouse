import { useState, useRef, useEffect } from "react";

export default function ClickableCanvas() {
  const [clicks, setClicks] = useState([]);
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    canvas.width = 411 
    canvas.height = 915;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "red";
    clicks.forEach(({ x, y }) => {
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI);
      ctx.fill();
    });
  }, [clicks]);

  useEffect(() => {
    const handleResize = () => {
      const canvas = canvasRef.current;
      canvas.width = 411 
      canvas.height = 915 
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const sendRequest = (x, y, action) => {
    fetch("http://localhost:8080/updateMouse", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ x, y, action, dimensions: {x: 411, y: 915}}),
    });
  };

  const handleClick = (event) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    setClicks([...clicks, { x, y }]);
  };

  const handleMoveClick = () => {
    if (clicks.length > 0) {
      const { x, y } = clicks[clicks.length - 1];
      sendRequest(x, y, "move");
    }
  };

  const handleGeneralClick = () => {
    if (clicks.length > 0) {
      const { x, y } = clicks[clicks.length - 1];
      sendRequest(x, y, "click");
    }
  };

  return (
    <div>
      <div className="absolute top-2 left-2 z-10">
        <button onClick={handleMoveClick}>Move</button>
        <button onClick={handleGeneralClick}>Click</button>
      </div>
      <canvas
        ref={canvasRef}
        style={{ border: "1px solid black", display: "block" }}
        onClick={handleClick}
      />
    </div>
  );
}
