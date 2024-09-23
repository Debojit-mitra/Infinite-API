import React from "react";

const Navigation = ({ sections, activeSection, setActiveSection }) => {
  return (
    <nav className="api-nav">
      <ul>
        {sections.map(({ id, title }) => (
          <li key={id} className={activeSection === id ? "active" : ""}>
            <a
              href={`#${id}`}
              onClick={(e) => {
                e.preventDefault();
                setActiveSection(id);
              }}
            >
              {title}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navigation;
