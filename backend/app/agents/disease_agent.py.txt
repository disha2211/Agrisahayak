from app.core.constants import DISEASE_DATABASE

from app.schemas.agent import DiseaseAnalysis


class DiseaseAgent:

    def analyze(
        self,
        prediction,
    ):

        disease = prediction["disease"]

        info = DISEASE_DATABASE.get(
            disease,
            None,
        )

        if info is None:

            return DiseaseAnalysis(

                crop="Unknown",

                disease=disease,

                confidence=prediction["confidence"],

                severity="Unknown",

                recommended_action="Consult expert.",

                needs_weather=False,

                needs_rag=True,

            )

        return DiseaseAnalysis(

            crop=info["crop"],

            disease=disease,

            confidence=prediction["confidence"],

            severity=info["severity"],

            recommended_action=info[
                "recommended_action"
            ],

            needs_weather=info[
                "needs_weather"
            ],

            needs_rag=info[
                "needs_rag"
            ],
        )