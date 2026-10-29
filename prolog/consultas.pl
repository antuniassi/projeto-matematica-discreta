:- consult('spotify_base.pl').

% Identifica artistas
artista(Artista) :-
    musica(_, _, Artista, _, _, _, _, _, _, _).


% Calcula a popularidade media de um artista
media_popularidade(Artista, Media) :-
    findall(
        Popularidade,
        musica(_, _, Artista, Popularidade, _, _, _, _, _, _),
        Lista
    ),
    Lista \= [],
    sum_list(Lista, Soma),
    length(Lista, Quantidade),
    Media is Soma / Quantidade.


% Conta as musicas de um artista
quantidade_musicas(Artista, Quantidade) :-
    findall(
        Id,
        musica(Id, _, Artista, _, _, _, _, _, _, _),
        Lista
    ),
    length(Lista, Quantidade).


% Encontra a maior media entre artistas que possuem pelo menos 5 musicas
artista_maior_media(Artista, Media) :-
    setof(
        MediaAtual-Nome,
        (
            artista(Nome),
            quantidade_musicas(Nome, Quantidade),
            Quantidade >= 5,
            media_popularidade(Nome, MediaAtual)
        ),
        ListaOrdenada
    ),
    last(ListaOrdenada, Media-Artista).


% Conta quantos artistas tem a quantidade de musicas maior ou igual ao pedido
contar_artistas_elegiveis(Minimo, Total) :-
    setof(Artista, artista(Artista), Artistas),
    findall(
        Nome,
        (
            member(Nome, Artistas),
            quantidade_musicas(Nome, Quantidade),
            Quantidade >= Minimo
        ),
        Elegiveis
    ),
    length(Elegiveis, Total).


% Gera uma lista com todos os artistas e suas quantidades de musicas, 
% ordenada da maior para a menor quantidade.
ranking_artistas(Ranking) :-
    setof(
        Quantidade-Artista,
        (
            artista(Artista),
            quantidade_musicas(Artista, Quantidade)
        ),
        ListaOrdenada
    ),
    reverse(ListaOrdenada, Ranking).


% Retorna os 5 artistas com mais musicas no dataset.
top_5_artistas(Top5) :-
    ranking_artistas(Ranking),
    length(Top5, 5),
    append(Top5, _, Ranking).


% Separa os generos associados a cada musica.
% Ignora generos desconhecidos.
genero_musica(Genero, Popularidade) :-
    musica(_, _, _, Popularidade, _, _, Generos, _, _, _),
    atom_string(Generos, Texto),
    split_string(Texto, ",", " ", Lista),
    member(Item, Lista),
    normalize_space(string(GeneroTexto), Item),
    GeneroTexto \= "",
    GeneroTexto \= "desconhecido",
    atom_string(Genero, GeneroTexto).


% Gera uma lista sem generos repetidos.
lista_generos(Generos) :-
    setof(
        Genero,
        Popularidade^genero_musica(Genero, Popularidade),
        Generos
    ).


% Conta quantas musicas pertencem a um genero.
quantidade_musicas_genero(Genero, Quantidade) :-
    findall(
        Popularidade,
        genero_musica(Genero, Popularidade),
        Lista
    ),
    length(Lista, Quantidade).


% Calcula a popularidade media das musicas de um genero.
media_popularidade_genero(Genero, Media) :-
    findall(
        Popularidade,
        genero_musica(Genero, Popularidade),
        Lista
    ),
    Lista \= [],
    sum_list(Lista, Soma),
    length(Lista, Quantidade),
    Media is Soma / Quantidade.


% Conta quantos generos possuem pelo menos
% uma quantidade minima de musicas.
contar_generos_elegiveis(Minimo, Total) :-
    lista_generos(Generos),
    findall(
        Genero,
        (
            member(Genero, Generos),
            quantidade_musicas_genero(Genero, Quantidade),
            Quantidade >= Minimo
        ),
        Elegiveis
    ),
    length(Elegiveis, Total).


% Monta o ranking dos generos.
% Calcula as estatisticas uma vez por genero.
% Considera apenas generos com pelo menos 30 musicas.
ranking_generos(Ranking) :-
    lista_generos(Generos),
    findall(
        Media-Genero,
        (
            member(Genero, Generos),
            findall(
                Popularidade,
                genero_musica(Genero, Popularidade),
                Lista
            ),
            length(Lista, Quantidade),
            Quantidade >= 30,
            sum_list(Lista, Soma),
            Media is Soma / Quantidade
        ),
        Resultados
    ),
    sort(Resultados, ListaOrdenada),
    reverse(ListaOrdenada, Ranking).


% Retorna o genero com a maior media de popularidade.
genero_maior_media(Genero, Media) :-
    ranking_generos([Media-Genero | _]).


% Retorna os cinco generos com maiores medias.
top_5_generos(Top5) :-
    ranking_generos(Ranking),
    length(Top5, 5),
    append(Top5, _, Ranking).
