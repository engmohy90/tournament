#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("truncate matchsrecord restart identity")
    c.execute("truncate numplayed restart identity")

    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("truncate players restart identity")
    conn.commit()
    conn.close()

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
    c.execute("insert into players values(%s)",(name,))
    conn.commit()
    conn.close()


def playerStandings():
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
    conn = connect()
    c = conn.cursor()
    c.execute("select players.player_id,players.name,matchsrecord.points,numplayed.mplayed from players left join matchsrecord on players.player_id=matchsrecord.player_id left join numplayed on matchsrecord.player_id=numplayed.player_id;")
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
    c.execute("select points from matchsrecord where player_id = %d " % winner)

    number_win = c.fetchone()
    if number_win is not None:

        n = number_win[0] + 1
        c.execute("update matchsrecord set points = %d where player_id = %d"%(n,winner))
    if number_win is None:
        c.execute("insert into matchsrecord values(%d,1)" % winner)


    c.execute("select mplayed from numplayed where player_id = %d " % winner)
    countwi = c.fetchone()
    if countwi is None :
        c.execute("insert into numplayed values (%d,1)" % winner)
    else:
        countwp = countwi[0] + 1
        c.execute("update numplayed set mplayed = %d where player_id = %d " % (countwp, winner))
        
    c.execute("select mplayed from numplayed where player_id = %d " % loser)
    countlo = c.fetchone()
    if countlo is None :
        c.execute("insert into numplayed values (%d,1)" % loser)   
    else :
        countlp = countlo[0] + 1
        c.execute("update numplayed set mplayed = %d where player_id = %d " % (countlp, loser))


    conn.commit()

    conn.close()

def swissPairings():
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


# x = raw_input("enter player name")
# registerPlayer(x)

# reportMatch(5,4)
# conn = connect()
# c = conn.cursor()
# c.execute("select * from matchsrecord")
# print "id , point", c.fetchall()
# c.execute("select * from numplayed")
# print "played , id", c.fetchall()

# conn.close()

print playerStandings()

# print countPlayers()
# print "ok"
