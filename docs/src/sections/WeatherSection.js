import React from "react";
import Section from "../components/Section";
import Endpoint from "../components/Endpoint";

const WeatherSection = () => (
  <Section id="weather" title="Weather">
    <Endpoint
      method="GET"
      path="/weather/{source}/{country}/{location}"
      description="Fetch weather data from a specified source for a specific location."
      params={[
        {
          name: "source",
          required: true,
          description: 'Either "wunderground" or "timeanddate".',
        },
        {
          name: "country",
          required: true,
          description: "The country name (2-50 characters).",
        },
        {
          name: "location",
          required: true,
          description: "The location name (2-50 characters).",
        },
      ]}
      examples={[
        {
          title: "Fetch weather data from Wunderground for Kokata, India",
          code: "GET /weather/wunderground/in/Kolkata",
        },
        {
          title: "Fetch weather data from TimeandDate for Kokata, India",
          code: "GET /weather/timeanddate/india/kolkata",
        },
      ]}
    />
  </Section>
);

export default WeatherSection;
