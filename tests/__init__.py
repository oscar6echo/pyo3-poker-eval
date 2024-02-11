# import sys
# from pathlib import Path

# # test dev
# f_dev = Path(__file__).parent.parent.resolve()
# sys.path.insert(0, str(f_dev))


def is_dict_approx_equal(d1, d2, precision=1e-6):
    """"""

    if len(d1) != len(d2):
        return False

    for k, v in d1.items():
        if k not in d2:
            return False

        # approx
        if isinstance(v, float) and isinstance(d2[k], float):
            if not abs(v - d2[k]) < precision:
                return False

        # recursive
        elif isinstance(v, dict):
            if not is_dict_approx_equal(v, d2[k], precision):
                return False

        # default
        elif v != d2[k]:
            return False

    return True
