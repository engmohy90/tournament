#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def commit(psql):
    """store in data base function"""
    conn = connect()
    c = conn.cursor()
    c.execute(psql)
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""

    commit("update players set points = 0")
    commit("update players set match_played  = 0")


def deletePlayers():
    """Remove all the player records from the database."""

    commit("truncate players restart identity")


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("select count(player_id) as num from players")
    num = c.fetchone()
    conn.close()
    return num[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()
    c.execute("insert into players values(%s)", (name,))
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

    conn = connect()
    c = conn.cursor()
    c.execute("select player_id,name,points,match_played  from players")
    stand_table = c.fetchall()
    conn.close()
    return stand_table


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    c.execute("select points,match_played from players where player_id = %d"
              % winner)
    winner_p = c.fetchall()
    wpoint = winner_p[0][0] + 1
    wmatch_played = winner_p[0][1] + 1
    c.execute("update players set points = %d where player_id = %d"
              % (wpoint, winner))
    c.execute("update players set match_played  = %d where player_id = %d"
              % (wmatch_played, winner))
    c.execute("select match_played from players where player_id = %d" % loser)
    loser_p = c.fetchone()
    lmatch_played = loser_p[0] + 1
    c.execute("update players set match_played  = %d where player_id = %d"
              % (lmatch_played, loser))
    conn.commit()
    conn.close()


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

    conn = connect()
    c = conn.cursor()
    max_match = math.log(countPlayers(), 2)
    c.execute("select max(points),min(points) from players")
    winner = c.fetchall()
    if winner[0][0] == max_match:
        d = "the tournament ended"
        return d
    else:
        c.execute("select player_id , name from players order by points")
        all_player = c.fetchall()
        paired = []
        for x in range(0, countPlayers()-1, 2):
            paired.append(all_player[x]+all_player[x+1])
        return paired
