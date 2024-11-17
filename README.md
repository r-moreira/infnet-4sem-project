# DEEPLISTEN

## ⚠️ Avisos ao Professor: 
* Para este TP, refatorei todo o projeto para ter backend e frontend separados, portanto, não é possível fazer o deploy no Streamlit Community Cloud. 

* Dirija-se ao diretório `documents` para acessar o Data Summary Report e o Project Charter, os conteúdos estão em inglês pois pretendo utilizar para o meu portfólio.

* O projeto suporta o uso de LLM Local e através de API da Open AI. Para utilizar o LLM Local, é necessário setar a variável de ambiente `ENABLE_LOCAL_LLM=true`.

* Não é possível utilizar o docker com o LLM Local, pois o modelo é muito pesado e não é possível subir o container.

* Para rodar o projeto usando o LLM GPT-4o é necessário uma API Key da Open AI, que pode ser obtida em [Tutorial API Key Open AI](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/), posso disponibilizar a minha caso necessário. De qualquer forma, disponibilizei um print do chat em funcionamento no diretório `images`.

* Para rodar o projeto, é necessário setar as variáveis de ambiente `SPOTIFY_CLIENT_ID` e `SPOTIFY_CLIENT_SECRET` com as credenciais da API do Spotify. [Tutorial criação de APP Spotify](https://developer.spotify.com/documentation/general/guides/app-settings/).


## Project Description
The problem that the project aims to solve is to help ethnomusicology professionals access music information more easily and quickly using artificial intelligence, so they can conduct their research more efficiently, aiding in the cataloging and research of music from different cultures. It can also be used by people who enjoy music and want more detailed information about the songs they listen to.

The Spotify API will be used to bring data about artists, playlists, songs, and albums from around the world, in addition to scraping a site that contains song lyrics. The LLM will use this data to provide consolidated information.

## Technologies
The project will use the following technologies:
* Python
* Streamlit
* Spotify API
* Web scraping
* Machine Learning
* Natural Language Processing (NLP) (To Do)
* LLM (Large Language Model)
* Docker
* Database (To Do)

#### Project Structure:
```
├── backend
│   ├── src
│   ├── requirements.txt
│   └── Dockerfile
│   └── config.yml
├── frontend
│   ├── src
│   ├── requirements.txt
│   └── Dockerfile
├── data
│   ├── external
│   ├── processed
│   └── raw
├── models
├── notebooks
├── references
├── documents
├── images
├── src
│   └── pages
├── README.md
├── docker-compose.yml
├── .streamlit
│   ├── config.toml
│   └── secrets.toml
├── .gitignore
└── .env
```

## Running the Project
To run the project, follow these steps:

Environment Setup:
```bash
export SPOTIFY_CLIENT_ID=your_spotify_client_id
export SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
export OPEN_AI_API_KEY=your_openai_api_key
```

Run with Docker Compose (Recomended, but don't support local LLM):
```bash
docker-compose up --build
```

Run without Docker:

(Optional) Run with local LLM:
```bash
export ENABLE_LOCAL_LLM=true

# update max_tokens in backend/config.yml as needed
```

1. Set python version to 3.11.9:
```bash
pyenv local 3.11.9
```

2. Create a virtual environment for backend and frontend, activate and install the required libraries:
```bash
# From root directory
python3 -m venv backend/.venv

source backend/.venv/bin/activate

pip install -r backend/requirements.txt

# From root directory
python3 -m venv frontend/.venv

source frontend/.venv/bin/activate

pip install -r frontend/requirements.txt
```

3. Run applications:
```bash
# From root directory
streamlit run frontend/src/app.py

# From root directory
PYTHONPATH=./backend/src uvicorn backend.src.app:app --reload
```

## Accessing the Application
Access the application at http://localhost:8501
