# Knowledge Engine — Spotify

Projeto desenvolvido para a disciplina de **Lógica e Matemática Discreta**, com o objetivo de construir uma base de conhecimento utilizando dados e realizar consultas por meio da linguagem Prolog.


## 1. Dataset utilizado

O projeto utiliza um dataset contendo informações sobre músicas disponíveis no Spotify, incluindo dados sobre artistas, popularidade, seguidores, gêneros musicais e duração das faixas.

**Fonte do dataset:** https://www.kaggle.com/datasets/wardabilal/spotify-global-music-dataset-20092025

O arquivo original utilizado no projeto é `spotify_data.csv`.

### Características do dataset original

- **Quantidade de registros:** 8.582 músicas.
- **Quantidade de colunas:** 15.
- **Formato:** CSV.

## 2. Preparação e limpeza dos dados

A etapa de preparação dos dados foi implementada no arquivo `preparar_spotify.py`, utilizando Python e a biblioteca pandas.

O processo consiste nas seguintes operações:

1. Leitura do dataset original.
2. Seleção de 10 campos relevantes para o projeto.
3. Remoção de registros sem identificador, nome da música ou artista.
4. Tratamento dos gêneros musicais ausentes, substituindo-os por `desconhecido`.
5. Conversão e validação dos campos numéricos.
6. Padronização dos valores booleanos.
7. Remoção de registros com identificadores duplicados.
8. Exportação do dataset preparado.
9. Conversão dos registros em fatos Prolog.

### Campos selecionados

Foram selecionados 10 campos, incluindo variáveis qualitativas e quantitativas:

| Campo | Descrição | Tipo |
|---|---|---|
| `track_id` | Identificador da música | Qualitativo |
| `track_name` | Nome da música | Qualitativo |
| `artist_name` | Nome do artista | Qualitativo |
| `track_popularity` | Popularidade da música | Quantitativo |
| `artist_popularity` | Popularidade do artista | Quantitativo |
| `artist_followers` | Quantidade de seguidores do artista | Quantitativo |
| `artist_genres` | Gêneros musicais do artista | Qualitativo |
| `explicit` | Indica conteúdo explícito | Qualitativo |
| `album_type` | Tipo de lançamento | Qualitativo |
| `track_duration_min` | Duração da música em minutos | Quantitativo |

### Resultado da limpeza

| Métrica | Resultado |
|---|---|
| Registros originais | 8.582 |
| Registros após limpeza | 8.579 |
| Registros removidos | 3 |
| Colunas originais | 15 |
| Colunas selecionadas | 10 |
| Registros com gênero desconhecido | 3.358 |

O resultado do processamento é armazenado em `spotify_preparado.csv`.

## 3. Geração da base de conhecimento Prolog

Após a limpeza, o script Python converte automaticamente os registros do CSV preparado em fatos Prolog.

Cada música é representada pelo predicado `musica/10`, contendo os dez campos selecionados.

A estrutura de um fato é:

```prolog
musica(
    Id,
    Nome,
    Artista,
    PopularidadeMusica,
    PopularidadeArtista,
    Seguidores,
    Generos,
    Explicita,
    TipoAlbum,
    Duracao
).
```

O arquivo `spotify_base.pl` contém os 8.579 fatos resultantes do processamento.
