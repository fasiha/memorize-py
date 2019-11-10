# memorize-py

This repo contains a pure-Python library that implements the Memorize algorithm described [online](http://learning.mpi-sws.org/memorize/) and in the peer-reviewed 2019 paper in [PNAS](https://doi.org/10.1073/pnas.1815156116) by Behzad Tabibian, Utkarsh Upadhyay, Abir De, Ali Zarezade, Bernhard Schölkopf, and Manuel Gomez-Rodriguez.

This library provides a single function that takes as inputs
- the memory model: a function that maps time to recall probability for a single fact,
- a number that trades off between the rate of reviews and probability of forgetting, and
- a time horizon (optionally infinite)

and outputs a due date for reviewing that fact.

Note that this is an *unaffiliated* implementation of the algorithm 😊! This is a proper library that you can `pip install` and `import` into your quiz application. It has no external dependencies. It is also agnostic to the memory model, i.e., this implementation will apply the Memorize algorithm to any function that maps time to recall probability. 

## Installation
Install with:
```
pip install memorizesrs
```
Then import into your library as
```py
import memorizesrs
```

## API: `memorizesrs.schedule(timeToRecallProb: Callable[[float], float], q: float, T: float, rng=None) -> float`
Given
- `timeToRecallProb`, a function that maps elapsed time (in "units from now" 0 is "now") to recall probability (between 0 and 1),
- `q`, a number that the algorithm uses to trade off reviewing intensity versus risk of forgetting: this should be a number greater than zero. For facts with very low probability of recall, the ***average*** due date returned by the function will be `sqrt(q)`, so making `q` small will allow the algorithm to on average schedule sooner reviews for low-recall-probability flashcards. Experiment with values between `q=0.1` to `q=1.0` to `q=10.0`.
- `T`, the maximum time horizon the algorithm should consider. This can be `math.inf` if you want the algorithm to search for a due date far, far into the future, although the algorithm might run for a long time. If `T` is finite, the algorithm may return `math.inf` to indicate that this flashcard should *not* be scheduled in this `T`-window.
- `rng` should be a class of `random.Random` if not `None`. Use this for setting the random generator (for reproducible results).

The output is a *number*, in the same units as `T` and the input to `timeToRecallProb`, which corresponds to "units from now to schedule the quiz".

**N.B.** Because Memorize is a *stochastic* algorithm, this function will return *different* numbers when you call it with the *same* input. In a nutshell, the algorithm converts the probability of recall and the `q` parameter above into a [Poisson point process](https://en.wikipedia.org/wiki/Poisson_point_process), which it then samples from. Over scheduling infinitely-many cards for infinitely-many reviews, the algorithm is guaranteed to be optimal (under the quadratic loss function), but the specific numbers *you* personally get for your quizzes are going to vary randomly.

**Note also** that this library does not help you with the recall probability function. You are welcome to use Duolingo's [half-life regression](https://github.com/duolingo/halflife-regression) or [Ebisu](https://fasiha.github.io/ebisu), or any other quantitative memory model. This library similarly does not help you update the memory model with the results of the quizzes. This library is very narrowly-scoped: to convert your memory models into quiz due dates using the Memorize algorithm.

## Dev
Format code with `yapf`.

Run tests with
```
$ python setup.py test
```

To publish to PyPI, update `setup.py` with a new version number, then:
```
$ rm dist/* && python setup.py sdist bdist_wheel && twine upload dist/* --skip-existing
```

## Contact
Please contact me, Ahmed Fasih, by either opening an [issue](https://github.com/fasiha/memorize-py/issues) if you have a GitHub account or by [contacting me directly](https://fasiha.github.io/#contact). I will be most delighted to receive your feedback, suggestions, bug reports, and pull requests, and will do my best to answer questions.

Consider contacting the inventors of the algorithm via [the Memorize website](http://learning.mpi-sws.org/memorize/) or the [Memorize GitHub repo](https://github.com/Networks-Learning/Memorize), and read their [open-access paper on PNAS](https://doi.org/10.1073/pnas.1815156116).
