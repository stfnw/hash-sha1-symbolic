This repo implements the SHA1 hash algorithm symbolically using the z3 SMT solver python API and its propositional logic / bitvector theories.
This allows formulating constraints on the inputs and outputs.

Of course this does not make it possible to break strong hashes because we quickly run into the exponentials!
But it nonetheless allows us to interactively explore the topic and find interesting pairs of inputs/outputs, like e.g. specific values at positions, fixed prefixes, or fixed suffixes.

# Examples

Here are some example input/output pairs I got while experimenting with this topic.
Note: All data input and hash output is hex encoded for easier printability.
The examples can be easily checked against the typical implementations available on Linux e.g. as follows:

```
printf 59db262ae923f6bed376763799172b93ca | xxd -r -p | md5sum
d7f3e5299129e1adfbc1e8a2edbcea00  -
```

```
Data hex:  080657357bfe25341629b6c5053cb800668f8cf86e
SHA1 hash: 00b3db84051392a65f59c0ff7348a855c1f5d0ba
           ||
```
