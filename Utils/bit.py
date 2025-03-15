# Bitwise operations


def get_bit(x: int, n: int):
    return (x >> n) & 1


def unset_bit(x: int, n: int):
    return x & ~(1 << n)


def get_freq(note: int):
    return 440. * (2 ** ((note - 69.) / 12.))


midi_skips = {
    0xA: 2,
    0xB: 2,
    0xC: 1,
    0xD: 1,
    0xE: 2
}

meta_not_skips = [
    0x2F,
    0x51,
    0x58,
]
