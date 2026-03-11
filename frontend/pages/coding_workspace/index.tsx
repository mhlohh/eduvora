import { useState } from "react";
import dynamic from "next/dynamic";
import Layout from "../../components/Layout";
import api from "../../lib/api";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export default function CodingWorkspacePage() {
  const [code, setCode] = useState("print(input())");
  const [result, setResult] = useState<any>(null);

  const run = async () => {
    const courseId = Number(localStorage.getItem("selected_course") || "2");
    const { data } = await api.post("/api/code/run", {
      course_id: courseId,
      language: "python",
      code,
      test_cases: [{ input: "hello", expected_output: "hello" }],
    });
    setResult(data);
  };

  return (
    <Layout>
      <div className="grid lg:grid-cols-2 gap-4">
        <div className="card">
          <h2 className="text-xl font-bold mb-3">Programming Practice</h2>
          <MonacoEditor
            height="420px"
            defaultLanguage="python"
            value={code}
            onChange={(v) => setCode(v || "")}
          />
          <button className="btn-primary mt-3" onClick={run}>Run Code</button>
        </div>

        <div className="card space-y-2">
          <h3 className="font-semibold">Execution & AI Feedback</h3>
          {result ? (
            <>
              <p><b>Output:</b> {result.execution.output || ""}</p>
              <p><b>Error:</b> {result.execution.error || "None"}</p>
              <p><b>Syntax errors:</b> {result.tracking.syntax_errors}</p>
              <p><b>Logic errors:</b> {result.tracking.logic_errors}</p>
              <p><b>Execution success:</b> {String(result.tracking.execution_success)}</p>
              <p><b>AI feedback:</b> {result.ai_feedback}</p>
            </>
          ) : (
            <p>Run code to see analysis.</p>
          )}
        </div>
      </div>
    </Layout>
  );
}
