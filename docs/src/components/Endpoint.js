import React from "react";
import CopyButton from "./CopyButton";

const Endpoint = ({ method, path, description, params, examples }) => (
  <div className="endpoint">
    <h3>
      <span className={`method ${method.toLowerCase()}`}>{method}</span> {path}
    </h3>
    <p className="description">{description}</p>
    {params && params.length > 0 && (
      <div className="params">
        <h4>Parameters:</h4>
        <ul>
          {params.map((param, index) => (
            <li key={index}>
              <span className="param-name">{param.name}</span>
              <span className="param-required">
                ({param.required ? "required" : "optional"})
              </span>
              <span className="param-description">{param.description}</span>
            </li>
          ))}
        </ul>
      </div>
    )}
    {examples && examples.length > 0 && (
      <div className="examples">
        <h4>Examples:</h4>
        {examples.map((example, index) => (
          <div key={index} className="example">
            <h5>{example.title}</h5>
            <div className="code-container">
              <pre>
                <code>
                  <span className="http-method">{method}</span> {example.code}
                </code>
              </pre>
              <CopyButton text={example.code} />
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);
export default Endpoint;
