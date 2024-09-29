import React from "react";
import Section from "../components/Section";
import Endpoint from "../components/Endpoint";

const HeroesSection = () => (
  <Section id="heroes" title="Heroes">
    <Endpoint
      method="GET"
      path="/hero/search"
      description="Search for heroes based on a query."
      params={[
        { name: "query", required: true, description: "The search query." },
      ]}
      examples={[
        {
          title: "Search heroes in hero-fandom.",
          code: "/hero/search?query=Superman",
        },
      ]}
    />
    <Endpoint
      method="GET"
      path="/hero/details"
      description="Fetch detailed information about a specific hero."
      params={[
        {
          name: "heroid",
          required: true,
          description: "The ID of the hero to fetch details for.",
        },
      ]}
      examples={[
        {
          title: "Fetch hereos details from hero-fandom with id.",
          code: "/hero/details?heroid=Superman_(DC)",
        },
      ]}
    />
    <Endpoint
      method="GET"
      path="/hero/heroes"
      description="Fetch superhero data from the hero fandom website starting with a specific letter."
      params={[
        {
          name: "start",
          required: true,
          description:
            "A single character (A-Z) to filter heroes by their starting letter.",
        },
      ]}
      examples={[
        {
          title: "Fetch hereos from hero-fandom with names starting from A-Z.",
          code: "/hero/heroes?start=A",
        },
      ]}
    />
  </Section>
);

export default HeroesSection;
