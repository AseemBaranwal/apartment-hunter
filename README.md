# 🏠 Apartment Hunter MVP

An MVP project to build a smart apartment hunting tool for **San Jose + San Francisco**.  
The goal is to scrape, enrich, and rank apartments based on **price fairness → locality → amenities**, and present them in a modern web UI.

---

## 🌐 Vision

Finding an apartment in the Bay Area is hard: high rent, scattered listings, and inconsistent data.  
This project aims to solve that by combining **scraping, open data, scoring, and enrichment APIs** into one streamlined platform.

### Core Ideas

- Scrape apartment listings from operators (Avalon, Prometheus, Essex) and Zillow
- Normalize and deduplicate communities
- Score apartments based on:
  - **Price fairness** vs. neighborhood median
  - **Locality**: WalkScore, POI density, safety metrics
  - **Amenities**: must-have filters + bonus points
- Enrich top results with **Google Places/Photos/Routes** for polish
- Display results in a **Next.js card-based UI with filters**

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python), SQLAlchemy + GeoAlchemy2 (ORM), async I/O
- **Database:** PostgreSQL with PostGIS (spatial support)
- **Scraping:** Playwright (dynamic), BeautifulSoup4 (parsing)
- **Data Engineering:** pandas (scoring + processing)
- **Frontend:** Next.js (TypeScript + React), TailwindCSS, shadcn/ui
- **APIs:**
  - Zillow (scraping)
  - Operator sites: Avalon, Prometheus, Essex, UDR
  - WalkScore API
  - Overpass API (OpenStreetMap)
  - SF + SJ open data portals (crime/incidents)
  - Google Places / Photos / Routes Matrix (for enrichment)
- **Containerization:** Docker + Docker Compose
- **Admin Tools:** pgAdmin (DB GUI)

---

## 📦 Architecture

### Dataflow (ETL pipeline mindset)

1. **Scrapers** → collect raw HTML/JSON, store in `source_snapshot`
2. **Normalizer** → extract structured data: `community`, `listing`, `unit_type`, `price_snapshot`
3. **Locality Scoring** → WalkScore + OSM POIs + crime data → `locality_metric`
4. **Ranking Engine** → price fairness + locality + amenities → `ranking`
5. **Google Enrichment** → enrich top-K with photos, ratings, commute times → `place_cache` + `route_cache`
6. **Frontend** → card-based UI with filters powered by `/ranked-communities` and `/enrich-topk`

### ER Diagram

See [`documentation/apartment_hunter_er_detailed_v2.png`](documentation/apartment_hunter_er_detailed_v2.png)

### Dataflow Diagram

See [`documentation/apartment_hunter_dataflow_v2.png`](documentation/apartment_hunter_dataflow_v2.png)

---

## 🚀 Week-by-Week Updates

### ✅ Week 1 – Backend & Schema Setup

- Set up **Docker Compose** with:
  - `backend` (FastAPI)
  - `db` (Postgres + PostGIS)
  - `pgadmin` (DB GUI)
- Defined **database schema** aligned to ER diagram:
  - `community`, `listing`, `unit_type`, `price_snapshot`, `amenity`, `listing_amenity`
  - `locality_metric`, `ranking`, `source_snapshot`
  - `route_cache`, `place_cache`, `cache_table`
- Integrated **SQLAlchemy + GeoAlchemy2** for ORM + spatial columns
- Added **Pydantic v2 schemas** with Base/Create/Out separation
- Implemented `/health` and `/communities` endpoints
- Eager loading in CRUD → `/communities` returns nested `listings` + `price_snapshots`
- Verified DB structure using pgAdmin
- Added **nuke workflow** with `docker compose down -v` for clean resets

---

## 📌 Next Steps

- **Week 2:** Scrape Avalon, Prometheus, Essex → populate communities, listings, price_snapshots
- **Week 3:** Scrape Zillow + deduplication
- **Week 4:** Compute locality metrics (WalkScore, OSM POIs, city data)
- **Week 5:** Ranking engine (price + locality + amenities)
- **Week 6:** Enrich top-K with Google Places/Photos/Routes
- **Week 7:** Next.js frontend (card UI with filters)
- **Week 8:** Filters, polish, deploy backend (Docker Compose) + frontend (Vercel)

---

## 🧑‍💻 Development

### Start services

```bash
docker compose up --build
```
