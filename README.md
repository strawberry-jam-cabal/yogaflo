# yogaflo

![Build](https://github.com/strawberry-jam-cabal/yogaflo/workflows/Build/badge.svg)

This package generates random yoga flows using a markov model

## Installation

```
pip install yogaflo
```
Requires Python 3.6 or greater.


## Usage

```
yogaflo
```

or

```
python3 -m yogaflo
```


## Contributing Training Flows

Flows are in `src/yogaflo/data/flows/` and are formatted as a list of lists of pose names eg:
```json
[
    ["downward dog", "high plank", "low plank", "upward dog", "downward dog"],
    ["table", "cat", "cow", "cat", "cow", "cat", "cow", "table"]
]
```

A good flow is long enough to be interesting and short enough to remember.

Flows may end with the same pose they start with or another pose that could lead to the starting pose. A full list of poses can be found in `src/yogaflo/data/poses.json`. For the best flow transition probablilities try to use poses already in the pose list as this is what is in the rest of the training data.
