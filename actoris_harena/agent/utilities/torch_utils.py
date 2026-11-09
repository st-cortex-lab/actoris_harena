"""Compatibility path: this module moved to ``actoris_harena.torch_utils``
(837bebf), unchanged apart from additions. Callers written against the old
path import from here, some with ``import *``, so everything public is
re-exported, including ``torch``, ``nn`` and ``F``, which those callers use
through the star import. ``OPTIMISER_CLASSES`` did not survive the move and
is defined here as it was."""

from actoris_harena.torch_utils import *  # noqa: F401,F403
from actoris_harena.torch_utils import (  # noqa: F401
    ACTIVATIONS,
    np_to_ts,
    soft_update_params,
    ts_to_np,
)

OPTIMISER_CLASSES = {"adam": optim.Adam}  # noqa: F405
