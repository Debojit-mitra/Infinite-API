import React, { useState, useRef } from "react";

const CopyButton = ({ text }) => {
  const [copied, setCopied] = useState(false);
  const buttonRef = useRef(null);

  const handleCopy = async () => {
    // Remove the HTTP method from the text
    const cleanedText = text.replace(/^(GET|POST|PUT|DELETE)\s/, "");

    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(cleanedText);
      } else {
        // Fallback for browsers that don't support clipboard API
        const textArea = document.createElement("textarea");
        textArea.value = cleanedText;
        textArea.style.position = "fixed"; // Prevent scrolling to the bottom
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);

      // Blur the button to prevent focus and avoid triggering the virtual keyboard
      if (buttonRef.current) {
        buttonRef.current.blur();
      }
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  return (
    <button ref={buttonRef} className="copy-button" onClick={handleCopy}>
      {copied ? "Copied!" : "Copy"}
    </button>
  );
};

export default CopyButton;
