from __future__ import annotations

import os
import ants
import bids
import logging
import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="m-pitou-rage -- a simple BIDS-app to transfrom MP2RAGE for T1w processing (sMRIPrep, freesurfer)")
    p.add_argument("bids_path", help="path to the BIDS dataset")
    p.add_argument("derivatives_path", help="path to the output BIDS dataset")
    p.add_argument(
        "--participant-label",
        action="store",
        nargs="+",
        default=bids.layout.Query.ANY,
        help="a space delimited list of participant identifiers or a single "
        "identifier (the sub- prefix can be removed)",
    )
    p.add_argument(
        "--session-label",
        action="store",
        nargs="+",
        default=[bids.layout.Query.NONE, bids.layout.Query.ANY],
        help="a space delimited list of sessions identifiers or a single "
        "identifier (the ses- prefix can be removed)",
    )
    p.add_argument(
        "--version-specific",
        action="store_true",
        default=False,
        help="allow schema to be specific to the scanner software version",
    )
    return p.parse_args()


def mp2rage_to_t1w(
    unit1_path:Path,
    inv2_path:Path,
    out_path:Path,
) -> None:

    unit1 = ants.image_read(unit1_path)
    inv2 = ants.image_read(inv2_path)

    # remove bias from inv2 image
    inv2_n4 = ants.abp_n4(inv2)
    inv2_n4_norm = ants.iMath(inv2_n4, "Normalize")

    unit1_inv2 = unit1 * inv2_n4_norm
    out_path.parent.mkdir(parents=True, exist_ok=True)
    unit1_inv2.to_filename(out_path)


def main() -> None:
    args = parse_args()
    layout = bids.BIDSLayout(os.path.abspath(args.bids_path))

    unit1_paths = layout.get(
        suffix="UNIT1",
        extension=".nii.gz",
        subject=args.participant_label,
        session=args.session_label,
    )

    for unit1 in unit1_paths:
        inv2_entities = unit1.get_entities().copy()
        inv2_entities["suffix"] = "MP2RAGE"
        inv2_entities["inv"] = 2
        print(inv2_entities)
        inv2 = layout.get(**inv2_entities)
        assert len(inv2) > 0, f"No second inversion image found for {unit1.relpath}"
        assert len(inv2) == 1, f"Multiple second inversion image found for {unit1.relpath}, not BIDS valid."
        inv2 = inv2[0]

        out_entities = unit1.get_entities().copy()
        out_entities["suffix"] = "T1w"
        out_entities["acq"] = "mp2rage"
        out_entities["rec"] = "unit1xinv2"
        out_path = Path(layout.build_path(out_entities).replace(args.bids_path, args.derivatives_path))
        logging.info("processing %s %s", unit1.relpath, inv2.relpath)
        mp2rage_to_t1w(unit1.path, inv2.path, out_path)

if __name__ == "__main__":
    main()
