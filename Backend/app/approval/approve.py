


def request_approval(
        model_name: str,
        model_version: int,
        metrics: dict,
        shap_summary: dict
) -> dict:

    """request the human approval for a registered model"""

    try:

        if not isinstance(model_name,str):
            raise ValueError("model_name must be string")

        if not isinstance(model_version,int):

            raise ValueError("model_version must be an integer")

        if not isinstance(metrics,dict):

            raise ValueError("metrics must be a dictionary")

        if not isinstance("shap_summary",dict):

            raise ValueError("shap_summary must be a dictionary")



        decision = input("\n Approve model for final artifact? (yes/no):").strip().lower()

        if decision == "yes":

            return{
                "approved":True,
                "model_name":model_name,
                "model_version":model_version,
                "message":"Model approved"
            }

        if decision == "no":

            return{
                "approved":False,
                "model_name":model_name,
                "model_version":model_version,
                "message":"Model rejected"
            }

    except Exception as e:
        raise RuntimeError(f"approved failed:{e}") from e