"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {

  const [file, setFile] = useState<File | null>(null);

  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {

    const selectedFile = event.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
    }
  };
   
  //approval model
  const approveModel = async()=>{
    
      try{

         if(!result?.best_model_name){
           alert ("best model not found");
           return;
         }


         const response = await fetch(
            `${API_URL}/approve?best_model=${encodeURIComponent(
                   result.best_model_name
            )}`,
            {
              method:"POST"
            }
         );
         const data = await response.json();

         console.log("approved response:",data)

         if (!response.ok) {
           throw new Error(data.detail || "Approval failed");
         }

         setResult({
          ...result,
          approved:true,
          download_url:data.download_url

         })


      }catch(error){
         console.log("Approve error",error)
         alert("approval failed")
      }
  }

  //human rejected - retrain model
  const rejectModel = async()=>{

        try{

          const response = await fetch(
            `${API_URL}/retrain`,
            {
              method:"POST",
            }
          )
          const data =await response.json()

          console.log("retrained result:",data)

          if(!response.ok){
            throw new Error(data.detail || "retrain is failed")
          }

          setResult(data)

        }catch(error){
            console.log("retraine error:",error)
            alert("Retrained failed")
        }
        
  }


  const runPipeline = async () => {

    if (!file) {
      alert("Please select a dataset");
      return;
    }

    if (!query.trim()) {
      alert("Please enter your objective");
      return;
    }

    try {

      setLoading(true);

      const formData = new FormData();

      formData.append("file", file);
      formData.append("query", query);


      const response = await fetch(
        `${API_URL}/run_pipeline`,
        {
          method: "POST",
          body: formData
        }
      );


      if (!response.ok) {
        throw new Error("Pipeline failed");
      }


      const data = await response.json();

      console.log("pipeline result", data);

      setResult(data);

    } catch (error) {

      console.error(error);
      alert("Pipeline failed");

    } finally {

      setLoading(false);

    }
  };

return (
  <main className="min-h-screen bg-gray-100 p-4">

    <div className="max-w-7xl mx-auto">

      {/* HEADER */}
      <div className="mb-4">
        <h1 className="text-2xl font-bold">
          AI Data Scientist
        </h1>

        <p className="text-gray-600 text-sm mt-1">
          Upload your dataset and describe your objective.
        </p>
      </div>

      {/* INPUT SECTION */}
      <div className="bg-white p-4 rounded-lg shadow mb-4">

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          {/* FILE */}
          <div>
            <label className="font-semibold text-sm">
              Upload Dataset
            </label>

            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileChange}
              className="w-full border p-2 rounded mt-1 text-sm"
            />

            {file && (
              <p className="mt-1 text-xs text-gray-600">
                Selected: {file.name}
              </p>
            )}
          </div>

          {/* OBJECTIVE */}
          <div>
            <label className="font-semibold text-sm">
              Business Objective
            </label>

            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Example: Predict customer churn"
              rows={2}
              className="w-full border p-2 rounded mt-1 text-sm"
            />
          </div>

        </div>

        {/* RUN BUTTON */}
        <button
          disabled={loading}
          onClick={runPipeline}
          className="w-full bg-black text-white p-2.5 rounded mt-4 disabled:bg-gray-400"
        >
          {loading ? "Running Pipeline..." : "Run Pipeline"}
        </button>

      </div>

      {/* RESULT SECTION */}
      <div className="bg-white p-5 rounded-lg shadow">

        <h2 className="text-xl font-bold mb-4">
          Pipeline Result
        </h2>

        {!result && (
          <div className="text-gray-500 text-center py-20">
            Run the pipeline to see results here.
          </div>
        )}

        {result && (
          <div>

            {/* TOP RESULT INFORMATION */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">

              <div className="bg-gray-100 p-4 rounded">
                <p className="text-gray-500 text-sm">
                  Problem Type
                </p>

                <p className="text-lg font-bold capitalize">
                  {result.problem_type}
                </p>
              </div>

              <div className="bg-gray-100 p-4 rounded">
                <p className="text-gray-500 text-sm">
                  Best Model
                </p>

                <p className="text-lg font-bold">
                  {result.best_model_name}
                </p>
              </div>

            </div>

            {/* CLASSIFICATION */}
            {result.problem_type === "classification" && (
              <div>

                <h3 className="font-bold mb-3">
                  Classification Metrics
                </h3>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">

                  {/* ACCURACY */}
                  <div className="bg-gray-100 p-3 rounded">
                    <p className="text-gray-500 text-sm">
                      Accuracy
                    </p>

                    <p className="text-lg font-bold">
                      {result.best_metrics?.accuracy !== undefined
                        ? `${(
                            result.best_metrics.accuracy * 100
                          ).toFixed(2)}%`
                        : "-"}
                    </p>
                  </div>

                  {/* PRECISION */}
                  <div className="bg-gray-100 p-3 rounded">
                    <p className="text-gray-500 text-sm">
                      Precision
                    </p>

                    <p className="text-lg font-bold">
                      {result.best_metrics?.precision !== undefined
                        ? `${(
                            result.best_metrics.precision * 100
                          ).toFixed(2)}%`
                        : "-"}
                    </p>
                  </div>

                  {/* RECALL */}
                  <div className="bg-gray-100 p-3 rounded">
                    <p className="text-gray-500 text-sm">
                      Recall
                    </p>

                    <p className="text-lg font-bold">
                      {result.best_metrics?.recall !== undefined
                        ? `${(
                            result.best_metrics.recall * 100
                          ).toFixed(2)}%`
                        : "-"}
                    </p>
                  </div>

                  {/* F1 SCORE */}
                  <div className="bg-gray-100 p-3 rounded">
                    <p className="text-gray-500 text-sm">
                      F1 Score
                    </p>

                    <p className="text-lg font-bold">
                      {result.best_metrics?.f1_score !== undefined
                        ? `${(
                            result.best_metrics.f1_score * 100
                          ).toFixed(2)}%`
                        : "-"}
                    </p>
                  </div>

                </div>
              </div>
            )}

            {/* REGRESSION */}
            {result.problem_type === "regression" && (
              <div>

                <h3 className="font-bold mb-3">
                  Regression Metrics
                </h3>

                <div className="grid grid-cols-3 gap-3">

                  {/* MAE */}
                  <div className="bg-gray-100 p-3 rounded">
                    <p className="text-gray-500 text-sm">
                      MAE
                    </p>

                    <p className="text-lg font-bold">
                      {result.best_metrics?.mae !== undefined
                        ? result.best_metrics.mae.toFixed(2)
                        : "-"}
                    </p>
                  </div>

                  {/* RMSE */}
                  <div className="bg-gray-100 p-3 rounded">
                    <p className="text-gray-500 text-sm">
                      RMSE
                    </p>

                    <p className="text-lg font-bold">
                      {result.best_metrics?.rmse !== undefined
                        ? result.best_metrics.rmse.toFixed(2)
                        : "-"}
                    </p>
                  </div>

                  {/* R2 */}
                  <div className="bg-gray-100 p-3 rounded">
                    <p className="text-gray-500 text-sm">
                      R² Score
                    </p>

                    <p className="text-lg font-bold">
                      {result.best_metrics?.r2 !== undefined
                        ? result.best_metrics.r2.toFixed(4)
                        : "-"}
                    </p>
                  </div>

                </div>
              </div>
            )}

            {/* HUMAN APPROVAL */}
            {result?.__interrupt__ && (
              <div className="mt-6 border-t pt-5">

                <h3 className="font-bold mb-3">
                  Human Approval
                </h3>

                <div className="flex gap-3">

                  <button
                      onClick={approveModel}
                   
                    className="flex-1 bg-green-600 text-white p-3 rounded hover:bg-green-700"
                  >
                    ✓ Approve
                  </button>

                  <button
                    onClick={rejectModel}
                    className="flex-1 bg-red-600 text-white p-3 rounded hover:bg-red-700"
                  >
                    ✕ Reject & Retrain
                  </button>

                </div>
              </div>
            )}

            {/* APPROVED RESULT */}
            {result?.approved && (
              <div className="mt-6 border-t pt-5">

                {/* SUCCESS MESSAGE */}
                <div className="bg-green-100 text-green-800 p-3 rounded mb-5">
                  ✓ Model approved successfully
                </div>

                {/* BEST MODEL */}
                <div className="bg-gray-100 p-4 rounded mb-5">

                  <p className="text-gray-500 text-sm">
                    Best Model
                  </p>

                  <p className="text-xl font-bold">
                    {result.best_model_name}
                  </p>

                  {/* BEST F1 SCORE */}
                  {result.problem_type === "classification" &&
                    result.best_metrics?.f1_score !== undefined && (
                      <p className="mt-2 text-gray-700">
                        Best F1 Score:{" "}
                        <span className="font-bold">
                          {(
                            result.best_metrics.f1_score * 100
                          ).toFixed(2)}
                          %
                        </span>
                      </p>
                    )}

                  {/* BEST R2 SCORE */}
                  {result.problem_type === "regression" &&
                    result.best_metrics?.r2 !== undefined && (
                      <p className="mt-2 text-gray-700">
                        Best R² Score:{" "}
                        <span className="font-bold">
                          {result.best_metrics.r2.toFixed(4)}
                        </span>
                      </p>
                    )}

                </div>

                {/* DOWNLOAD ARTIFACT */}
                <div>

                  <h3 className="text-lg font-bold mb-3">
                    Model Artifact
                  </h3>

                  <a
                    href={`${API_URL}/artifacts/models.pkl`}
                    download="models.pkl"
                     onClick={() => {
                              alert("✓ Model downloaded successfully");
                     }}
                    className="block w-full text-center bg-black text-white p-3 rounded-lg hover:bg-gray-800"
                  >
                    ↓ Download model.pkl
                  </a>

                </div>

              </div>
            )}

          </div>
        )}

      </div>

    </div>

  </main>
);
}