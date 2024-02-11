use std::{collections::HashMap, sync::Arc};

use pyo3::{exceptions::PyTypeError, prelude::*, types::PyDict};
use serde::Deserialize;

use poker_eval::{
    calc::{equity_det::calc_equity_det, equity_mc::calc_equity_monte_carlo},
    eval::{self, five::get_rank_five, seven::get_rank, target::HandStats},
    stats,
};
use serde_pyobject::{from_pyobject, to_pyobject};

#[pyclass]
#[derive(Debug)]
pub struct PokerEval {
    /// 5-card and 7-card lookup tables used by poker_eval
    t7: Arc<eval::seven::TableSeven>,
    /// 5-card hand statistics
    stats_five: HashMap<String, HandStats>,
    /// 7-card hand statistics
    stats_seven: HashMap<String, HandStats>,
}

#[pyclass]
#[derive(Debug, Clone, Deserialize)]
struct HandsFive {
    /// list of 5-card hands
    hands: Vec<[usize; 5]>,
}

#[pyclass]
#[derive(Debug, Clone, Deserialize)]
struct HandsSeven {
    /// list of 7-card hands
    hands: Vec<[usize; 7]>,
}

#[pyclass]
#[derive(Debug, Clone, Deserialize)]
struct GameDet {
    /// list of players with their 2 cards
    players: Vec<[u32; 2]>,
    /// table cards
    table: Vec<u32>,
}

#[pyclass]
#[derive(Debug, Clone, Deserialize)]
struct GameMc {
    /// list of players with their known cards (0, 1, or 2)
    players: Vec<Vec<u32>>,
    /// table cards
    table: Vec<u32>,
    /// number of games to simulate
    nb_game: u32,
}

#[pymethods]
impl PokerEval {
    #[new]
    fn new() -> Result<Self, PyErr> {
        let start = std::time::Instant::now();

        let t7 = eval::seven::build_tables(false);
        let stats_seven = stats::build_seven(t7.clone(), false);

        let t5_ = Arc::new(t7.t5.clone());
        let stats_five = stats::build_five(t5_, false);

        let end = std::time::Instant::now();
        println!("PokerEval new runtime: {:?}", end - start);

        Ok(PokerEval {
            t7,
            stats_five,
            stats_seven,
        })
    }

    fn stats_five(slf: &PyCell<Self>) -> &PyAny {
        let _slf = slf.borrow();
        let stats = _slf.stats_five.clone();
        to_pyobject(slf.py(), &stats).unwrap()
    }

    fn stats_seven(slf: &PyCell<Self>) -> &PyAny {
        let _slf = slf.borrow();
        let stats = _slf.stats_seven.clone();
        to_pyobject(slf.py(), &stats).unwrap()
    }

    #[pyo3(signature = (payload))]
    fn rank_five(&self, payload: &PyDict) -> Result<Vec<u32>, PyErr> {
        let input: Result<HandsFive, serde_pyobject::Error> = from_pyobject(payload);

        match input {
            Ok(payload) => {
                let t5_ = &self.t7.t5;

                let mut ranks = vec![];
                for hand in payload.hands.iter() {
                    // catch error is not in lib
                    catch_hand_card_no_error(hand)?;

                    let rank = get_rank_five(t5_, *hand);
                    ranks.push(rank);
                }

                Ok(ranks)
            }
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }

    #[pyo3(signature = (payload))]
    fn rank_seven(&self, payload: &PyDict) -> Result<Vec<u32>, PyErr> {
        let input: Result<HandsSeven, serde_pyobject::Error> = from_pyobject(payload);

        match input {
            Ok(payload) => {
                let t7_ = self.t7.clone();

                let mut ranks = vec![];
                for hand in payload.hands.iter() {
                    // catch error is not in lib
                    catch_hand_card_no_error(hand)?;

                    let rank = get_rank(&t7_, *hand);
                    ranks.push(rank);
                }

                Ok(ranks)
            }
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }

    #[pyo3(signature = (payload))]
    fn game_det<'a>(slf: &'a PyCell<Self>, payload: &'a PyDict) -> Result<&'a PyAny, PyErr> {
        let input: Result<GameDet, serde_pyobject::Error> = from_pyobject(payload);

        match input {
            Ok(payload) => {
                let _slf = slf.borrow();
                let equity = calc_equity_det(
                    _slf.t7.clone(),
                    payload.players.clone(),
                    payload.table.clone(),
                    false,
                );

                match equity {
                    Ok(eqty) => {
                        println!("eqty: {:?}", eqty);
                        let py_obj = to_pyobject(slf.py(), &eqty).unwrap();
                        Ok(py_obj)
                    }
                    Err(e) => {
                        let msg = format!("{}", e);
                        Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(msg))
                    }
                }
            }
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }

    #[pyo3(signature = (payload))]
    fn game_mc<'a>(slf: &'a PyCell<Self>, payload: &'a PyDict) -> Result<&'a PyAny, PyErr> {
        let input: Result<GameMc, serde_pyobject::Error> = from_pyobject(payload);

        match input {
            Ok(payload) => {
                let _slf = slf.borrow();
                let equity = calc_equity_monte_carlo(
                    _slf.t7.clone(),
                    payload.players.clone(),
                    payload.table.clone(),
                    payload.nb_game,
                );

                match equity {
                    Ok(eqty) => {
                        let py_obj = to_pyobject(slf.py(), &eqty).unwrap();
                        Ok(py_obj)
                    }
                    Err(e) => {
                        let msg = format!("{}", e);
                        Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(msg))
                    }
                }
            }
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }
}

//
// util
//

fn catch_hand_card_no_error(hand: &[usize]) -> Result<(), PyErr> {
    let card_max = hand.iter().max().unwrap();
    if *card_max > 51 {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
            "Invalid player card: {}",
            card_max
        )));
    }
    Ok(())
}
