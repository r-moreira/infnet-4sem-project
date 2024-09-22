# DEEPLISTEN

## ⚠️ Avisos ao Professor: 

* Dirija-se ao notebook `genius_webscrapping` dentro do diretório ```./notebook``` para acessar o código de webscrapping utilizado para gerar o arquivo para upload no streamlit.

* Dirija-se ao diretório `documents` para acessar o Data Summary Report e o Project Charter, os conteúdos estão em inglês pois pretendo utilizar para o meu portfólio.
  
* Dirija-se ao diretório `data/processed` para acessar os arquivos de dados processados através de webscrapping para upload no streamlit.
 
* Para testar o chat é necessário uma API Key da Open AI, que pode ser obtida em [Tutorial como criar API Key](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/), posso disponibilizar a minha caso necessário. De quaquer forma, disponibilizei um print do chat em funcionamento no diretório `images`.

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
├── requirements.txt
├── Dockerfile
├── .gitignore
└── .env
```

## Running the Project
To run the project, follow these steps:

1. Set python version to 3.11.9:
```bash
pyenv local 3.11.9
```

2. Create a virtual environment:
```bash
python -m venv venv

source venv/bin/activate
```

3. Install the required libraries:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit application:
```bash
streamlit run src/app.py
```

5. (Optional) Run with Docker:
```bash
docker-compose up --build
```