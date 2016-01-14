import noise


def simplex_noise_1d(i, seed=0, octaves=1, freq_ratio=16.0) -> float:
    """
    Create simplex noise between 0 and 1
    :param i: index of the noise
    :param seed: seed to use
    :param octaves: higher number makes the noise smoother
    :param freq_ratio: how often to sample as the ratio changes
    :return: float between 0 and 1
    """
    freq = octaves * freq_ratio
    return (noise.snoise2(seed, i / freq, octaves) + 1) / 2


def simplex_noise_2d(x, y, seed=0, octaves=1, freq_ratio=16.0) -> float:
    """
    Create simplex noise between 0 and 1
    :param seed: seed to use
    :param octaves: higher number makes the noise smoother
    :param freq_ratio: how often to sample as the ratio changes
    :return: float between 0 and 1
    """
    freq = octaves * freq_ratio
    return (noise.snoise3(seed, x / freq, y / freq, octaves) + 1) / 2


def simplex_noise_3d(x, y, z, seed=0, octaves=1, freq_ratio=16.0) -> float:
    """
    Create simplex noise between 0 and 1
    :param x: x coord for the nose
    :param y: y coord for the noise
    :param z: z coord for the noise
    :param seed: seed to use
    :param octaves: higher number makes the noise smoother
    :param freq_ratio: how often to sample as the ratio changes
    :return: float between 0 and 1
    """
    freq = octaves * freq_ratio
    return (noise.snoise4(seed, x / freq, y / freq, z / freq, octaves) + 1) / 2
