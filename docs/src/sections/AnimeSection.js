import React from "react";
import Section from "../components/Section";
import Endpoint from "../components/Endpoint";

const AnimeSection = () => (
  <Section id="anime" title="Anime">
    <Endpoint
      method="GET"
      path="/anime/mal/top"
      description="Get top anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-100). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top anime, page 1",
          code: "/anime/mal/top?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/top_airing"
      description="Get top airing anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-5). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top airing anime, page 1",
          code: "/anime/mal/top_airing?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/top_upcoming"
      description="Get top upcoming anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-6). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top upcoming anime, page 1",
          code: "/anime/mal/top_upcoming?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/top_series"
      description="Get top TV series anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-100). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top TV series anime, page 1",
          code: "/anime/mal/top_series?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/top_movies"
      description="Get top anime movies from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-40). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top anime movies, page 1",
          code: "/anime/mal/top_movies?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/top_ova"
      description="Get top OVA anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-30). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top OVA anime, page 1",
          code: "/anime/mal/top_ova?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/top_ona"
      description="Get top ONA anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-30). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top ONA anime, page 1",
          code: "/anime/mal/top_ona?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/top_special"
      description="Get top special anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-36). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get top special anime, page 1",
          code: "/anime/mal/top_special?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/most_popular"
      description="Get most popular anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-100). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get most popular anime, page 1",
          code: "/anime/mal/most_popular?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/most_fav"
      description="Get most favorited anime from MyAnimeList."
      params={[
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1 (1-100). Default: 1",
        },
      ]}
      examples={[
        {
          title: "Get most favorited anime, page 1",
          code: "/anime/mal/most_fav?page=1",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/season"
      description="Get anime for a specific season from MyAnimeList."
      params={[
        {
          name: "y",
          required: false,
          description: "Year of the anime season",
        },
        {
          name: "s",
          required: false,
          description: "Season (winter, spring, summer, fall)",
        },
      ]}
      examples={[
        {
          title: "Get anime for Spring 2023",
          code: "/anime/mal/season?y=2023&s=spring",
        },
        {
          title: "Get anime for current season",
          code: "/anime/mal/season",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/schedule"
      description="Get anime schedule from MyAnimeList."
      examples={[
        {
          title: "Get current anime schedule",
          code: "/anime/mal/schedule",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/search"
      description="Search anime on MyAnimeList."
      params={[
        {
          name: "q",
          required: true,
          description: "Search query",
        },
        {
          name: "page",
          required: false,
          description: "Page number, starting from 1. Default: 1",
        },
        {
          name: "type",
          required: false,
          description: "Anime type (tv / ova / movie / special / ona / music)",
        },
        {
          name: "score",
          required: false,
          description: "Minimum score (1-10)",
        },
        {
          name: "status",
          required: false,
          description: "Airing status (finished / airing / not_aired)",
        },
        {
          name: "genre",
          required: false,
          description:
            "Genre names. Available genres: action, adventure, avant garde, award winning, boys love, comedy, drama, fantasy, girls love, gourmet, horror, mystery, romance, sci-fi, slice of life, sports, supernatural, suspense, ecchi, erotica, hentai",
        },
        {
          name: "adult",
          required: false,
          description:
            "Whether to include adult anime (true / false). Default: false",
        },
        {
          name: "demographic",
          required: false,
          description:
            "Demographics (josei / kids / seinen / shoujo / shounen)",
        },
        {
          name: "start_date",
          required: false,
          description: "Start date (YYYY-MM-DD)",
        },
        {
          name: "end_date",
          required: false,
          description: "End date (YYYY-MM-DD)",
        },
      ]}
      examples={[
        {
          title: "Search for 'Naruto' anime",
          code: "/anime/mal/search?q=Naruto",
        },
        {
          title: "Search for TV series with minimum score 8",
          code: "/anime/mal/search?q=&type=tv&score=8",
        },
        {
          title: "Search for ongoing shounen anime",
          code: "/anime/mal/search?q=&status=airing&demographic=shounen",
        },
      ]}
    />

    <Endpoint
      method="GET"
      path="/anime/mal/details"
      description="Get anime details from MyAnimeList."
      params={[
        {
          name: "id",
          required: true,
          description: "MyAnimeList ID of the anime",
        },
      ]}
      examples={[
        {
          title: "Get details for 'Death Note' (ID: 1535)",
          code: "/anime/mal/details?id=1535",
        },
      ]}
    />
  </Section>
);

export default AnimeSection;
