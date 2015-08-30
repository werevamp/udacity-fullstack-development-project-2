#!/usr/bin/env python
"""tournament.py -- implementation of a Swiss-system tournament"""

import psycopg2
import math
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def delete_matches():
    """Remove all the match records from the database."""

    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def delete_players():
    """Remove all the player records from the database."""

    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def count_players():
    """Returns the number of players currently registered."""

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT count(*) as num FROM players")
    count = cur.fetchone()
    conn.close()

    return count[0]


def register_player(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()


def initialize_players():
    """Adds players to the game"""
    register_player('albert')
    register_player('chris')
    register_player('mike')
    register_player('dylan')
    register_player('hylan')
    register_player('lauren')
    register_player('jazz')
    register_player('judith')


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    """
    [(id, name, wins, matches), (id, name, wins, matches), (id, name, wins, matches)]
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("\
        SELECT players.id, players.name,\
               coalesce(winners.wins, 0), coalesce(matches_amount.matches, 0)\
        FROM players\
        LEFT JOIN (\
                SELECT winner, count(winner) AS wins\
                FROM matches\
                GROUP BY winner\
        ) AS winners\
        ON players.id = winners.winner\
        LEFT JOIN (\
                SELECT players.id, count(players.id) AS matches\
                FROM players\
                JOIN matches\
                ON players.id = matches.winner\
                        OR players.id = matches.loser\
                GROUP BY players.id\
        ) AS matches_amount\
        ON players.id = matches_amount.id\
        ORDER BY winners.wins DESC NULLS LAST\
    ")
    query_results = cur.fetchall()
    conn.close()

    return query_results

def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO matches(winner, loser) VALUES (%s, %s)", (winner, loser,))
    conn.commit()
    conn.close()

    return winner


def swiss_pairings():
    """Swiss pairing is a sorting algorithm that allows players to be matched
    for the next round"""

    paired_players = []
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    """
        get a database connection
        have it sort the players by the most wins
        have it return a list of players
    """

    """needs to return a list of tuples
    [(id1, name1, id2, name2),
     (id2, name2, id2, name2),
     ...,
     (id2, name2, id2, name2)
    ]
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("\
        SELECT players.id, players.name\
        FROM (\
            SELECT winner, count(*) AS wins\
            FROM matches GROUP BY winner\
        ) AS matches\
        RIGHT JOIN players\
        ON players.id = matches.winner\
        ORDER BY matches.wins DESC NULLS LAST\
    ")
    query_results = cur.fetchall()
    conn.close()

    print query_results
    loop_amount = len(query_results) / 2
    paired_players = []
    for n in range(loop_amount):
        pair = query_results[0::2][n] + query_results[1::2][n]
        paired_players.append(pair)

    return paired_players


def enough_players():
    """Checks if there are enough players to play the game"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT count(*) as player_count FROM players");
    player_count = cur.fetchall()
    conn.close()

    print player_count[0][0]


def set_rounds():

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT count(*) as player_count FROM players");
    player_count = cur.fetchall()
    conn.close()
    return int(math.log(player_count[0][0], 2))


def start_game():
    """This functions starts the game"""

    initialize_players()
    #enough_players()
    #rounds_amount = set_rounds()
    #loop_through_rounds(rounds_amount)
    player_standings()


def loop_through_rounds(rounds_amount):
    """Loops through all the matches"""

    for n in range(rounds_amount):
        paired_players = swiss_pairings()
        loop_through_matches(paired_players)


def loop_through_matches(paired_players):
    """loops through all the matches in each round"""

    for pair in paired_players:
        selected_winner = bool(random.getrandbits(1))

        if(selected_winner):
            report_match(pair[0], pair[2])
        else:
            report_match(pair[2], pair[0])


def start_matches():

    for n in range(4):
        print n


def end_game():
    """This function Ends the game"""
    delete_players()
    delete_matches()


#start_game()
#end_game()
