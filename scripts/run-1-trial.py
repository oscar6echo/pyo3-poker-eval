from timeit import default_timer as timer

from pyo3_poker_eval import PokerEval

t0 = timer()
c = PokerEval()
t1 = timer()
print(f"PokerEval init runtime: {t1 - t0:.6f} s")

# stats

t0 = timer()
print("stats_five")
stats_five = c.stats_five()
print(stats_five)
t1 = timer()
print(f"stats_five runtime: {t1 - t0:.6f} s")

t0 = timer()
print("stats_seven")
stats_seven = c.stats_seven()
print(stats_seven)
t1 = timer()
print(f"stats_seven runtime: {t1 - t0:.6f} s")


# ranks

t0 = timer()
print("rank_five")
input = {"hands": [[21, 33, 24, 22, 39], [51, 38, 14, 36, 17]]}
rank_five = c.rank_five(input)
print(rank_five)
t1 = timer()
print(f"rank_five runtime: {t1 - t0:.6f} s")

t0 = timer()
print("rank_seven")
input = {"hands": [[50, 6, 0, 5, 38, 7, 17], [23, 16, 34, 26, 0, 10, 8]]}
rank_seven = c.rank_seven(input)
print(rank_seven)
t1 = timer()
print(f"rank_seven runtime: {t1 - t0:.6f} s")

# game deterministic

t0 = timer()
print("game_det")
input = {"players": [[8, 29], [4, 11]], "table": [13, 14, 50, 22]}
game_det = c.game_det(input)
print(game_det)
t1 = timer()
print(f"game_det runtime: {t1 - t0:.6f} s")

# game monte carlo

t0 = timer()
print("game_mc")
input = {
    "players": [[8, 9], [11], []],
    "table": [15, 47, 23, 33],
    "nb_game": 100_000_000,
}
game_mc = c.game_mc(input)
print(game_mc)
t1 = timer()
print(f"game_mc runtime: {t1 - t0:.6f} s")
