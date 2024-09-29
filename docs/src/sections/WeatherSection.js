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
          title: "Fetch weather data from Wunderground for Kolkata, India",
          code: "/weather/wunderground/in/Kolkata",
        },
        {
          title: "Fetch weather data from TimeandDate for Kolkata, India",
          code: "/weather/timeanddate/india/kolkata",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/weather/timeanddate/{country}/{location}/14day"
      description="Fetch 14-day weather forecast from TimeAndDate for a specific location."
      params={[
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
          title: "Fetch 14-day forecast from TimeandDate for Kolkata, India",
          code: "/weather/timeanddate/india/kolkata/14day",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/weather/timeanddate/{country}/{location}/24hour"
      description="Fetch 24-hour weather forecast from TimeAndDate for a specific location."
      params={[
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
          title: "Fetch 24-hour forecast from TimeandDate for Kolkata, India",
          code: "/weather/timeanddate/india/kolkata/24hour",
        },
      ]}
    />
  </Section>
);

export default WeatherSection;
