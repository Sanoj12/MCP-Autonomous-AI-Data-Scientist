from langgraph.graph import StateGraph,START,END

from langgraph.checkpoint.memory import InMemorySaver

from Backend.app.graph.state import DataScientistState
from Backend.app.graph.node import(
    load_node, analysis_node, cleaning_node,
    target_node, problem_type_node,
    feature_node, data_leakage_node,
    train_test_split_node, data_preprocessor_node,
    model_selection_node, model_training_node, model_evalution_node,
    critic_node, retrain_node,
    mlflow_node, registry_node, approval_node,artifiacts_node
)


#Build LANGGRAPH workflow


def approval_router(state: DataScientistState):

    if state["human_approved"]:

        return "approved"

    return "rejected"


def build_workflow():

    builder = StateGraph(DataScientistState)


    ##add node
    builder.add_node("load_data",load_node)
    builder.add_node("data_analysis",analysis_node)
    builder.add_node("clean_data",cleaning_node)
    builder.add_node("target_column",target_node)
    builder.add_node("problem_type",problem_type_node)
    builder.add_node("feature_engineering",feature_node)
    builder.add_node("data_leakage",data_leakage_node)
    builder.add_node("data_split",train_test_split_node)
    builder.add_node("data_preprocess",data_preprocessor_node)
    builder.add_node("model_selection",model_selection_node)
    builder.add_node("model_training",model_training_node)
    builder.add_node("model_evaluation",model_evalution_node)
    builder.add_node("critic",critic_node)

    builder.add_node("mlflow",mlflow_node)
    builder.add_node("model_registry",registry_node)
    

    builder.add_node("approval",approval_node)
    builder.add_node("retrain_model",retrain_node)
    builder.add_node("artifact",artifiacts_node)



     ###main workflow pipeline

    builder.add_edge(START, "load_data")

    builder.add_edge("load_data" , "data_analysis")

    builder.add_edge("data_analysis","clean_data")

    builder.add_edge("clean_data","target_column")

    builder.add_edge("target_column","problem_type")

    builder.add_edge("problem_type","feature_engineering")

    builder.add_edge("feature_engineering","data_leakage")

    builder.add_edge("data_leakage","data_split")

    builder.add_edge("data_split","data_preprocess")

    builder.add_edge("data_preprocess","model_selection")

    builder.add_edge("model_selection","model_training")

    builder.add_edge("model_training","model_evaluation")

    builder.add_edge("model_evaluation","critic")

    builder.add_edge("critic","mlflow")

   

    
    builder.add_edge("mlflow","model_registry")

    builder.add_edge("model_registry","approval")

    builder.add_conditional_edges(
        "approval",
        approval_router,
        {
            "approved":"artifact",
            "rejected":"retrain_model"
        }
    )

    builder.add_edge("retrain_model","model_evaluation")


    builder.add_edge("artifact",END)

    checkpointer = InMemorySaver()

    workflow=builder.compile(
        checkpointer=checkpointer
    )


    return workflow





###data ingestion workflow load->analysis->clean data

def data_ingestion_workflow():

    builder = StateGraph(DataScientistState)

    builder.add_node(
        "load_data",load_node
    )
    builder.add_node(
        "data_analysis",analysis_node
    )
    builder.add_node(
        "clean_data",cleaning_node
    )


    ##edges
    builder.add_edge(START,"load_data")
    builder.add_edge("load_data","data_analysis")
    builder.add_edge("data_analysis","clean_data")
    builder.add_edge("clean_data",END)

    return builder.compile()


####data preprocessing workflow

def data_preprocessing_workflow():

    builder =StateGraph(DataScientistState)

    builder.add_node("target_column",target_node)
    builder.add_node("problem_type",problem_type_node)
    builder.add_node("feature_engineering",feature_node)
    builder.add_node("data_leakage",data_leakage_node)
    builder.add_node("data_split",train_test_split_node)
    builder.add_node("data_preprocess",data_preprocessor_node)

    #add edges
    builder.add_edge(START,"target_column")

    builder.add_edge("target_column","problem_type")
    
    builder.add_edge("problem_type","feature_engineering")
    
    builder.add_edge("feature_engineering","data_leakage")
    
    builder.add_edge("data_leakage","data_split")
    
    builder.add_edge("data_split","data_preprocess")

    builder.add_edge("data_preprocess",END)

    return builder.compile()



####Training workflow
#  model selection -> model training

def data_training_workflow():

    builder = StateGraph(DataScientistState)

    builder.add_node("model_selection",model_selection_node)
    builder.add_node("model_training",model_training_node)

    ##edge

    builder.add_edge(START,"model_selection")
    builder.add_edge("model_selection","model_training")
    builder.add_edge("model_training",END)

    return builder.compile()


##model evaluation workflow

def model_evaluation_workflow():

    builder = StateGraph(DataScientistState)

    builder.add_node("model_evaluation",model_evalution_node)
    builder.add_node("critic",critic_node)
    

    ##edge
    builder.add_edge(START,"model_evalution")

    builder.add_edge("model_evaluation","critic")

    
    builder.add_edge("critic",END)

    return builder.compile()


##model deployment workflow mlflow ->artifact


def model_deployment_workflow():

    builder = StateGraph(DataScientistState)

    ##add node
    builder.add_node("mlflow",mlflow_node)
    builder.add_node("model_registry",registry_node)
    builder.add_node("approval",approval_node)
    builder.add_node("retrain_model",retrain_node)
    builder.add_node("artifact",artifiacts_node)
    builder.add_node("model_evaluation",model_evalution_node)
    builder.add_node("critic",critic_node)
  

    ##add_Egde
   
    builder.add_edge(START,"mlflow")
    
    builder.add_edge("mlflow","model_registry")
    
    builder.add_edge("model_registry","approval")
    
    builder.add_conditional_edges(
            "approval",
            approval_router,
            {
                "approved":"artifact",
                "rejected":"retrain_model"
            }
        )
    
    builder.add_edge("retrain_model","model_evaluation")

    builder.add_edge("model_evaluation","critic")

    builder.add_edge("critic","mlflow")

    
    builder.add_edge("artifact",END)

    checkpointer=checkpointer
    return builder.compile(checkpointer=None)
        

 

    

