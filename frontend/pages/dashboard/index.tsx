import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import DashboardCharts from "../../components/DashboardCharts";
import api from "../../lib/api";

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [message, setMessage] = useState("");
  const [tutor, setTutor] = useState<any>(null);

  useEffect(() => {
    const courseId = Number(localStorage.getItem("selected_course") || "1");
    api.get("/api/dashboard").then((res) => setData(res.data));
    api.get(`/api/recommendations/${courseId}`).then((res) => setRecommendations(res.data.recommendations || []));
  }, []);

  const askTutor = async () => {
    const { data } = await api.post("/api/tutor/chat", { message, context: {} });
    setTutor(data);
  };

  if (!data) return <Layout><p>Loading dashboard...</p></Layout>;

  return (
    <Layout>
      <div className="grid md:grid-cols-4 gap-4 mb-4">
        <div className="card"><p className="text-sm">Progress Level</p><p className="text-xl font-bold">{data.progress_level}</p></div>
        <div className="card"><p className="text-sm">Learning Streak</p><p className="text-xl font-bold">{data.learning_streak} days</p></div>
        <div className="card"><p className="text-sm">Knowledge Level</p><p className="text-xl font-bold">{data.knowledge_level}</p></div>
        <div className="card"><p className="text-sm">Learning Speed</p><p className="text-xl font-bold">{data.learning_speed}</p></div>
      </div>

      <DashboardCharts weekly={data.weekly_learning_progress} mastery={data.topic_mastery_chart} />

      <div className="grid md:grid-cols-2 gap-4 mt-4">
        <div className="card">
          <h3 className="font-semibold mb-2">Strong vs Weak Topics</h3>
          <p><b>Strong:</b> {data.strong_topics.join(", ") || "None"}</p>
          <p><b>Weak:</b> {data.weak_topics.join(", ") || "None"}</p>
        </div>

        <div className="card">
          <h3 className="font-semibold mb-2">AI Recommendations</h3>
          <ul className="list-disc pl-6">
            {recommendations.map((r, i) => (
              <li key={i}>{r.title} ({r.type})</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card mt-4 space-y-2">
        <h3 className="font-semibold">AI Tutor</h3>
        <div className="flex gap-2">
          <input className="w-full border rounded p-2" placeholder="Ask a doubt..." value={message} onChange={(e) => setMessage(e.target.value)} />
          <button className="btn-primary" onClick={askTutor}>Ask</button>
        </div>
        {tutor && (
          <div>
            <p><b>Answer:</b> {tutor.answer}</p>
            <p><b>Practice:</b> {tutor.practice_questions.join(" | ")}</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
