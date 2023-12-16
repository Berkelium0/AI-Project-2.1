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
      