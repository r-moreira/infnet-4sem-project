# DEEPLISTEN

## ⚠️ Avisos ao Professor: 

* Dirija-se ao notebook `genius_webscrapping` dentro do diretório ```./notebook``` para acessar o código de webscrapping utilizado para gerar o arquivo para upload no streamlit.

* Dirija-se ao diretório `documents` para acessar o Data Summary Report e o Project Charter, os conteúdos estão em inglês pois pretendo utilizar para o meu portfólio.
  
* Dirija-se ao diretório `data/processed` para acessar os arquivos de dados processados através de webscrapping para upload no streamlit.
 
* Para testar o chat é necessário uma API Key da Open AI, que pode ser obtida em [Tutorial como criar API Key](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/), posso disponibilizar a minha caso necessário. De qualquer forma, disponibilizei um print do chat em funcionamento no diretório `images`.

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
* Natural Language Processing (NLP)
* LLM (Large Language Model)
* Docker
* Database

#### Project Structure:
```
├── backend
│   ├── src
│   ├── requirements.txt
│   └── Dockerfile
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
├── .gitignore
└── .env
```

## Running the Project
To run the project, follow these steps:

0. (Optional) Run with Docker Compose:
```bash
docker-compose up --build
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
uvicorn backend.src.app:app --reload