This repo implements the SHA1 hash algorithm symbolically using the z3 SMT solver python API and its propositional logic / bitvector theories.
This allows formulating constraints on the inputs and outputs.

Of course this does not make it possible to break strong hashes because we quickly run into the exponentials!
This is nothing serious, just playing around.
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
Data hex:  080657357bfe25341629b6c5053cb800668f8cf86e
SHA1 hash: 00b3db84051392a65f59c0ff7348a855c1f5d0ba
           ||

Data hex:  f4e4f7d712092b811a9b5b48b802d52583010ceb59
SHA1 hash: 470062e5a5d433700180e68d690b60832c963f26
             ||

Data hex:  324bf95d02404df6c8023c5450068eb65710a8d5b0
SHA1 hash: babb00d5ae06181792254db98cdeecf9c5f5a345
               ||

Data hex:  a3aea29f1b69e0af9f3a9b7deaa1621b00a320cf9c
SHA1 hash: e896cb0013dada849cfa212133c5e131175881cb
                 ||

Data hex:  3919673cda75befe940363e4046fcd6fcb0c458b11
SHA1 hash: c28fa11e00ff9c1a7533e5115de84f30171fd9ab
                   ||

Data hex:  1004a44306e490a5b3213e6353c3d81928dd45eea2
SHA1 hash: bb8c3a504b00d36ec1457416d9a78f1640ef94d8
                     ||

Data hex:  fa4766b0053c59842006f8d35b4e1b4f4015460a2b
SHA1 hash: c28c4285356800589662e30fe01def5467af8a8e
                       ||

Data hex:  c5d5451af82726afee65f4210617ec68b32de0f2c7
SHA1 hash: 6c665726e7676500a574fae7b04904181151f84e
                         ||

Data hex:  5019d79397e4260a2a4698afb584812cb30614d100
SHA1 hash: 32986b2758dc0f2a00aaa148f18fb569d75385da
                           ||

Data hex:  8043eb7009bdbe5326a68f02a2640321221402d1be
SHA1 hash: 0960c355aee6b51d310067f70ae688827c0a934b
                             ||

Data hex:  f1ca5c2f22700e94924ba30ed80ad3fc9682079b6c
SHA1 hash: 2dc063306b3009bb027e0025734de1c5ca3b3fbe
                               ||

Data hex:  190b3fb9dfc8995b69bca647114a881f6c0e1b0df4
SHA1 hash: 52c110189145bbb36643a7000257cf58cbee17cb
                                 ||

Data hex:  fa8445ad687c4e558942a3cb3c41fcf353efc8023b
SHA1 hash: 63ec9f27dd7bd5ae081c956d00b8a1cd723c7d36
                                   ||

Data hex:  e9ede58cf6ee39b74b560ea330448029006c5136db
SHA1 hash: 9f19bb1824bdbf87e1aea5d1fd00758dfebc0da1
                                     ||

Data hex:  a947b449abc397467922b8d78429752b7954c6c5da
SHA1 hash: a38096c0c69b305937a479458ddb00fb47197b9f
                                       ||

Data hex:  a103e7454a0ed01ec70c30df2adced89d0f0811d12
SHA1 hash: f1e90b8326e0926edf5de78aec93aa005c497a65
                                         ||

Data hex:  f144303fda1514a0fcdbff944520306a5b36c39111
SHA1 hash: cfc2077c02f9364c0ab7d51517d1ed350066aeba
                                           ||

Data hex:  004bc5dd17ad24d4500487434e35849949aa216922
SHA1 hash: 8140a56c9aa78026933706ce733873681400ee53
                                             ||

Data hex:  e8c76449f4c6a06185124fb0060069fd3034815a2c
SHA1 hash: 006cb3fe409e8234d3262758fd2e7824ac8c0003
                                               ||

Data hex:  b0096d49302033591001d601070b44d814639c36fe
SHA1 hash: 762ee3db2ae6cde04df1f37c0467c9a73a840500
                                                 ||
```

Some hashes where the i-th and (i+1)-th hash-byte have the same value:

```
Data hex:  cc4edc8b40d9a3d189a1084056c0237b66b2006464
SHA1 hash: e5e5707af701735e0a88d7f2ebcfba4733f29c3f
           ||||

Data hex:  747e4405102a13410180c21c00821601598db0011b
SHA1 hash: d62a2a917902568745c57294c364ecd0bd618178
             ||||

Data hex:  5103885482498d3818303eb8ec1f67d34315522837
SHA1 hash: 30cb9d9dc83afc47f1e09bf4dfd7d603d94542e4
               ||||

Data hex:  0502674db7497f1612d4804141d822cd04290585f5
SHA1 hash: fe6ad8f1f1ba518561aa63b808359d8f19bd3c8e
                 ||||

Data hex:  f9066439f7fff7dbf45130fd7ea21a7e141d0693b0
SHA1 hash: dc438de099994f27ac2fee99ea533b83111cd580
                   ||||

Data hex:  38ff26c40036a9bb0140bcab9104798d4adb8942b1
SHA1 hash: b5c3af306d83838c8d8d01861919bf85d06109d8
                     ||||

Data hex:  c1de0480a5f52ff4997a6180774cf086d001ffb605
SHA1 hash: 58813fcdcc8130305ca629b029ee22e8240a53e1
                       ||||

Data hex:  2108604101ae0233887e830c024e4d3a3112180361
SHA1 hash: 59682ee4d319b54646483f9818768251d83607e2
                         ||||

Data hex:  2d0b4be9094f6a4a40b0a981513705e57a1303a71b
SHA1 hash: c6a04a07c0a90f5c0606c2d5906e39ceafb8ccc0
                           ||||

Data hex:  665fcf5104f78881421b725b490a3f077c6beda546
SHA1 hash: 07bb33cfed74b35804efef98476070ab28044376
                             ||||

Data hex:  ac19c721da38382739090d752976d5f409830a3162
SHA1 hash: a7fda65ee96dc85a1348e9e992520a4a0a0cc72e
                               ||||

Data hex:  3f1367494542117f227060903dff11c5197404a875
SHA1 hash: 00e9422c2d30b4e443cdefc0c009f7792159d282
                                 ||||

Data hex:  1f20f86c186708c203a75fec8d3638df2f247febf8
SHA1 hash: eb019432212a3723ef99af949e9e23143d9ffd37
                                   ||||

Data hex:  a44e67cdf6b97bf55e0aad2d9dc581cb2952ace9bf
SHA1 hash: 7c4b6826430ac7c5d5900369da555542c181b726
                                     ||||

Data hex:  39455dd2b847aafc79048cc23021e51f80f6308531
SHA1 hash: 7266f5a7a05863c2fd9ef8e556be9a9ade5e9ff4
                                       ||||

Data hex:  fa03c72b6236af07bc04e2da379785d5238535d300
SHA1 hash: 661b5d16565332454062f8c3ac7c3fb0b02a9063
                                         ||||

Data hex:  4121d9450856bb9b8ce226c5813df191233b35e235
SHA1 hash: e375f307c7eb4907c0ba00a900f889fd545491ae
                                           ||||

Data hex:  f94a3fc9f8b40fdf2bffffcd75cbe327162878ce1e
SHA1 hash: a8200e4b63ca7c24b405dec8a2796df440838350
                                             ||||

Data hex:  32c4aed0412551bd18467bdd2e4367c6348e44c59f
SHA1 hash: 9c56d799f81415248d9208f2386614dea8053030
                                               ||||
```

Some hashes where the i-th hash-byte and its mirror have the same value:

```
Data hex:  a053c3c5d8d911018006c04116c1a303089fc32182
SHA1 hash: 8255ffa85b6de41655168d8276df786564ab4182
           ||                                    ||

Data hex:  ff0a6f90c0e59a7fd3e30bdff206f4248639a560ab
SHA1 hash: b408ebdec84a70e8709abcebbaf0a4d7147408be
             ||                                ||

Data hex:  f907420901d3db57b83d92844c2e80472a07153100
SHA1 hash: c4f3e98cf4e3b2929d40d1fb3ae7e4ebafe963cc
               ||                            ||

Data hex:  2a064441a13384552040901c084e9429cc3f12822d
SHA1 hash: a6df0099940aa0e3353e5412522659e4997b3ce8
                 ||                        ||

Data hex:  3c36ef812ba116453ca242e0c347c213ea3707d21d
SHA1 hash: 484d0d69da32bc03606c3943312b87da016e3fb6
                   ||                    ||

Data hex:  2a81a759218729b9e8fcde4c208418c93845382f13
SHA1 hash: 576c1a6df42b98d06a78ad5224492be11b681ab8
                     ||                ||

Data hex:  7c8964c9cf50366f8640156c0b43945d4595eac128
SHA1 hash: 7e78a03bf1b40d64ecc00882380df549061343b1
                       ||            ||

Data hex:  38a1bb5d8dc428d5976b90956b26e8f80950f0907c
SHA1 hash: 4d80e99e059b65d3f406ac7cd375bab6a167cbfc
                         ||        ||

Data hex:  f039670f611ab82d5ed4aeef0432c933d6df4a2f10
SHA1 hash: 3e06ec0750e4729be78896e7f40b69d86f818ecb
                           ||    ||

Data hex:  c9463fc23bee2445247f1147228452ef1731810142
SHA1 hash: 7eb5b0f306e18d2ed3eeeec23b206bda36d4c649
                             ||||

Data hex:  9847c5fcb5425ad732ee0405988096711d9a5433fa
SHA1 hash: 971a9d20dc6e48ef5d9f9f0a3ebcf456a3f24bde
                             ||||

Data hex:  7047377e901820332c8be25f5800a1b80020214730
SHA1 hash: 05486387ecfd446297942597772caeac4fe24175
                           ||    ||

Data hex:  745dfe195eac56823d50987dbc8353579840039a49
SHA1 hash: 7c057acec1d0fe7db48447947db81d330c23a216
                         ||        ||

Data hex:  1d0af546fe0038b79b60ff625542aea8848f5c2f94
SHA1 hash: 2fede3900c0c2235a5c0dad647221d4e48c2a547
                       ||            ||

Data hex:  91144015670159968f344be6c7e5532fa35693543a
SHA1 hash: 1a5b623d13eff8319e4f191ab0d7ef7aaa6d656a
                     ||                ||

Data hex:  2039d945908e42913894486535a0007bb1084cab34
SHA1 hash: aee950058b6ef86f34799a50edd5a78b65a77926
                   ||                    ||

Data hex:  e9874549e9537361e03e8f8b4f6e69f29f92b7ce08
SHA1 hash: e628d4516e5f0206db444b92c6b7f8865154d4ea
                 ||                        ||

Data hex:  6d898331e8098b095c02c7e604c4abe2fa90044969
SHA1 hash: 8872bda78d65ddff0099bec64b14a6501ebd8741
               ||                            ||

Data hex:  f855a289077fc6dd8421c71740c403e32404b06181
SHA1 hash: 57724a12a6aa42ac7199d4230975a07af8367237
             ||                                ||

Data hex:  f86e602d04af79bf3cf15310d015e485124ab0e134
SHA1 hash: 71d5764e2cb699e0f56267ab5432a5ab2d894671
           ||                                    ||
```

Some hashes where i-th input and hash byte have the same value:

```
           ||
Data hex:  04c3a4cc86420cb3c8992d06f42df7beb7f043083d
SHA1 hash: 04c63389329274d9fdb4a52cc9d6dbfc1258c214

             ||
Data hex:  a01f616907559b4dc81bbb373fbff60f9a026ad071
SHA1 hash: c71fabf4e9bea3d48f72c9972140daa2e73dbb04

               ||
Data hex:  75fe441a22570fe7e0c1f07c93a9815b0400077105
SHA1 hash: 274044e7b7fe17dcc7b43931bfd5d4f1c40199f1

                 ||
Data hex:  1d184c00ce967bd8bbb004e06099f04a0f0522ffa1
SHA1 hash: 6efcd3003ae713592bca761f54f2a5b3076c9d85

                   ||
Data hex:  59492f44c6a894adf8fd4a050713e91d0a8613f105
SHA1 hash: a4571586c6b9c9f7c6b51ec53d14de00ad0ec34f

                     ||
Data hex:  7d03ebe3021df8693902200f881c3c1ddd3fd859d6
SHA1 hash: a7db8906501d37dab8ede74fa794fec6be5a01b4

                       ||
Data hex:  36df387d713b931f4aef5d68e2e58c78e95ae4eea4
SHA1 hash: 15710b83e0ac93fd238dffc76a48d88a0d9011db

                         ||
Data hex:  f90403c1023a645ab4e2982c7a6910d7233295ca01
SHA1 hash: 17cdcc47a8aca45a5ae99983cf492ccd5faaecec

                           ||
Data hex:  ff073f441550405730e44d79aaba68e7a0b04fa1e0
SHA1 hash: dddd8aef12b95a2c30fa36ec27014feca1994c6b

                             ||
Data hex:  0006444901f2925bba8a97d8f80635c70b7f733328
SHA1 hash: f26ac5a6f536592cc68a7cbb34c082491087c3ae

                               ||
Data hex:  ea6d0368f9d30a011042bf5b621bcfa824a1945353
SHA1 hash: 925407703f402926974abfe8c686ed14c56598dd

                                 ||
Data hex:  2927674bf18b451629a43dbf0cf4601c329560747c
SHA1 hash: 57755a51159af8be4f0bb3bfef5d137cb15265a0

                                   ||
Data hex:  f906444901f3935fb15f7394349c2ac126012c890a
SHA1 hash: f99cb5f62c10c547849a1f6d348c796eb4a2cfdb

                                     ||
Data hex:  244380cd0604bf5220a8132f2ab296ef2b811f1b29
SHA1 hash: ccd0c79f07798e4458e5c0c8d5b2e0269ab4f62d

                                       ||
Data hex:  f3094449c18fa360b6a5309445f1fa2b01e16c0120
SHA1 hash: 885cd019490b49ee3623ab104b0cfa0af8740b72

                                         ||
Data hex:  806b6d5e551a0e59e57c28baf0009276401145bd01
SHA1 hash: 0729ee1d535856f5ede08656f87b8b76b7be4d68

                                           ||
Data hex:  78836041e04e1865782519412d150920031936b328
SHA1 hash: 2b83ce3e01caa669ffe2c66f5f11157903b24037

                                             ||
Data hex:  b9066441006f64640743b3f0585e521da8d2a0a97e
SHA1 hash: 7465a17038aff319d4cbe9569c1afee6add2d66c

                                               ||
Data hex:  f90805c9fe99d6df253001900e08b28fd108211140
SHA1 hash: 6496e977784861d5c76f61c744a32633b47a2132

                                                 ||
Data hex:  d9085c41c1206c439a47882c018c66850ab9833f04
SHA1 hash: 0ea39fa2ad4460fb72637a27c46e1895826af83f
```
