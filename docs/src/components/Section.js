import React from "react";

const Section = ({ id, title, children }) => (
  <section id={id} className="api-section">
    <h2>{title}</h2>
    {children}
  </section>
);

export default Section;
