# Grounding Gemini with Google Search and Other Data Sources

## Overview

When you only have a few data sources (e.g., PDFs, JSON) that are required in your generative AI application, building RAG might not be worth the time and effort. In this repo, I'll show how you can use Google Gemini to retrieve context from three data sources. I'll also show how you can combine the context and ground results using Google search. This enables the end user to combine real-time information from Google Search with their internal data sources.

This application can answer any question related to events occurring in Philadelphia (I'm only using Philadelphia as an example because I found some good public data.) The datasources I used to send context to Gemini were a Looker report that has a few columns related to car crashes in Philadelphia for 2023, Ticketmaster events occurring for the following week, and weather for the following week. 

Parts of the code were generated using Gemini 1.5 Pro and Anthropic Claude Sonnet 3.5.

<img width="1064" alt="image" src="https://github.com/user-attachments/assets/0b33a345-2747-4b93-96dd-f7e2b1a90613" />
