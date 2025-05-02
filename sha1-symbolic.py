#!/usr/bin/python3

import z3  # type: ignore


def main() -> None:
    z3.set_param(verbose=2)

    # Sanity check that the symbolic implementation is correct by passing
    # fully determined input.
    # assert "0a4d55a8d778e5022fab701977c5d840bbc486d0" == sha1hash_(b"Hello World")
    # assert "4b94287d001bc19d133233a57b64443504e3f08f" == sha1hash_(b"1" * 10000)

    # Find message whose checksum starts with one null byte.
    # s.add(hash[0] == make_u8(0))

    # for i in range(SHA1HashSize):
    for i in range(SHA1HashSize - 1):

        data = [z3.BitVec("data" + str(i), 8) for i in range(SHA1HashSize + 1)]
        print(
            f"[+] Constructing U8 array of {len(data)} symbolic bytes "
            + "and the symbolic hash computation for it"
        )
        hash = sha1hash(data)

        print("[+] Adding additional constraints to the solver")
        s = z3.Solver()

        # Find message whose i-th hash-byte is null.
        # s.add(hash[i] == make_u8(0))

        # Find message whose i-th and (i+1)-th hash-byte is null.
        # s.add(hash[i + 0] == make_u8(0))
        # s.add(hash[i + 1] == make_u8(0))

        # Find message whose i-th and (i+1)-th hash-byte have the same value.
        s.add(hash[i + 0] == hash[i + 1])

        print("[+] Checking for boolean satisfiability")
        if s.check() == z3.sat:
            print("[+] Found valid model")

            m = s.model()
            dataval = [m.evaluate(d) for d in data]
            hashval = [m.evaluate(h) for h in hash]

            print(f"    Data hex:  {hex_from_bv(dataval)}")
            print(f"    SHA1 hash: {hex_from_bv(hashval)}")


type U8 = z3.BitVecRef
type U32 = z3.BitVecRef


def make_u8(n: int) -> U8:
    return z3.BitVecVal(n, 8)


def make_u32(n: int) -> U32:
    return z3.BitVecVal(n, 32)


def sha1hash(val: list[U8]) -> list[U8]:
    m = SHA1()
    m.SHA1Input(val)
    digest = m.SHA1Result()
    return [z3.simplify(b) for b in digest]


# Use symbolic version with fixed fully determined input for checking that the
# implementation is correct.
def sha1hash_(val: bytes) -> str:
    m = SHA1()
    m.SHA1Input(bv_from_bytes(val))
    digest = m.SHA1Result()
    return hex_from_bv(digest)


def bv_from_bytes(data: bytes) -> list[U8]:
    return [make_u8(b) for b in data]


def bytes_from_bv(data: list[U8]) -> bytes:
    return bytes([z3.simplify(b).as_long() for b in data])


def hex_from_bv(input: list[U8]) -> str:
    bs = bytes_from_bv(input)
    return bytes.hex(bs)


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
        self.state: list[U32] = [
            make_u32(0x67452301),
            make_u32(0xEFCDAB89),
            make_u32(0x98BADCFE),
            make_u32(0x10325476),
            make_u32(0xC3D2E1F0),
        ]
        self.length: int = 0
        self.msg_block_idx: int = 0
        self.msg_block: list[U8] = [make_u8(0) for _ in range(SHA1_Message_Block_Size)]
        self.computed: bool = False

    def SHA1ProcessMessageBlock(self) -> None:
        K: list[U32] = [
            make_u32(0x5A827999),
            make_u32(0x6ED9EBA1),
            make_u32(0x8F1BBCDC),
            make_u32(0xCA62C1D6),
        ]

        W: list[U32] = [make_u32(0) for _ in range(80)]

        for t in range(16):
            W[t] |= z3.ZeroExt(24, self.msg_block[t * 4 + 0]) << (3 * 8)
            W[t] |= z3.ZeroExt(24, self.msg_block[t * 4 + 1]) << (2 * 8)
            W[t] |= z3.ZeroExt(24, self.msg_block[t * 4 + 2]) << (1 * 8)
            W[t] |= z3.ZeroExt(24, self.msg_block[t * 4 + 3]) << (0 * 8)

        for t in range(16, 80):
            W[t] = z3.RotateLeft(W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16], 1)

        A, B, C, D, E = self.state

        for t in range(20):
            temp = z3.RotateLeft(A, 5) + SHA_Ch(B, C, D) + E + W[t] + K[0]
            E = D
            D = C
            C = z3.RotateLeft(B, 30)
            B = A
            A = temp

        for t in range(20, 40):
            temp = z3.RotateLeft(A, 5) + SHA_Parity(B, C, D) + E + W[t] + K[1]
            E = D
            D = C
            C = z3.RotateLeft(B, 30)
            B = A
            A = temp

        for t in range(40, 60):
            temp = z3.RotateLeft(A, 5) + SHA_Maj(B, C, D) + E + W[t] + K[2]
            E = D
            D = C
            C = z3.RotateLeft(B, 30)
            B = A
            A = temp

        for t in range(60, 80):
            temp = z3.RotateLeft(A, 5) + SHA_Parity(B, C, D) + E + W[t] + K[3]
            E = D
            D = C
            C = z3.RotateLeft(B, 30)
            B = A
            A = temp

        self.state[0] += A
        self.state[1] += B
        self.state[2] += C
        self.state[3] += D
        self.state[4] += E
        self.msg_block_idx = 0

    def SHA1Input(self, message_array: list[U8]) -> None:
        assert len(message_array) != 0
        assert not self.computed

        for i in range(len(message_array)):
            self.msg_block[self.msg_block_idx] = message_array[i]
            self.msg_block_idx += 1

            self.length += 8
            if self.msg_block_idx == SHA1_Message_Block_Size:
                self.SHA1ProcessMessageBlock()

    def SHA1PadMessage(self, Pad_Byte: U8) -> None:
        if self.msg_block_idx >= (SHA1_Message_Block_Size - 8):
            self.msg_block[self.msg_block_idx] = Pad_Byte
            self.msg_block_idx += 1

            while self.msg_block_idx < SHA1_Message_Block_Size:
                self.msg_block[self.msg_block_idx] = make_u8(0)
                self.msg_block_idx += 1

            self.SHA1ProcessMessageBlock()

        else:
            self.msg_block[self.msg_block_idx] = Pad_Byte
            self.msg_block_idx += 1

        while self.msg_block_idx < (SHA1_Message_Block_Size - 8):
            self.msg_block[self.msg_block_idx] = make_u8(0)
            self.msg_block_idx += 1

        self.msg_block[56] = make_u8(self.length >> (8 * 7))
        self.msg_block[57] = make_u8(self.length >> (8 * 6))
        self.msg_block[58] = make_u8(self.length >> (8 * 5))
        self.msg_block[59] = make_u8(self.length >> (8 * 4))
        self.msg_block[60] = make_u8(self.length >> (8 * 3))
        self.msg_block[61] = make_u8(self.length >> (8 * 2))
        self.msg_block[62] = make_u8(self.length >> (8 * 1))
        self.msg_block[63] = make_u8(self.length >> (8 * 0))

        self.SHA1ProcessMessageBlock()

    def SHA1Finalize(self, Pad_Byte: U8) -> None:
        self.SHA1PadMessage(Pad_Byte)
        self.length = 0
        self.computed = True

    def SHA1Result(self) -> list[U8]:
        if not self.computed:
            self.SHA1Finalize(make_u8(0x80))

        digest = [z3.BitVecVal(0, 8) for _ in range(SHA1HashSize)]

        for i in range(SHA1HashSize):
            digest[i] = z3.Extract(
                8 - 1, 0, self.state[i >> 2] >> (8 * (3 - (i & 0x03)))
            )

        return digest


if __name__ == "__main__":
    main()


# clear ; mypy --strict *py  ; pylint --disable=R0903,C0114,C0115,C0116,C0200,C0103 *py
