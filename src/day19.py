import itertools
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Literal,
    NamedTuple,
    NewType,
    Optional,
    Tuple,
)


def sign(x: int) -> Literal[-1, 0, 1]:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


class Orientation(NamedTuple):
    facing_axis: int
    facing_direction: int
    up_axis: int
    up_direction: int


class Offset(NamedTuple):
    dx: int
    dy: int
    dz: int

    def normalize(self) -> "Offset":
        vals = sorted(abs(i) for i in [self.dx, self.dy, self.dz])
        return Offset(*vals)

    def orient_to(self, reference: "Offset") -> Orientation:
        "Get the orientation of this offset, if `reference` is facing +x with +y up."
        ref_abs = [abs(i) for i in reference]

        # pylint: disable=unsubscriptable-object
        facing_axis = ref_abs.index(abs(self[0]))
        facing_direction = sign(reference[0]) * sign(self[facing_axis])
        up_axis = ref_abs.index(abs(self[1]))
        up_direction = sign(reference[1]) * sign(self[up_axis])

        return Orientation(facing_axis, facing_direction, up_axis, up_direction)

    def __format__(self, format_spec: str) -> str:
        if format_spec:
            return f"({self.dx:{format_spec}}, {self.dy:{format_spec}}, {self.dz:{format_spec}})"
        return str(self)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{self:d}"


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def __sub__(self, other: Any) -> Offset:
        if isinstance(other, Coord):
            return Offset(self.x - other.x, self.y - other.y, self.z - other.z)
        # if isinstance(other, Offset):
        #     return Coord(self.x - other.dx, self.y - other.dy, self.z - other.dz)
        return NotImplemented

    def __add__(self, other: Offset) -> "Coord":  # type: ignore
        if not isinstance(other, Offset):
            return NotImplemented
        return Coord(self.x + other.dx, self.y + other.dy, self.z + other.dz)

    def __format__(self, format_spec: str) -> str:
        if format_spec:
            return f"({self.x:{format_spec}}, {self.y:{format_spec}}, {self.z:{format_spec}})"
        return str(self)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{self:d}"


@dataclass
class Scanner:
    position: Optional[Coord] = None
    beacons: List[Coord] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.beacons)

    def __getitem__(self, key: int) -> Coord:
        return self.beacons[key]

    def __iter__(self) -> Iterator[Coord]:
        return iter(self.beacons)


ScannerPair = NewType("ScannerPair", Tuple[int, int])
BeaconPair = NewType("BeaconPair", Tuple[int, int])


def identify(scanners: List[Scanner]) -> None:
    scanners[0].position = Coord(0, 0, 0)
    offsets: Dict[Offset, Dict[int, BeaconPair]] = defaultdict(dict)
    for s, beacons in enumerate(scanners):
        for i, j in itertools.combinations(range(len(beacons)), 2):
            offset = beacons[i] - beacons[j]
            norm_offset = offset.normalize()
            if 0 in norm_offset or len(set(norm_offset)) < 3:
                print(f"degenerate offset at {s}, {(i, j)}: {offset}")
            assert (
                s not in offsets[norm_offset]
            ), f"duplicate offset for scanner {s} at {norm_offset}"
            offsets[norm_offset][s] = BeaconPair((i, j))

    offsets = {k: v for k, v in offsets.items() if len(v) > 1}

    shared_lines: Dict[ScannerPair, List[Tuple[BeaconPair, BeaconPair]]] = defaultdict(
        list
    )
    for norm_offset, matches in offsets.items():
        quiet = False
        if len(matches) < 3:
            quiet = True
        if not quiet:
            print(f"normalized offset = {norm_offset}:")
        for s, (i, j) in matches.items():
            beacons = scanners[s]
            offset = beacons[i] - beacons[j]
            if not quiet:
                print(f"  scanner {s}: {offset:-5d}")
        for i, j in itertools.combinations(sorted(matches), 2):
            shared_lines[ScannerPair((i, j))].append((matches[i], matches[j]))
    print()

    located = 1
    while located < len(scanners):
        for indices, lines in shared_lines.items():
            if (scanners[indices[0]].position is None) ^ (
                scanners[indices[1]].position is None
            ):
                orient((scanners[indices[0]], scanners[indices[1]]), lines)
                located += 1


def orient(
    scanners: Tuple[Scanner, Scanner], lines: List[Tuple[BeaconPair, BeaconPair]]
) -> None:
    if scanners[0].position is not None:
        ref_index = 0
        unknown_index = 1
    else:
        ref_index = 1
        unknown_index = 0
    reference = scanners[ref_index]
    ref_lines = [l[ref_index] for l in lines]
    unknown = scanners[unknown_index]
    unknown_lines = [l[unknown_index] for l in lines]

    # get the first two beacons from the first entry
    ref_beacons: List[int] = list(ref_lines[0])
    unknown_beacons: List[int] = list(unknown_lines[0])

    # get a third beacon and figure out the order of the first two
    for i, pair in enumerate(ref_lines):
        # we want a pair with one beacon we already have and one we don't
        if len(set(ref_beacons) & set(pair)) != 1:
            continue
        # get the other index from the pair
        (new_ref,) = set(pair) - {ref_beacons[0]}
        ref_beacons.append(new_ref)

        # check the order of the first two unknown
        if unknown_beacons[0] not in unknown_lines[i]:
            # swap second and first unknown
            unknown_beacons[:2] = unknown_beacons[:2][::-1]

        # add the third to unknown
        (new_unknown,) = set(unknown_lines[i]) - {unknown_beacons[0]}
        unknown_beacons.append(new_unknown)

    # get a fourth beacon, the same way as the third
    for i, pair in enumerate(ref_lines):
        if len(set(ref_beacons) & set(pair)) != 1:
            continue
        (new_ref,) = set(pair) - set(ref_beacons)
        (old_ref,) = set(pair) - {new_ref}
        ref_beacons.append(new_ref)

        (new_unknown,) = set(unknown_lines[i]) - set(unknown_beacons)
        unknown_beacons.append(new_unknown)

    # TODO: construct a tetrahedron


def parse(lines: List[str]) -> List[Scanner]:
    scanners: List[Scanner] = []
    for line in lines:
        if line.startswith("---"):
            scanners.append(Scanner())
        elif line:
            scanners[-1].beacons.append(Coord(*map(int, line.split(","))))
    return scanners


def part_1(lines: List[str]) -> int:
    scanners = parse(lines)

    identify(scanners)
    print()

    reference = scanners[1][8] - scanners[1][24]
    offset = scanners[4][24] - scanners[4][3]
    # reference = Coord(-618, -824, -621) - Coord(-537, -823, -458)
    # offset = Coord(686, 422, 578) - Coord(605, 423, 415)

    if reference.normalize() == offset.normalize():
        print("reference:", reference)
        print("offset:   ", offset)
        print(offset.orient_to(reference))

    return -1
