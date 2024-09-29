import React from "react";
import Section from "../components/Section";
import Endpoint from "../components/Endpoint";

const BooksSection = () => (
  <Section id="books" title="Books">
    <Endpoint
      method="GET"
      path="/books/libgen/{bookname}"
      description="Fetch book data from Libgen for a specific book name."
      params={[
        {
          name: "bookname",
          required: true,
          description: "The name of the book to search for (1-200 characters).",
        },
      ]}
      examples={[
        {
          title: "Fetch multiple books from libgen.",
          code: "/books/libgen/Thermodynamics R K",
        },
      ]}
    />
    <Endpoint
      method="GET"
      path="/books/libgen/download/{source}/{download_id}"
      description="Fetch download link for a specific book from Libgen."
      params={[
        {
          name: "source",
          required: true,
          description: 'Either "library_lol" or "libgen_li".',
        },
        {
          name: "download_id",
          required: true,
          description: "32-character ID of the book.",
        },
      ]}
      examples={[
        {
          title: "Download books from libgen.",
          code: "/books/libgen/download/library_lol/1234567890abcdef1234567890abcdef",
        },
      ]}
    />
  </Section>
);

export default BooksSection;
