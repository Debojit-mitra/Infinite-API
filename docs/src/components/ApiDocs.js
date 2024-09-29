import React, { useState, useEffect, useRef } from "react";
import { useTransition, animated } from "react-spring";
import Navigation from "./Navigation";
import ThemeToggle from "./ThemeToggle";
import WeatherSection from "../sections/WeatherSection";
import BooksSection from "../sections/BooksSection";
import PhonesSection from "../sections/PhonesSection";
import HeroesSection from "../sections/HeroesSection";
import apiLogo from "../logo192.png";
import AnimeSection from "../sections/AnimeSection";

const ApiDocs = () => {
  const [activeSection, setActiveSection] = useState("weather"); //comment below is important
  const prevSectionRef = useRef(activeSection); // eslint-disable-next-line
  const [direction, setDirection] = useState(0);
  const [isDark, setIsDark] = useState(() => {
    const savedTheme = localStorage.getItem("theme");
    return savedTheme ? savedTheme === "dark" : true;
  });

  const mainContentRef = useRef(null);

  const sections = [
    { id: "weather", title: "Weather", component: WeatherSection },
    { id: "books", title: "Books", component: BooksSection },
    { id: "phones", title: "Phones", component: PhonesSection },
    { id: "heroes", title: "Heroes", component: HeroesSection },
    { id: "anime", title: "Anime", component: AnimeSection },
  ];

  const toggleTheme = () => {
    setIsDark((prevIsDark) => {
      const newTheme = !prevIsDark;
      localStorage.setItem("theme", newTheme ? "dark" : "light");
      return newTheme;
    });
  };

  useEffect(() => {
    document.body.className = isDark ? "dark-theme" : "light-theme";
  }, [isDark]);

  const resetScroll = () => {
    if (mainContentRef.current) {
      mainContentRef.current.scrollTop = 0;
    }
  };

  const handleSetActiveSection = (newSection) => {
    const currentIndex = sections.findIndex(
      (section) => section.id === activeSection
    );
    const newIndex = sections.findIndex((section) => section.id === newSection);
    setDirection(newIndex > currentIndex ? 1 : -1);
    prevSectionRef.current = activeSection;
    setActiveSection(newSection);
    resetScroll();
  };

  const transitions = useTransition(activeSection, {
    from: { opacity: 0, position: "absolute", width: "100%", height: "100%" },
    enter: { opacity: 1 },
    leave: { opacity: 0 },
    config: { duration: 300 },
  });

  return (
    <div className="api-docs">
      <header>
        <div className="header-content">
          <img src={apiLogo} alt="API Icon" className="api-icon" />
          <h1>Infinite API Documentation</h1>
        </div>
        <ThemeToggle isDark={isDark} toggleTheme={toggleTheme} />
      </header>
      <div className="content">
        <Navigation
          sections={sections}
          activeSection={activeSection}
          setActiveSection={handleSetActiveSection}
        />
        <main ref={mainContentRef}>
          <div className="section-container">
            {transitions((style, item) => (
              <animated.div style={style} className="animated-section">
                {sections.find((section) => section.id === item)?.component()}
              </animated.div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
};

export default ApiDocs;
