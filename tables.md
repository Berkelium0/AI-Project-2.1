### country

These two conditional probability tables show the allele distribution of the given countries.

| Alleles | north_wumponia |
|:-------:|:--------------:|
|    A    |      0.40      |
|    B    |      0.35      |
|    O    |      0.25      |  

| Alelles | south_wumponia |
|:-------:|:--------------:|
|    A    |      0.25      |
|    B    |      0.45      |
|    O    |      0.30      |

### subject_values

This table shows what can be the child's alleles depending on their parent's alleles.

| subX | subY |  A  |  B  |  O  |
|:----:|:----:|:---:|:---:|:---:|
|  A   |  A   |  1  |  0  |  0  |
|  A   |  B   | 0.5 | 0.5 |  0  |
|  A   |  O   | 0.5 |  0  | 0.5 |
|  B   |  A   | 0.5 | 0.5 |  0  |
|  B   |  B   |  0  |  1  |  0  |
|  B   |  O   |  0  | 0.5 | 0.5 |
|  O   |  A   | 0.5 |  0  | 0.5 |
|  O   |  B   |  0  | 0.5 | 0.5 |
|  O   |  O   |  0  |  0  |  1  |

### blood_type_chart

This table shows the resulting blood type of a person, given their alleles.

| AlleleX | AlleleY | A | B | AB | O |
|---------|:-------:|:-:|:-:|:--:|:-:|
| A       |    A    | 1 | 0 | 0  | 0 |
| A       |    B    | 0 | 0 | 1  | 0 |
| A       |    O    | 1 | 0 | 0  | 0 |
| B       |    A    | 0 | 0 | 1  | 0 |
| B       |    B    | 0 | 1 | 0  | 0 |
| B       |    O    | 0 | 1 | 0  | 0 |
| O       |    A    | 1 | 0 | 0  | 0 |
| O       |    B    | 0 | 1 | 0  | 0 |
| O       |    O    | 0 | 0 | 0  | 1 |

### mixed_blood_test

This CPD gives us the mixed blood test's results, depending on the blood types of person 1 and person 2 that takes the
test.

| Person 1 | Person 2 | A | B | AB | O |
|:--------:|:--------:|:-:|:-:|:--:|:-:|
|    A     |    A     | 1 | 0 | 0  | 0 |
|    A     |    B     | 0 | 0 | 1  | 0 |
|    A     |    AB    | 0 | 0 | 1  | 0 |
|    A     |    O     | 1 | 0 | 0  | 0 |
|    B     |    A     | 0 | 0 | 1  | 0 |
|    B     |    B     | 0 | 1 | 0  | 0 |
|    B     |    AB    | 0 | 0 | 1  | 0 |
|    B     |    O     | 0 | 1 | 0  | 0 |
|    AB    |    A     | 0 | 0 | 1  | 0 |
|    AB    |    B     | 0 | 0 | 1  | 0 |
|    AB    |    AB    | 0 | 0 | 1  | 0 |
|    AB    |    O     | 0 | 0 | 1  | 0 |
|    O     |    A     | 1 | 0 | 0  | 0 |
|    O     |    B     | 0 | 1 | 0  | 0 |
|    O     |    AB    | 0 | 0 | 1  | 0 |
|    O     |    0     | 0 | 0 | 0  | 1 |

### pair_blood_test_check

This table is used for storing the probability of a Pair Blood Test giving the correct result.

| PBT is working | Probability |
|----------------|-------------|
| True           | 0.8         |
| False          | 0.2         |

### pair_blood_test_1

This table takes three variables; results of person 1, results of person 2 and
whether if the PBT test gave the correct results or not. Depending on those, the table shows
which blood type Person 1 can have.

| Result 1 | Result 2 | PBT is | A | B | AB | O |
|----------|----------|--------|---|---|----|---|
| A        | A        | True   | 1 | 0 | 0  | 0 |
| A        | A        | False  | 1 | 0 | 0  | 0 |
| A        | B        | True   | 1 | 0 | 0  | 0 |
| A        | B        | False  | 0 | 1 | 0  | 0 |
| A        | AB       | True   | 1 | 0 | 0  | 0 |
| A        | AB       | False  | 0 | 0 | 1  | 0 |
| A        | O        | True   | 1 | 0 | 0  | 0 |
| A        | O        | False  | 0 | 0 | 0  | 1 |
| B        | A        | True   | 0 | 1 | 0  | 0 |
| B        | A        | False  | 1 | 0 | 0  | 0 |
| B        | B        | True   | 0 | 1 | 0  | 0 |
| B        | B        | False  | 0 | 1 | 0  | 0 |
| B        | AB       | True   | 0 | 1 | 0  | 0 |
| B        | AB       | False  | 0 | 0 | 1  | 0 |
| B        | O        | True   | 0 | 1 | 0  | 0 |
| B        | O        | False  | 0 | 0 | 0  | 1 |
| AB       | A        | True   | 0 | 0 | 0  | 0 |
| AB       | A        | False  | 1 | 0 | 1  | 0 |
| AB       | B        | True   | 0 | 0 | 0  | 0 |
| AB       | B        | False  | 0 | 0 | 1  | 0 |
| AB       | AB       | True   | 0 | 1 | 0  | 0 |
| AB       | AB       | False  | 0 | 0 | 1  | 0 |
| AB       | O        | True   | 0 | 0 | 0  | 1 |
| AB       | O        | False  | 0 | 0 | 0  | 0 |
| O        | A        | True   | 0 | 0 | 0  | 0 |
| O        | A        | False  | 1 | 0 | 0  | 1 |
| O        | B        | True   | 0 | 0 | 0  | 0 |
| O        | B        | False  | 0 | 0 | 0  | 1 |
| O        | AB       | True   | 0 | 0 | 0  | 0 |
| O        | AB       | False  | 0 | 0 | 1  | 1 |
| O        | O        | True   | 0 | 0 | 0  | 0 |
| O        | O        | False  | 0 | 0 | 0  | 1 |

### pair_blood_test_2

This table takes three variables; results of person 1, results of person 2 and
whether if the PBT test gave the correct results or not. Depending on those, the table shows
which blood type Person 2 can have.

| Result 1 | Result 2 | PBT is | A | B | AB | O |
|----------|----------|--------|---|---|----|---|
| A        | A        | True   | 1 | 0 | 0  | 0 |
| A        | A        | False  | 1 | 0 | 0  | 0 |
| A        | B        | True   | 0 | 1 | 0  | 0 |
| A        | B        | False  | 1 | 0 | 0  | 0 |
| A        | AB       | True   | 0 | 0 | 1  | 0 |
| A        | AB       | False  | 1 | 0 | 0  | 0 |
| A        | O        | True   | 0 | 0 | 0  | 1 |
| A        | O        | False  | 1 | 0 | 0  | 0 |
| B        | A        | True   | 1 | 0 | 0  | 0 |
| B        | A        | False  | 0 | 1 | 0  | 0 |
| B        | B        | True   | 0 | 1 | 0  | 0 |
| B        | B        | False  | 0 | 1 | 0  | 0 |
| B        | AB       | True   | 0 | 0 | 1  | 0 |
| B        | AB       | False  | 0 | 1 | 0  | 0 |
| B        | O        | True   | 0 | 0 | 0  | 1 |
| B        | O        | False  | 1 | 1 | 0  | 0 |
| AB       | A        | True   | 0 | 0 | 0  | 0 |
| AB       | A        | False  | 0 | 0 | 1  | 0 |
| AB       | B        | True   | 0 | 0 | 0  | 0 |
| AB       | B        | False  | 0 | 1 | 1  | 0 |
| AB       | AB       | True   | 0 | 0 | 0  | 0 |
| AB       | AB       | False  | 0 | 0 | 1  | 0 |
| AB       | O        | True   | 0 | 0 | 1  | 1 |
| AB       | O        | False  | 1 | 0 | 0  | 0 |
| O        | A        | True   | 0 | 0 | 0  | 1 |
| O        | A        | False  | 0 | 1 | 0  | 0 |
| O        | B        | True   | 0 | 0 | 0  | 1 |
| O        | B        | False  | 0 | 0 | 1  | 0 |
| O        | AB       | True   | 0 | 0 | 0  | 1 |
| O        | AB       | False  | 0 | 0 | 1  | 1 |
| O        | O        | True   | 0 | 0 | 0  | 1 |
| O        | O        | False  | 0 | 0 | 0  | 1 |
