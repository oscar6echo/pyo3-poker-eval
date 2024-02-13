from timeit import default_timer as timer

import pytest

from pyo3_poker_eval import PokerEval

from . import is_dict_approx_equal


@pytest.fixture(scope="module")
def c():
    """"""
    t0 = timer()
    c = PokerEval()
    t1 = timer()
    print(f"PokerEval c runtime: {t1 - t0:.6f} s")
    return c


def test_stats_five(c):
    """"""
    stats = c.stats_five()

    target = {
        "high-card": {
            "nb_hand": 1277,
            "min_rank": 0,
            "max_rank": 1276,
            "nb_occur": 1302540,
        },
        "one-pair": {
            "nb_hand": 2860,
            "min_rank": 1277,
            "max_rank": 4136,
            "nb_occur": 1098240,
        },
        "two-pairs": {
            "nb_hand": 858,
            "min_rank": 4137,
            "max_rank": 4994,
            "nb_occur": 123552,
        },
        "three-of-a-kind": {
            "nb_hand": 858,
            "min_rank": 4995,
            "max_rank": 5852,
            "nb_occur": 54912,
        },
        "straight": {
            "nb_hand": 10,
            "min_rank": 5853,
            "max_rank": 5862,
            "nb_occur": 10200,
        },
        "flush": {
            "nb_hand": 1277,
            "min_rank": 5863,
            "max_rank": 7139,
            "nb_occur": 5108,
        },
        "full-house": {
            "nb_hand": 156,
            "min_rank": 7140,
            "max_rank": 7295,
            "nb_occur": 3744,
        },
        "four-of-a-kind": {
            "nb_hand": 156,
            "min_rank": 7296,
            "max_rank": 7451,
            "nb_occur": 624,
        },
        "straight-flush": {
            "nb_hand": 10,
            "min_rank": 7452,
            "max_rank": 7461,
            "nb_occur": 40,
        },
    }

    assert stats == target


def test_stats_seven(c):
    """"""
    stats = c.stats_seven()

    target = {
        "high-card": {
            "nb_hand": 407,
            "min_rank": 48,
            "max_rank": 1276,
            "nb_occur": 23294460,
        },
        "one-pair": {
            "nb_hand": 1470,
            "min_rank": 1295,
            "max_rank": 4136,
            "nb_occur": 58627800,
        },
        "two-pairs": {
            "nb_hand": 763,
            "min_rank": 4140,
            "max_rank": 4994,
            "nb_occur": 31433400,
        },
        "three-of-a-kind": {
            "nb_hand": 575,
            "min_rank": 5003,
            "max_rank": 5852,
            "nb_occur": 6461620,
        },
        "straight": {
            "nb_hand": 10,
            "min_rank": 5853,
            "max_rank": 5862,
            "nb_occur": 6180020,
        },
        "flush": {
            "nb_hand": 1277,
            "min_rank": 5863,
            "max_rank": 7139,
            "nb_occur": 4047644,
        },
        "full-house": {
            "nb_hand": 156,
            "min_rank": 7140,
            "max_rank": 7295,
            "nb_occur": 3473184,
        },
        "four-of-a-kind": {
            "nb_hand": 156,
            "min_rank": 7296,
            "max_rank": 7451,
            "nb_occur": 224848,
        },
        "straight-flush": {
            "nb_hand": 10,
            "min_rank": 7452,
            "max_rank": 7461,
            "nb_occur": 41584,
        },
    }

    assert stats == target


def test_rank_five(c):
    """"""
    input = {"hands": [[21, 33, 24, 22, 39], [51, 38, 14, 36, 17]]}
    ranks = c.rank_five(input)

    target = [2459, 3431]

    assert ranks == target


def test_rank_seven(c):
    """"""
    input = {"hands": [[50, 6, 0, 5, 38, 7, 17], [23, 16, 34, 26, 0, 10, 8]]}
    ranks = c.rank_seven(input)

    target = [5124, 1766]

    assert ranks == target


def test_game_det(c):
    """"""
    input = {"players": [[8, 29], [4, 11]], "table": [13, 14, 50, 22]}
    game_det = c.game_det(input)

    target = [
        {"win": 0.6363636363636364, "tie": 0.056818181818181816},
        {"win": 0.25, "tie": 0.056818181818181816},
    ]

    for g, t in zip(game_det, target):
        assert is_dict_approx_equal(g, t, precision=1e-8)


def test_game_mc(c):
    """"""
    input = {
        "players": [[8, 9], [11], []],
        "table": [15, 47, 23, 33],
        "nb_game": 100_000_000,
    }
    game_mc = c.game_mc(input)

    target = {"win": 0.1676863067074523, "tie": 0.0034908351396334054}

    assert is_dict_approx_equal(game_mc, target, precision=1e-3)
