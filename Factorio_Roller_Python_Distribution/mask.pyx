cimport numpy as np
import numpy as np
np.import_array()


ctypedef np.uint8_t uint8_t


def mask(np.ndarray[uint8_t, ndim=3] source, np.ndarray[uint8_t, ndim=2] rgb,
         np.ndarray[uint8_t, ndim=2] outside_radius_mask, np.ndarray[uint8_t, ndim=2] starter_mask, int scale):
    cdef np.ndarray[uint8_t, ndim=2, cast=True] base_mask = source[:, :, 0] == 150
    cdef np.ndarray[uint8_t, ndim=2, cast=True] power_mask = source[:, :, 0] == 165
    cdef np.ndarray[uint8_t, ndim=2, cast=True] invalid = outside_radius_mask + base_mask + power_mask
    cdef np.ndarray[uint8_t, ndim=2, cast=True] not_invalid = np.invert(invalid)
    starter_mask = np.logical_and(starter_mask, not_invalid)

    cdef np.ndarray[uint8_t, ndim=2, cast=True] water_mask = source[:, :, 0] == 45
    cdef np.ndarray[uint8_t, ndim=2, cast=True] iron_mask = source[:, :, 1] == 229
    cdef np.ndarray[uint8_t, ndim=2, cast=True] copper_mask = source[:, :, 1] == 127
    cdef np.ndarray[uint8_t, ndim=2, cast=True] coal_mask = source[:, :, 0] == 30
    cdef np.ndarray[uint8_t, ndim=2, cast=True] stone_mask = source[:, :, 1] == 255
    cdef np.ndarray[uint8_t, ndim=2, cast=True] crude_oil_mask = np.logical_and(source[:, :, 0] > 175, source[:, :, 2] > 175)

    cdef np.ndarray[uint8_t, ndim=3] a = np.zeros((1024, 1024, 3), dtype=np.uint8)
    iron_mask = np.logical_and(iron_mask, not_invalid)
    stone_mask = np.logical_and(stone_mask, not_invalid)
    copper_mask = np.logical_and(copper_mask, not_invalid)
    coal_mask = np.logical_and(coal_mask, not_invalid)
    crude_oil_mask = np.logical_and(crude_oil_mask, not_invalid)

    # uncomment to generate array for visual mask output for debugging
    #a[iron_mask] = rgb[1]
    #a[stone_mask] = rgb[4]
    #a[copper_mask] = rgb[2]
    #a[coal_mask] = rgb[3]
    #a[crude_oil_mask] = rgb[7]
    #a[iron_mask & starter_mask] = rgb[8]
    #a[stone_mask & starter_mask] = rgb[11]
    #a[copper_mask & starter_mask] = rgb[9]
    #a[coal_mask & starter_mask] = rgb[10]
    #a[outside_radius_mask] = rgb[12]
    #a[base_mask] = rgb[13]
    #a[power_mask] = rgb[14]
    #a[water_mask] = rgb[0]

    cdef int starter_iron_tiles = np.count_nonzero(iron_mask & starter_mask) * scale
    cdef int iron_tiles = np.count_nonzero(iron_mask) * scale - starter_iron_tiles
    cdef int starter_copper_tiles = np.count_nonzero(copper_mask & starter_mask) * scale
    cdef int copper_tiles = np.count_nonzero(copper_mask) * scale - starter_copper_tiles
    cdef int starter_coal_tiles = np.count_nonzero(coal_mask & starter_mask) * scale
    cdef int coal_tiles = np.count_nonzero(coal_mask) * scale - starter_coal_tiles
    cdef int starter_stone_tiles = np.count_nonzero(stone_mask & starter_mask) * scale
    cdef int stone_tiles = np.count_nonzero(stone_mask) * scale - starter_stone_tiles
    cdef int crude_oil_tiles = np.count_nonzero(crude_oil_mask)

    return a, iron_tiles, stone_tiles, copper_tiles, coal_tiles, starter_iron_tiles, starter_stone_tiles, starter_copper_tiles, starter_coal_tiles, crude_oil_tiles