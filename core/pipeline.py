from dataclasses import dataclass, field
from typing import Callable, List, Any


@dataclass
class PipelineStage:
    """
    One processing stage of the research pipeline.
    """

    name: str

    function: Callable[[Any], Any]


class ResearchPipeline:
    """
    AncientScriptLab Research Pipeline

    Each stage receives an object and returns an object.

    The pipeline itself knows nothing about
    Indus, Rongorongo or any specific writing system.
    """

    def __init__(self):

        self.stages: List[PipelineStage] = []

    # ------------------------------------------------

    def add_stage(self, name, function):

        self.stages.append(

            PipelineStage(

                name=name,

                function=function

            )

        )

    # ------------------------------------------------

    def run(self, data):

        result = data

        for stage in self.stages:

            print(f"[PIPELINE] {stage.name}")

            result = stage.function(result)

        return result

    # ------------------------------------------------

    def summary(self):

        return {

            "stages": len(self.stages),

            "names": [x.name for x in self.stages]

        }

