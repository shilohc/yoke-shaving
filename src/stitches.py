from typing import Optional
import yoke_pb2


def _make_stitch_type(
    descriptor: str = "", height_factor: Optional[float] = 1.0
) -> yoke_pb2.StitchType:
    try:
        name, count = descriptor.split(" ")
        count_before, count_after = count.split("/")
        count_before = int(count_before)
        count_after = int(count_after)
        assert count_before >= 0
        assert count_after >= 0
    except Exception as e:
        print(f"Malformed descriptor {descriptor}: {e}")
        raise

    return yoke_pb2.StitchType(
        name=name,
        count_before=count_before,
        count_after=count_after,
        height_factor=height_factor,
    )


builtin_stitch_types = dict()
for stitch_type in [
    _make_stitch_type("k 1/1"),
    _make_stitch_type("p 1/1"),
    _make_stitch_type("yo 0/1"),
    _make_stitch_type("m1r 1/2"),
    _make_stitch_type("m1l 1/2"),
    _make_stitch_type("k2tog 2/1"),
    _make_stitch_type("ssk 2/1"),
]:
    builtin_stitch_types[stitch_type.name] = stitch_type
