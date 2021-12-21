from typing import List, Tuple

import numpy as np
import numpy.typing as npt

BitArray = npt.NDArray[np.bool_]


def parse(lines: List[str]) -> Tuple[BitArray, BitArray]:
    lut: BitArray = np.array([x == "#" for x in lines[0]], dtype=np.bool_)
    image: BitArray = np.array(
        [[x == "#" for x in line] for line in lines[2:]], dtype=np.bool_
    )
    return lut, image


def enhance_vec(lut: BitArray, orig_image: BitArray, iters: int) -> BitArray:
    for i in range(iters):
        bg = lut[0] and i % 2 == 1
        image: BitArray = np.full(
            (orig_image.shape[0] + 4, orig_image.shape[1] + 4), bg, dtype=np.bool_
        )
        image[2:-2, 2:-2] = orig_image

        # fmt: off
        indices = (
            256 * image[0:-2, 0:-2] +
            128 * image[0:-2, 1:-1] +
             64 * image[0:-2, 2:  ] +
             32 * image[1:-1, 0:-2] +
             16 * image[1:-1, 1:-1] +
              8 * image[1:-1, 2:  ] +
              4 * image[2:,   0:-2] +
              2 * image[2:,   1:-1] +
              1 * image[2:,   2:  ]
        )
        # fmt: on
        orig_image = lut[indices]
    return orig_image


def display(image: BitArray) -> None:
    print(
        "\n".join(
            l.lstrip(" ").lstrip("[").rstrip("]")
            for l in np.array2string(
                image,
                separator="",
                formatter={"bool": lambda x: "#" if x else "."},
                threshold=image.size,
                max_line_width=image.shape[1] + 4,
            ).splitlines(keepends=False)
        )
        + "\n"
    )


def part_1(lines: List[str]) -> int:
    lut, image = parse(lines)
    image = enhance_vec(lut, image, 2)
    return np.count_nonzero(image)


def part_2(lines: List[str]) -> int:
    lut, image = parse(lines)
    image = enhance_vec(lut, image, 50)
    return np.count_nonzero(image)
