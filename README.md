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

Hash with first byte null:

```
Data hex:  080657357bfe25341629b6c5053cb800668f8cf86e
SHA1 hash: 00b3db84051392a65f59c0ff7348a855c1f5d0ba
           ||
```

Some hashes where the i-th hash-byte is null:

```
080657357bfe25341629b6c5053cb800668f8cf86e
00b3db84051392a65f59c0ff7348a855c1f5d0ba
||

f4e4f7d712092b811a9b5b48b802d52583010ceb59
470062e5a5d433700180e68d690b60832c963f26
  ||

324bf95d02404df6c8023c5450068eb65710a8d5b0
babb00d5ae06181792254db98cdeecf9c5f5a345
    ||

a3aea29f1b69e0af9f3a9b7deaa1621b00a320cf9c
e896cb0013dada849cfa212133c5e131175881cb
      ||

3919673cda75befe940363e4046fcd6fcb0c458b11
c28fa11e00ff9c1a7533e5115de84f30171fd9ab
        ||

1004a44306e490a5b3213e6353c3d81928dd45eea2
bb8c3a504b00d36ec1457416d9a78f1640ef94d8
          ||

fa4766b0053c59842006f8d35b4e1b4f4015460a2b
c28c4285356800589662e30fe01def5467af8a8e
            ||

c5d5451af82726afee65f4210617ec68b32de0f2c7
6c665726e7676500a574fae7b04904181151f84e
              ||

5019d79397e4260a2a4698afb584812cb30614d100
32986b2758dc0f2a00aaa148f18fb569d75385da
                ||

8043eb7009bdbe5326a68f02a2640321221402d1be
0960c355aee6b51d310067f70ae688827c0a934b
                  ||

f1ca5c2f22700e94924ba30ed80ad3fc9682079b6c
2dc063306b3009bb027e0025734de1c5ca3b3fbe
                    ||

190b3fb9dfc8995b69bca647114a881f6c0e1b0df4
52c110189145bbb36643a7000257cf58cbee17cb
                      ||

fa8445ad687c4e558942a3cb3c41fcf353efc8023b
63ec9f27dd7bd5ae081c956d00b8a1cd723c7d36
                        ||

e9ede58cf6ee39b74b560ea330448029006c5136db
9f19bb1824bdbf87e1aea5d1fd00758dfebc0da1
                          ||

a947b449abc397467922b8d78429752b7954c6c5da
a38096c0c69b305937a479458ddb00fb47197b9f
                            ||

a103e7454a0ed01ec70c30df2adced89d0f0811d12
f1e90b8326e0926edf5de78aec93aa005c497a65
                              ||

f144303fda1514a0fcdbff944520306a5b36c39111
cfc2077c02f9364c0ab7d51517d1ed350066aeba
                                ||

004bc5dd17ad24d4500487434e35849949aa216922
8140a56c9aa78026933706ce733873681400ee53
                                  ||

e8c76449f4c6a06185124fb0060069fd3034815a2c
006cb3fe409e8234d3262758fd2e7824ac8c0003
                                    ||

b0096d49302033591001d601070b44d814639c36fe
762ee3db2ae6cde04df1f37c0467c9a73a840500
                                      ||
```
