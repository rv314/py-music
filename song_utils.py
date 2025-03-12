
import numpy as np
import simpleaudio as sa


def linear(t, initial: float, target: float):
    if (t.shape[0] == 0):
        return t
    assert (initial >= 0 and initial <= 1)
    assert (target >= 0 and target <= 1)
    x = np.linspace(0, 1, num=t.shape[0])
    return (x * (target - initial)) + initial


def ADSR(t, attack, decay, sustain, release):  # release not implemented YET
    if t.shape[0] == 0:
        return t, np.array([])
    assert (attack >= 0 and decay >= 0 and sustain >= 0 and release >= 0)

    adsr = np.zeros_like(t)

    t_base = t - np.min(t)
    attack_idx = np.searchsorted(t_base, attack)
    decay_idx = np.searchsorted(t_base, attack + decay)

    adsr[:attack_idx] = linear(t_base[:attack_idx], 0, 1)
    adsr[attack_idx:decay_idx] = linear(
        t_base[attack_idx:decay_idx], 1, sustain)
    adsr[decay_idx:] = sustain

    release = None

    return adsr, release


def get_freq(note):
    return (440. * (2 ** ((note - 69) / 12.)))


def get_note(t, wave, pitch, velocity):
    return wave(t * get_freq(pitch) * 2 * np.pi) * (velocity / 127.)


def play_notes(notes, ticks_per_quarter, bpm, wave, wait_done=True, play=False):

    sample_rate = 44100
    volume = 0.5

    def to_seconds(tick):
        return ((tick * 60) / (bpm * ticks_per_quarter))

    song_time = to_seconds(notes[-1].end)

    t = np.linspace(0., song_time, (int)(song_time * sample_rate), False)
    song = np.zeros_like(t)

    for idx, note in enumerate(notes):
        print("\rArranging notes... %d / %d" % (idx + 1, len(notes)), end='')
        start_pos = np.searchsorted(t, to_seconds(note.start))
        end_pos = np.searchsorted(t, to_seconds(note.end))

        note_t = t[start_pos:end_pos]
        envelope, release = ADSR(note_t, 0.5, 0.2, 0.7, 0.2)
        song[start_pos:end_pos] += get_note(note_t, wave,
                                            note.pitch, note.velocity) * envelope
    print()

    song = song / np.max(song)
    audio = (song * volume * (2 ** 15 - 1)).astype(np.int16)

    if play:
        print("Playing song...")
        player = sa.play_buffer(audio, 1, 2, sample_rate)
        sa.stop_all()

    if wait_done and play:
        player.wait_done()

    if play:
        return audio, player
    else:
        return audio
