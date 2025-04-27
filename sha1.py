#!/usr/bin/python3


from typing import TypeVar


def main() -> None:
    assert "0a4d55a8d778e5022fab701977c5d840bbc486d0" == sha1hash(b"Hello World")
    assert "4b94287d001bc19d133233a57b64443504e3f08f" == sha1hash(b"1" * 10000)


def sha1hash(val: bytes) -> str:
    m = SHA1()
    m.SHA1Input(frombytes(val))
    digest = m.SHA1Result()
    return bytes.hex(tobytes(digest))


# Proper parametric polymorphism (with type classes and checked at compile time
# and actually enforced like in Haskell) is kind of nicer than this bolted on
# mypy type system around dynamic subtyping...
T = TypeVar("T", bound="FixedWidthUInt")


class FixedWidthUInt:
    def __init__(self: T, val: int, width: int):
        self.width = width
        self.maxval = 2**width - 1
        self.val = self.maxval & val

    def __str__(self: T) -> str:
        return str(self.val)

    def __add__(self: T, other: T) -> T:
        assert self.width == other.width, f"{self.width} != {other.width}"
        return self.__class__(self.val + other.val)

    def __and__(self: T, other: T) -> T:
        assert self.width == other.width, f"{self.width} != {other.width}"
        return self.__class__(self.val & other.val)

    def __or__(self: T, other: T) -> T:
        assert self.width == other.width, f"{self.width} != {other.width}"
        return self.__class__(self.val | other.val)

    def __invert__(self: T) -> T:
        return self.__class__(~self.val)

    def __xor__(self: T, other: T) -> T:
        assert self.width == other.width, f"{self.width} != {other.width}"
        return self.__class__(self.val ^ other.val)

    def __lshift__(self: T, other: T) -> T:
        assert self.width == other.width, f"{self.width} != {other.width}"
        return self.__class__(self.val << other.val)

    def __rshift__(self: T, other: T) -> T:
        assert self.width == other.width, f"{self.width} != {other.width}"
        return self.__class__(self.val >> other.val)

    def rotate_left(self: T, other: T) -> T:
        assert self.width == other.width, f"{self.width} != {other.width}"
        return (self << other) | (self >> self.__class__(self.width - other.val))


# seems not easily possible
# def from_u8(val: "U8", width: int) -> T:


class U8(FixedWidthUInt):
    def __init__(self, val: int):
        super().__init__(val, 8)


class U32(FixedWidthUInt):
    def __init__(self, val: int):
        super().__init__(val, 32)


class U64(FixedWidthUInt):
    def __init__(self, val: int):
        super().__init__(val, 64)


def frombytes(data: bytes) -> list[U8]:
    return [U8(b) for b in data]


def tobytes(data: list[U8]) -> bytes:
    return bytes([b.val for b in data])


SHA1_Message_Block_Size = 64
SHA1HashSize = 20
SHA1HashSizeBits = 160


def SHA_Ch(x: U32, y: U32, z: U32) -> U32:
    return (x & y) ^ ((~x) & z)


def SHA_Maj(x: U32, y: U32, z: U32) -> U32:
    return (x & y) ^ (x & z) ^ (y & z)


def SHA_Parity(x: U32, y: U32, z: U32) -> U32:
    return x ^ y ^ z


class SHA1:

    def __init__(self) -> None:
        self.Intermediate_Hash: list[U32] = [
            U32(0x67452301),
            U32(0xEFCDAB89),
            U32(0x98BADCFE),
            U32(0x10325476),
            U32(0xC3D2E1F0),
        ]
        self.Length: int = 0
        self.Message_Block_Index: int = 0
        self.Message_Block: list[U8] = [U8(0) for _ in range(SHA1_Message_Block_Size)]
        self.Computed: bool = False

    def SHA1ProcessMessageBlock(self) -> None:
        K: list[U32] = [
            U32(0x5A827999),
            U32(0x6ED9EBA1),
            U32(0x8F1BBCDC),
            U32(0xCA62C1D6),
        ]

        W: list[U32] = [U32(0) for _ in range(80)]

        for t in range(16):
            W[t] |= U32(self.Message_Block[t * 4 + 0].val) << U32(3 * 8)
            W[t] |= U32(self.Message_Block[t * 4 + 1].val) << U32(2 * 8)
            W[t] |= U32(self.Message_Block[t * 4 + 2].val) << U32(1 * 8)
            W[t] |= U32(self.Message_Block[t * 4 + 3].val) << U32(0 * 8)

        for t in range(16, 80):
            W[t] = (W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16]).rotate_left(U32(1))

        A, B, C, D, E = self.Intermediate_Hash

        for t in range(20):
            temp = A.rotate_left(U32(5)) + SHA_Ch(B, C, D) + E + W[t] + K[0]
            E = D
            D = C
            C = B.rotate_left(U32(30))
            B = A
            A = temp

        for t in range(20, 40):
            temp = A.rotate_left(U32(5)) + SHA_Parity(B, C, D) + E + W[t] + K[1]
            E = D
            D = C
            C = B.rotate_left(U32(30))
            B = A
            A = temp

        for t in range(40, 60):
            temp = A.rotate_left(U32(5)) + SHA_Maj(B, C, D) + E + W[t] + K[2]
            E = D
            D = C
            C = B.rotate_left(U32(30))
            B = A
            A = temp

        for t in range(60, 80):
            temp = A.rotate_left(U32(5)) + SHA_Parity(B, C, D) + E + W[t] + K[3]
            E = D
            D = C
            C = B.rotate_left(U32(30))
            B = A
            A = temp

        self.Intermediate_Hash[0] += A
        self.Intermediate_Hash[1] += B
        self.Intermediate_Hash[2] += C
        self.Intermediate_Hash[3] += D
        self.Intermediate_Hash[4] += E
        self.Message_Block_Index = 0

    def SHA1Input(self, message_array: list[U8]) -> None:
        assert len(message_array) != 0
        assert not self.Computed

        for i in range(len(message_array)):
            self.Message_Block[self.Message_Block_Index] = message_array[i]
            self.Message_Block_Index += 1

            self.Length += 8
            if self.Message_Block_Index == SHA1_Message_Block_Size:
                self.SHA1ProcessMessageBlock()

    def SHA1PadMessage(self, Pad_Byte: U8) -> None:
        if self.Message_Block_Index >= (SHA1_Message_Block_Size - 8):
            self.Message_Block[self.Message_Block_Index] = Pad_Byte
            self.Message_Block_Index += 1

            while self.Message_Block_Index < SHA1_Message_Block_Size:
                self.Message_Block[self.Message_Block_Index] = U8(0)
                self.Message_Block_Index += 1

            self.SHA1ProcessMessageBlock()

        else:
            self.Message_Block[self.Message_Block_Index] = Pad_Byte
            self.Message_Block_Index += 1

        while self.Message_Block_Index < (SHA1_Message_Block_Size - 8):
            self.Message_Block[self.Message_Block_Index] = U8(0)
            self.Message_Block_Index += 1

        self.Message_Block[56] = U8(self.Length >> (8 * 7))
        self.Message_Block[57] = U8(self.Length >> (8 * 6))
        self.Message_Block[58] = U8(self.Length >> (8 * 5))
        self.Message_Block[59] = U8(self.Length >> (8 * 4))
        self.Message_Block[60] = U8(self.Length >> (8 * 3))
        self.Message_Block[61] = U8(self.Length >> (8 * 2))
        self.Message_Block[62] = U8(self.Length >> (8 * 1))
        self.Message_Block[63] = U8(self.Length >> (8 * 0))

        self.SHA1ProcessMessageBlock()

    def SHA1Finalize(self, Pad_Byte: U8) -> None:
        self.SHA1PadMessage(Pad_Byte)
        self.Length = 0
        self.Computed = True

    def SHA1Result(self) -> list[U8]:
        if not self.Computed:
            self.SHA1Finalize(U8(0x80))

        digest = [U8(0) for _ in range(SHA1HashSize)]

        for i in range(SHA1HashSize):
            digest[i] = U8(
                (self.Intermediate_Hash[i >> 2] >> U32(8 * (3 - (i & 0x03)))).val
            )

        return digest


if __name__ == "__main__":
    main()

# TODO refactor pylint *py
# TODO refactor mypy --strict *py
# TODO refactor variable names
# TODO refactor method names remove prefix

# clear ; mypy --strict *py  ; pylint --disable=R0903,C0114,C0115,C0116,C0200 *py
