use pyo3::prelude::*;

mod poker;

/// BlackScholes option pricing implemented in Rust and exposed to Python with PyO3.
#[pymodule]
fn _rust(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    let mod_poker = PyModule::new(py, "poker")?;
    mod_poker.add_class::<poker::PokerEval>()?;
    m.add_submodule(mod_poker)?;

    Ok(())
}
