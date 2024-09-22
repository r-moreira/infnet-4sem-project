# Project Charter

## Business background

* **Client**: Researchers and enthusiasts in the field of ethnomusicology.
* **Business domain**: Music research and cataloging.
* **Business problems**: Difficulty in accessing and consolidating detailed information about music from different cultures quickly and efficiently.

## Scope

* **Data science solutions**: 
  * Build an application that uses AI to provide detailed information about music, including artist data, playlists, albums, and song lyrics.
  * Integrate Spotify API and web scraping for lyrics to gather comprehensive music data.
* **What will we do**:
  * Develop a user-friendly interface for searching and retrieving music information.
  * Implement AI models to analyze and interpret music data.
* **Consumption by customer**:
  * The application will be used by ethnomusicologists and music enthusiasts to access detailed music information for research and personal interest.

## Personnel

* **Project Team**:
  * Rodrigo Avila - Project Manager, Data Scientist and Developer
* **Client/Stakeholders**:
  * **Researchers in ethnomusicology**: Primary users who will benefit from detailed music information for their research.
  * **Music enthusiasts**: Individuals interested in exploring and learning about music from different cultures.
  * **Academic institutions**: Universities and colleges offering courses in ethnomusicology and music studies.
  * **Music libraries and archives**: Organizations that catalog and preserve music data.
  * **Cultural organizations**: Groups focused on preserving and promoting cultural heritage through music.
  * **Developers and data scientists**: Professionals involved in the development and maintenance of the application.
  * **Music streaming services**: Companies like Spotify that may collaborate or integrate with the application.
  * **Investors and sponsors**: Entities providing financial support for the project.


## Metrics

* **Qualitative objectives**:
  * Provide quick and accurate music information.
  * Ensure ease of use and intuitive navigation for users.
* **Quantifiable metrics**:
  * Reduce the time taken to retrieve music information from researchers.
  * Achieve a user satisfaction rate of 90% based on feedback.
* **Improvement targets**:
  * Increase the accuracy of music data retrieval by 30%.
* **Baseline values**:
  * Current user satisfaction rate: Unknown.
* **Measurement methods**:
  * Collect user feedback through surveys and usage analytics.

## Plan

* **Phases**:
  * **Phase 1**: Requirements gathering and initial design (2 weeks)
  * **Phase 2**: Development of core features and integration with Spotify API (1 month)
  * **Phase 3**: Implementation of AI models and web scraping for lyrics (1 month)
  * **Phase 4**: Testing and user feedback collection (2 weeks)
  * **Phase 5**: Final adjustments and deployment (1 month)

## Architecture

* **Data**:
  * Expected data: Artist data, playlists, albums, and song lyrics from Spotify API and web scraping.
* **Data movement**:
  * Data will be moved from Spotify API and web scraping sources to the application database.
* **Tools and resources**:
  * Python for data processing and AI model development.
  * Streamlit for web application development.
  * Docker for containerization.
  * Database for storing music data.
* **Consumption of web services**:
  * The application will provide APIs for retrieving music information.
  * Users will interact with the application through a web interface.
* **Data flow and decision architecture**:
  * A diagram will be created to show the end-to-end data flow from data sources to the user interface during development.

## Communication

* **Meetings**:
  * Meetings to discuss progress and address any issues.
* **Contact persons**:
  * INFNET Professor: Diego Rodrigues
