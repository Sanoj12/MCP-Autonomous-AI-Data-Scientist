from mcp.server.mcpserver import MCPServer
from app.ml.llm import llm
from app.graph.workflow import (
    build_workflow,
    data_ingestion_workflow,
    data_preprocessing_workflow,
    data_training_workflow,
    model_evaluation_workflow,
    model_deployment_workflow

)

workflow = build_workflow()
ingestion_workflow = data_ingestion_workflow()
preprocess_workflow = data_preprocessing_workflow()
trainig_workflow = data_training_workflow()
evaluation_workflow = model_evaluation_workflow()
deployment_workflow = model_deployment_workflow()

# initialize MCP Server
mcp = MCPServer("AutonomousDataScientist")


##full ml pipeline tool
@mcp.tool()
def run_pipeline(state:dict) -> dict:
    """run the full ml pipeline end-to-end"""

    ##inject llm to state
    state["llm"] = llm
    return workflow.invoke(state)


##for debugging tools -find and fix the problem

@mcp.tool()
def run_data_ingestion(state:dict) ->dict:

    """load file,data analysis,clean data"""

    return data_ingestion_workflow.invoke(state)


@mcp.tool()
def run_data_preprocesing(state:dict) ->dict:
    """target,problem_type,feature engineering,data leakage,split,preprocessing"""
    return data_preprocessing_workflow.invoke(state)

@mcp.tool()
def run_model_selection(state:dict) ->dict:
    """model selection and training"""
    return data_training_workflow.invoke(state)


@mcp.tool()
def run_model_evaluation(state:dict) ->dict:
    
    """model evaluation ,critic,shap explaination"""

    return model_evaluation_workflow.invoke(state)

@mcp.tool()
def run_model_deployment(state:dict) ->dict:
    """mlflow,model registry, approval, retrain,artifact"""
    

    return model_deployment_workflow.invoke(
        state,
        config={
        "configurable": {
            "thread_id": "test-1"
        }
    } )




if __name__ == "__main__":
    mcp.run(transport="streamable-http")