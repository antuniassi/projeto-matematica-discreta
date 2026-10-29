# Knowledge Engine — Spotify

Projeto desenvolvido para a disciplina de **Lógica e Matemática Discreta**, com o objetivo de construir uma base de conhecimento a partir de dados e responder perguntas utilizando **Prolog e Lógica de Primeira Ordem**.

## 1. Dataset

O projeto utiliza dados de músicas do Spotify, incluindo informações sobre artistas, popularidade, seguidores, gêneros musicais e duração.

**Fonte:** [Spotify Global Music Dataset (2009–2025) — Kaggle](https://www.kaggle.com/datasets/wardabilal/spotify-global-music-dataset-20092025)

**Arquivo original:** `dados/spotify_data.csv`

O dataset utilizado possui **8.582 registros e 15 colunas**.

## 2. Preparação dos dados

A preparação foi realizada pelo script `scripts/preparar_spotify.py`, utilizando **Python e pandas**.

O processamento inclui:

1. Seleção de 10 campos qualitativos e quantitativos.
2. Remoção de registros sem identificador, música ou artista.
3. Substituição de gêneros ausentes por `desconhecido`.
4. Validação de valores numéricos e booleanos.
5. Remoção de identificadores duplicados.
6. Exportação do CSV preparado e geração dos fatos Prolog.

### Campos selecionados

| Campo | Descrição | Tipo |
|---|---|---|
| `track_id` | Identificador da música | Qualitativo |
| `track_name` | Nome da música | Qualitativo |
| `artist_name` | Nome do artista | Qualitativo |
| `track_popularity` | Popularidade da música | Quantitativo |
| `artist_popularity` | Popularidade do artista | Quantitativo |
| `artist_followers` | Seguidores do artista | Quantitativo |
| `artist_genres` | Gêneros musicais | Qualitativo |
| `explicit` | Conteúdo explícito | Qualitativo |
| `album_type` | Tipo de lançamento | Qualitativo |
| `track_duration_min` | Duração em minutos | Quantitativo |

**Resultado:** 8.579 músicas válidas, 10 campos e 3.358 registros com gênero desconhecido.

O dataset preparado é salvo em `dados/spotify_preparado.csv`.

## 3. Base de conhecimento Prolog

O script Python converte os registros preparados em **8.579 fatos Prolog**, armazenados em `prolog/spotify_base.pl`.

Cada música é representada pelo predicado `musica/10`:

```prolog
musica(Id, Nome, Artista, PopularidadeMusica,
       PopularidadeArtista, Seguidores, Generos,
       Explicita, TipoAlbum, Duracao).
```

As regras e consultas estão implementadas em `prolog/consultas.pl`.

## 4. Perguntas implementadas

Foram implementadas três perguntas sofisticadas em Prolog, utilizando agrupamento, agregação, comparação e ordenação dos dados.

### Pergunta 1 — Artista com maior popularidade média

**Qual artista possui a maior média de popularidade de suas músicas, considerando apenas artistas com pelo menos 5 músicas cadastradas?**

A consulta agrupa as músicas por artista, calcula a popularidade média, filtra artistas com menos de cinco músicas e identifica a maior média.

```prolog
?- artista_maior_media(Artista, Media),
   quantidade_musicas(Artista, Quantidade).
```

**Resultado:**

- **Artista:** Alex Warren
- **Popularidade média:** 83,40
- **Quantidade de músicas:** 5

O limite mínimo de cinco músicas foi escolhido para reduzir a influência de artistas com poucos registros, mantendo uma análise abrangente. Com esse critério, 336 artistas são elegíveis.

### Pergunta 2 — Artistas com mais músicas

**Quais são os cinco artistas com mais músicas cadastradas no dataset?**

A consulta conta as músicas por artista e organiza os resultados em ordem decrescente.

```prolog
?- top_5_artistas(Top5).
```

**Resultado:**

| Posição | Artista | Músicas |
|---|---|---:|
| 1º | Taylor Swift | 324 |
| 2º | The Weeknd | 141 |
| 3º | Lana Del Rey | 99 |
| 4º | Ariana Grande | 94 |
| 5º | Nirvana | 91 |

Taylor Swift possui a maior quantidade de músicas cadastradas, com 324 registros.

### Pergunta 3 — Gênero musical com maior popularidade média

**Qual gênero musical possui a maior média de popularidade, considerando apenas gêneros associados a pelo menos 30 músicas?**

A consulta separa os gêneros associados a cada música, elimina gêneros desconhecidos, calcula a média de popularidade por gênero e ordena os resultados.

O limite de 30 músicas foi escolhido para reduzir a influência de gêneros pouco representados. Com esse critério, 73 gêneros são elegíveis, enquanto um limite de cinco músicas incluiria 212 gêneros.

```prolog
?- genero_maior_media(Genero, Media),
   quantidade_musicas_genero(Genero, Quantidade).
```

**Resultado:**

- **Gênero:** electropop
- **Popularidade média:** 73,89
- **Quantidade de músicas:** 61

**Ranking dos cinco gêneros com maiores médias:**

```prolog
?- top_5_generos(Top5).
```

| Posição | Gênero | Popularidade média |
|---|---|---:|
| 1º | Electropop | 73,89 |
| 2º | Dark pop | 73,89 |
| 3º | Trap latino | 73,53 |
| 4º | Urbano latino | 73,05 |
| 5º | Reggaeton | 71,94 |

Electropop e dark pop apresentaram a mesma maior média de popularidade (73,89). Como a ordenação considera também o nome do gênero em caso de empate, electropop aparece na primeira posição do ranking.

Uma música pode estar associada a múltiplos gêneros e, portanto, participar do cálculo de cada um deles.

### Validação da base

Para verificar a quantidade total de fatos carregados no Prolog:

```prolog
?- aggregate_all(count, musica(_,_,_,_,_,_,_,_,_,_), Total).
```

**Resultado:** `Total = 8579`, confirmando o carregamento dos 8.579 registros preparados.

## 5. Estrutura do projeto

```text
projeto-matematica-discreta/
├── dados/
│   ├── spotify_data.csv
│   └── spotify_preparado.csv
├── scripts/
│   └── preparar_spotify.py
├── prolog/
│   ├── spotify_base.pl
│   └── consultas.pl
├── README.md
└── requirements.txt
```

## 6. Como executar

### Pré-requisitos

- Python 3
- SWI-Prolog

### Instalar dependências

Na raiz do projeto:

```bash
python -m pip install -r requirements.txt
```

### Preparar os dados

```bash
python scripts/preparar_spotify.py
```

O script gera `dados/spotify_preparado.csv` e `prolog/spotify_base.pl`.

### Executar as consultas

Inicie o SWI-Prolog:

```bash
swipl -s prolog/consultas.pl
```

No interpretador, execute as perguntas:

```prolog

?- artista_maior_media(Artista, Media),
   quantidade_musicas(Artista, Quantidade).

?- top_5_artistas(Top5).

?- genero_maior_media(Genero, Media),
   quantidade_musicas_genero(Genero, Quantidade).
```

Para verificar a quantidade de fatos carregados:

```prolog
?- aggregate_all(count, musica(_,_,_,_,_,_,_,_,_,_), Total).
```

**Resultado esperado:** `Total = 8579`.

## 7. Observações

- Os resultados representam somente as músicas presentes no dataset, não todo o catálogo do Spotify.
- Gêneros ausentes foram identificados como `desconhecido`.
- A popularidade média é calculada a partir dos valores disponíveis no dataset.
- Todo o processamento dos dados é feito em Python, enquanto as regras e consultas são implementadas em Prolog.