# Job Scraper API - README

## Overview
The Job Scraper Application combines a FastAPI backend and a React frontend to create a seamless job-searching experience. It scrapes job listings from Google search results targeting the Wellfound platform (formerly AngelList) and presents them in a user-friendly interface.

## Screenshots
<img width="1440" alt="Screenshot 2024-12-06 at 2 00 54 AM" src="https://github.com/user-attachments/assets/57db5b67-8e22-43b5-b580-872b9c1918eb">
<img width="1440" alt="Screenshot 2024-12-06 at 2 00 41 AM" src="https://github.com/user-attachments/assets/6fd2f6bb-701b-45b2-88bd-192532ab2cc6">
<img width="1440" alt="Screenshot 2024-12-06 at 2 00 32 AM" src="https://github.com/user-attachments/assets/d32f67f1-12f9-4071-8993-cde81dd75116">

## Features

- Backend (FastAPI)
1) Search for Jobs: Accepts a keyword to scrape job data from Wellfound via Google search.
2) Real-Time Scraping: Dynamically scrapes and parses job listings.
3) CORS Support: Middleware allows integration with the React frontend.
4) Error Handling: Provides structured error responses for failed requests.

- Frontend (React)
1) User-Friendly UI: Displays job results in an interactive and aesthetic layout.
2)Search Bar: Accepts job keywords to query the backend.
