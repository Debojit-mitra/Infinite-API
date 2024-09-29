import React from "react";
import Section from "../components/Section";
import Endpoint from "../components/Endpoint";

const PhonesSection = () => (
  <Section id="phones" title="Phones">
    <Endpoint
      method="GET"
      path="/phones/gsmarena/{search_query}"
      description="Fetch phone data from GSMArena for a specific search query."
      params={[
        {
          name: "search_query",
          required: true,
          description: "The search query for phones (1-200 characters).",
        },
      ]}
      examples={[
        {
          title: "Fetch phone details data from GSMArena.",
          code: "/phones/gsmarena/iphone%2012",
        },
      ]}
    />
    <Endpoint
      method="GET"
      path="/phones/gsmarena/top"
      description="Fetch top seventy phones from GSMArena."
      examples={[
        {
          title: "Fetch phone details data from GSMArena.",
          code: "/phones/gsmarena/top",
        },
      ]}
    />
    <Endpoint
      method="GET"
      path="/phones/gsmarena"
      description="Fetch detailed phone specifications from GSMArena for a specific phone URL."
      params={[
        {
          name: "id",
          required: true,
          description: "URL of the phone details page on GSMArena.",
        },
      ]}
      examples={[
        {
          title: "Fetch phone details data from GSMArena.",
          code: "/phones/gsmarena?id=https://www.gsmarena.com/samsung_galaxy_s21-10626.php",
        },
      ]}
    />
  </Section>
);

export default PhonesSection;
