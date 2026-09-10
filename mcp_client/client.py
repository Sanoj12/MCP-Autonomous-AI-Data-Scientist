from mcp.client import Client


def mcp_client():

    #connect to mcp server
    client = Client("http://127.0.0.1:8000")
    client.connect()

    state = {"dataset_path": "data/house_data.csv", "human_approved": True}


    ##run full pipeline
    
    pipeline_result = client.call_tool("run_pipeline",{"state":state})
    print("pipeline_result:",pipeline_result)


    ###run data ingestion tool

    data_ingestion_result = client.call_tool("run_data_ingestion",{"state":state})
    print("data_ingestion_result:",data_ingestion_result)


    #data preprocessing tool
    data_preprocessing_result  =client.call_tool("run_data_preprocesing",{"state":state})
    print("data_preprocessing_result:",data_preprocessing_result)


    ##model selection tool
    model_selection_result= client.call_tool("run_model_selection",{"state":state})
    print("model_selection_result",model_selection_result)


    ##model evaluation tool
    model_evaluation_result = client.call_tool("run_model_evaluation",{"state":state})
    print("model_evaluation_result",model_evaluation_result)


    ###model deployment tool
    model_deployment_result = client.call_tool("run_model_deployment",{"state":state})
    print("model_deployment_result",model_deployment_result)

    client.close()

if __name__ == "__main__":
    mcp_client()