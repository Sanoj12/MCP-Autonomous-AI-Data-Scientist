from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from Backend.app.graph.workflow import build_workflow

import os

app = FastAPI()

app.mount(
    "/artifacts",
    StaticFiles(directory="artifacts"),
    name="artifacts"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://mcp-autonomous-ai-data-scientist.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



workflow = build_workflow()


@app.get("/")
def root():
    return {"message": "FastAPI is running"}

@app.post("/run_pipeline")
async def run_pipeline(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    try:
        os.makedirs("uploads", exist_ok=True)

        file_path = os.path.join(
            "uploads",
            file.filename
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("file saved:", file_path)
        print("query:", query)

        state = {
            "file_path": file_path,
            "objective": query,
            "threshold": 0.80
        }

        print("Starting workflow...")

        result = workflow.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": "test-1"
                }
            }
        )

      

        print("WORKFLOW RESULT:")
    

        print("\n========== FINAL WORKFLOW STATE ==========")
        print(result)
        print("==========================================")

        print("best_model_name:", result.get("best_model_name"))
        print("best_metrics:", result.get("best_metrics"))
        print("best_columns:", result.get("best_columns"))
        
        return result

    except Exception as e:
        import traceback

        traceback.print_exc()

        return {
            "error": str(e)
        }



@app.post("/approve")

def approve(best_model: str):
    
    artifact_path = f"/artifacts/{best_model}.pkl"

    return {
        "approved":True,
        "download_url": artifact_path

    }

@app.post("/retrain")
def retrain():
    # Trigger retraining with different model
    new_result = workflow.invoke({"retrain": True},
             config={
                "configurable": {
                    "thread_id": "test-1"
                }
            })
    
    return {
        "best_model": new_result.get("best_model"),
        "metrics": new_result.get("metrics"),
        
    }