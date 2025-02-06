import React, { useEffect, useState } from "react";
import axios from "axios";

const keys = [
  "Esc",
  "F1",
  "F2",
  "F3",
  "F4",
  "F5",
  "F6",
  "F7",
  "F8",
  "F9",
  "F10",
  "F11",
  "F12",
  "PrtSc",
  "ScrLk",
  "Pause",
  "`",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "0",
  "-",
  "=",
  "Backspace",
  "Tab",
  "Q",
  "W",
  "E",
  "R",
  "T",
  "Y",
  "U",
  "I",
  "O",
  "P",
  "[",
  "]",
  "\\",
  "CapsLock",
  "A",
  "S",
  "D",
  "F",
  "G",
  "H",
  "J",
  "K",
  "L",
  ";",
  "'",
  "Enter",
  "Shift",
  "Z",
  "X",
  "C",
  "V",
  "B",
  "N",
  "M",
  ",",
  ".",
  "/",
  "Shift",
  "Ctrl",
  "Alt",
  "Space",
  "Alt",
  "Ctrl",
];

interface Response {
  PressedKeys: string[];
}

async function sendKeys(sequences: string[][]) {
  for (let i = 0; i < sequences.length; i++) {
    const seq = sequences[i];
    try {
      const data: Response = { PressedKeys: seq };
      const response = await axios.post("http://localhost:8080/update", data, {
        headers: { "Content-Type": "application/json" },
      });
      console.log(`Successfully updated server with sequence ${i + 1}:`, seq);
    } catch (err) {
      console.error("Error sending update to server:", err.message);
      // You can implement more detailed error handling here (e.g., retry mechanism, user notification)
    }

    // Enforce at least 3-second interval between requests
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}

const Keyboard = () => {
  const [pressedKeys, setPressedKeys] = useState<Set<string>>(new Set());
  const [heldKeys, setHeldKeys] = useState<Set<string>>(new Set());

  useEffect(() => {
    const interval = setInterval(() => {
      const keysToSend = Array.from(pressedKeys).concat(Array.from(heldKeys));
      console.log("sendingKeys", keysToSend);
      try {
        sendKeys([keysToSend]);
      } catch (err) {
        console.error("Error during key send process:", err);
        // You can show some user feedback here if necessary
      }
    }, 5000);

    // Cleanup the interval when the component unmounts
    return () => clearInterval(interval);
  }, [pressedKeys, heldKeys]); // Add pressedKeys and heldKeys as dependencies

  const handlePress = (key: string) => {
    try {
      setPressedKeys((prev) => new Set(prev).add(key));
      setTimeout(() => {
        setPressedKeys((prev) => {
          const newKeys = new Set(prev);
          if (!heldKeys.has(key)) newKeys.delete(key); // Use the current state value
          return newKeys;
        });
      }, 5);
    } catch (err) {
      console.error("Error handling key press:", err);
    }
  };

  const handleHold = (key: string) => {
    try {
      setHeldKeys((prev) => {
        const newSet = new Set(prev);
        if (newSet.has(key)) {
          newSet.delete(key);
          setPressedKeys((prevKeys) => {
            const newKeys = new Set(prevKeys);
            newKeys.delete(key);
            return newKeys;
          });
        } else {
          newSet.add(key);
          setPressedKeys((prevKeys) => new Set(prevKeys).add(key));
        }
        return newSet;
      });
    } catch (err) {
      console.error("Error handling key hold:", err);
    }
  };

  return (
    <div className="flex flex-col items-center p-4">
      <div
        className="grid gap-2 w-[85%]"
        style={{ gridTemplateColumns: "repeat(5, minmax(40px, 1fr))" }}
      >
        {keys.map((key) => (
          <div key={key} className="flex flex-col items-center m-1">
            <button
              className={`w-20 px-3 py-2 rounded-md shadow-md ${
                pressedKeys.has(key) ? "bg-blue-600" : "bg-gray-800"
              } text-white hover:bg-gray-600`}
              onClick={() => handlePress(key)}
            >
              {key} (Press)
            </button>
            <button
              className={`w-20 px-3 py-2 rounded-md shadow-md ${
                heldKeys.has(key) ? "bg-red-600" : "bg-gray-800"
              } text-white hover:bg-gray-600 mt-1`}
              onClick={() => {
                handleHold(key);
              }}
            >
              {key} (Hold)
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Keyboard;
