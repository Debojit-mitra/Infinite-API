# API Endpoints

## Heroes

### 1. GET /heroes

**Description:** Fetch superhero data from the hero fandom website starting with a specific letter.

- **Query Parameters:**
  - `start` (required): A single character (A-Z) to filter heroes by their starting letter.

### 2. GET /details

**Description:** Fetch detailed information about a specific hero.

- **Query Parameters:**
  - `heroid` (required): The ID of the hero to fetch details for.

### 3. GET /search

**Description:** Search for heroes based on a query.

- **Query Parameters:**
  - `query` (required): The search query.

## Phones

### 4. GET /gsmarena

**Description:** Fetch detailed phone specifications from GSMArena for a specific phone URL.

- **Query Parameters:**
  - `id` (required): URL of the phone details page on GSMArena.

### 5. GET /gsmarena/top

**Description:** Fetch top seventy phones from GSMArena.

### 6. GET /gsmarena/{search_query}

**Description:** Fetch phone data from GSMArena for a specific search query.

- **Path Parameters:**
  - `search_query` (required): The search query for phones (1-200 characters).

## Books

### 7. GET /libgen/download/{source}/{download_id}

**Description:** Fetch download link for a specific book from Libgen.

- **Path Parameters:**
  - `source` (required): Either "library_lol" or "libgen_li".
  - `download_id` (required): 32-character ID of the book.

### 8. GET /libgen/{bookname}

**Description:** Fetch book data from Libgen for a specific book name.

- **Path Parameters:**
  - `bookname` (required): The name of the book to search for (1-200 characters).

## Weather

### 9. GET /{source}/{country}/{location}

**Description:** Fetch weather data from a specified source for a specific location.

- **Path Parameters:**
  - `source` (required): Either "wunderground" or "timeanddate".
  - `country` (required): The country name (2-50 characters).
  - `location` (required): The location name (2-50 characters).
