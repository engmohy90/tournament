#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def commit(sql, data1=None, data2=None):
    """store in data base function"""
    conn = connect()
    c = conn.cursor()
    if data1 is None and data2 is None:
        c.execute(sql)
        conn.commit()
        conn.close()
    if data1 is not None and data2 is not None:
        c.execute(sql % (data1, data2))
        conn.commit()
        conn.close()
    if data2 is None and data1 is not None:
        c.execute(sql % data1)
        conn.commit()
        conn.close()


def fetch_all(sql, data1=None, data2=None):
    conn = connect()
    c = conn.cursor()
    if data1 is None and data2 is None:
        c.execute(sql)
        data = c.fetchall()
        conn.close()
        return data
    if data1 is not None and data2 is not None:
        c.execute(sql % (data1, data2))
        data = c.fetchall()
        conn.close()
        return data

    if data2 is None and data1 is not None:
        c.execute(sql % data1)
        data = c.fetchall()
        conn.close()
        return data


def deleteMatches():
    """Remove all the match records from the database."""

    commit("TRUNCATE record")
    commit("TRUNCATE match")


def deletePlayers():
    """Remove all the player records from the database."""

    commit("TRUNCATE players RESTART IDENTITY")


def countPlayers():
    """Returns the number of players currently registered."""

    num = fetch_all("SELECT count(player_id) as num from players")
    return num[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players values(%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    stand_table = fetch_all("SELECT * FROM all_record")
    return stand_table


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # record the winner points and number of played match
    winner_p = fetch_all("SELECT points FROM record WHERE player_id = %d",
                         winner)
    if winner_p == []:
        commit("INSERT INTO record VALUES (1,%d)", winner)
    else:
        wpoint = winner_p[0][0] + 1
        commit("UPDATE record SET points=%d WHERE player_id = %d",
               wpoint, winner)

    win_m = fetch_all("SELECT match_played FROM match WHERE player_id = %d",
                      winner)
    if win_m == []:
        commit("INSERT INTO match VALUES (1,%d)", winner)
    else:
        wmatch_played = winner_p[0][0] + 1
        commit("UPDATE match SET match_played=%d WHERE player_id=%d",
               wmatch_played, winner)

    # record the number of match loser played
    loser_p = fetch_all("SELECT match_played FROM match WHERE player_id=%d",
                        loser)
    if loser_p == []:
        commit("INSERT INTO match VALUES (1,%d)", loser)
    else:
        lmatch_played = loser_p[0][0] + 1
        commit("UPDATE match SET match_played=%d WHERE player_id=%d",
               lmatch_played, loser)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player
    adjacent to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    all_player = playerStandings()
    paired = []
    for x in range(0, countPlayers()-1, 2):
        paired.append(all_player[x][:2]+all_player[x+1][:2])
    return paired
