from __future__ import annotations

from core.context.feature_context import FeatureContext
from core.execution.algorithm import Algorithm


class AspectRatio(Algorithm):

    name = "aspect_ratio"

    def execute(self, context: FeatureContext) -> float:

        bbox = context.bounding_box

        if bbox.height == 0:
            return 0.0

        return float(bbox.width / bbox.height)