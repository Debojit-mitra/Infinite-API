import React from "react";

const ThemeToggle = ({ isDark, toggleTheme }) => {
  return (
    <button className="theme-toggle" onClick={toggleTheme}>
      {isDark ? "☀️" : "🌙"}
    </button>
  );
};

export default ThemeToggle;
