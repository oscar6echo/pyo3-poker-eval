def test_doc() -> None:
    import pyo3_poker_eval

    rust_doc = "BlackScholes option pricing implemented in Rust and exposed to Python with PyO3."
    assert pyo3_poker_eval.__doc__ == rust_doc
