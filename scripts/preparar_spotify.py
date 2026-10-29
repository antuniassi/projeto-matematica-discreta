import pandas as pd
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

PASTA_DADOS = RAIZ / "dados"
PASTA_PROLOG = RAIZ / "prolog"

PASTA_DADOS.mkdir(exist_ok=True)
PASTA_PROLOG.mkdir(exist_ok=True)

# Arquivo de entrada
if len(sys.argv) > 1:
    arquivo_entrada = Path(sys.argv[1]).resolve()
else:
    arquivo_entrada = PASTA_DADOS / "spotify_data.csv"

# Arquivos de saida
arquivo_csv = PASTA_DADOS / "spotify_preparado.csv"
arquivo_prolog = PASTA_PROLOG / "spotify_base.pl"



# Leitura do dataset original

df = pd.read_csv(arquivo_entrada)

print("Registros originais:", len(df))
print("Colunas originais:", len(df.columns))



# Seleção dos 10 campos

colunas = [
    "track_id",
    "track_name",
    "artist_name",
    "track_popularity",
    "artist_popularity",
    "artist_followers",
    "artist_genres",
    "explicit",
    "album_type",
    "track_duration_min"
]

df = df[colunas].copy()


# Limpeza dos dados ausentes

# Remove registros sem ID, música ou artista
df = df.dropna(
    subset=["track_id", "track_name", "artist_name"]
)

# Remove registros com textos vazios
for coluna in ["track_id", "track_name", "artist_name"]:
    df[coluna] = df[coluna].astype(str).str.strip()
    df = df[df[coluna] != ""]

# Preenche gêneros ausentes
df["artist_genres"] = (
    df["artist_genres"]
    .fillna("desconhecido")
    .astype(str)
    .str.strip()
)

df.loc[
    df["artist_genres"] == "",
    "artist_genres"
] = "desconhecido"

# Preenche tipos de álbum ausentes
df["album_type"] = (
    df["album_type"]
    .fillna("desconhecido")
    .astype(str)
    .str.strip()
)


# Tratamento de campos numéricos

colunas_numericas = [
    "track_popularity",
    "artist_popularity",
    "artist_followers",
    "track_duration_min"
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )

# Remove registros com números inválidos
df = df.dropna(subset=colunas_numericas)

# Remove valores negativos
df = df[
    (df["track_popularity"] >= 0) &
    (df["artist_popularity"] >= 0) &
    (df["artist_followers"] >= 0) &
    (df["track_duration_min"] > 0)
]

# Popularidade deve estar entre 0 e 100
df = df[
    (df["track_popularity"] <= 100) &
    (df["artist_popularity"] <= 100)
]

# Converte números inteiros
for coluna in [
    "track_popularity",
    "artist_popularity",
    "artist_followers"
]:
    df[coluna] = df[coluna].astype(int)

# Padroniza duração
df["track_duration_min"] = (
    df["track_duration_min"].round(2)
)


# Tratamento de valores booleanos

# Converte explicit para true ou false
df["explicit"] = (
    df["explicit"]
    .astype(str)
    .str.strip()
    .str.lower()
)

valores_validos = {
    "true": True,
    "false": False,
    "1": True,
    "0": False
}

df["explicit"] = df["explicit"].map(valores_validos)

# Remove valores desconhecidos
df = df.dropna(subset=["explicit"])

df["explicit"] = df["explicit"].astype(bool)


# Remove duplicatas

# Cada track_id deve identificar uma unica música
df = df.drop_duplicates(subset=["track_id"])

df = df.reset_index(drop=True)


# Salva csv limpo

df.to_csv(
    arquivo_csv,
    index=False,
    encoding="utf-8-sig"
)

print("\nLIMPEZA CONCLUIDA")
print("Registros finais:", len(df))
print("Colunas finais:", len(df.columns))

print(
    "Generos desconhecidos:",
    (df["artist_genres"] == "desconhecido").sum()
)


# Converte valores para prolog

def texto_prolog(valor):
    texto = str(valor)
    texto = texto.replace("\\", "\\\\")
    texto = texto.replace("'", "''")
    return f"'{texto}'"


def booleano_prolog(valor):
    return "true" if valor else "false"


# Gera base de conhecimento prolog

with open(
    arquivo_prolog,
    "w",
    encoding="utf-8"
) as arquivo:

    arquivo.write(
        "% Base de conhecimento Spotify\n"
    )

    arquivo.write(
        "% Gerada automaticamente com Python\n\n"
    )

    for _, linha in df.iterrows():

        fato = (
            "musica("
            f"{texto_prolog(linha['track_id'])}, "
            f"{texto_prolog(linha['track_name'])}, "
            f"{texto_prolog(linha['artist_name'])}, "
            f"{linha['track_popularity']}, "
            f"{linha['artist_popularity']}, "
            f"{linha['artist_followers']}, "
            f"{texto_prolog(linha['artist_genres'])}, "
            f"{booleano_prolog(linha['explicit'])}, "
            f"{texto_prolog(linha['album_type'])}, "
            f"{linha['track_duration_min']}"
            ").\n"
        )

        arquivo.write(fato)


print("\nARQUIVOS GERADOS:")
print(arquivo_csv)
print(arquivo_prolog)

print("\nProcesso finalizado com sucesso!")
