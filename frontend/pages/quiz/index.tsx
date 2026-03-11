import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/router";
import Layout from "../../components/Layout";
import api from "../../lib/api";

export default function QuizPage() {
  const router = useRouter();
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<any>({});
  const [startTimes, setStartTimes] = useState<any>({});
  const [idx, setIdx] = useState(0);
  const [skipCount, setSkipCount] = useState(0);
  const [result, setResult] = useState<any>(null);

  const courseId = useMemo(() => Number(localStorage.getItem("selected_course") || "1"), []);

  useEffect(() => {
    api.get(`/api/quiz/diagnostic/${courseId}`).then((res) => {
      setQuestions(res.data.questions);
      const now = Date.now();
      const map = {};
      res.data.questions.forEach((q: any) => (map[q.id] = now));
      setStartTimes(map);
    });
  }, [courseId]);

  const select = (selected: number | null) => {
    const q = questions[idx];
    if (!q) return;

    if (selected === null) {
      if (skipCount >= 2) return alert("Skip limit reached (2)");
      setSkipCount((s) => s + 1);
    }

    const elapsed = Math.floor((Date.now() - startTimes[q.id]) / 1000);
    setAnswers((prev) => ({ ...prev, [q.id]: { selected, time_taken: elapsed } }));
    if (idx < questions.length - 1) setIdx((i) => i + 1);
  };

  const submit = async () => {
    const payload = questions.map((q) => ({
      question_id: q.id,
      selected: answers[q.id]?.selected ?? null,
      time_taken: answers[q.id]?.time_taken ?? 0,
    }));

    const { data } = await api.post("/api/quiz/submit", { course_id: courseId, answers: payload });
    setResult(data);
  };

  if (!questions.length) {
    return <Layout><p>Loading quiz...</p></Layout>;
  }

  if (result) {
    return (
      <Layout>
        <div className="card space-y-3">
          <h2 className="text-2xl font-bold">AI Analysis Complete</h2>
          <p>Score: <b>{result.quiz_result.score}%</b></p>
          <p>Knowledge Level: <b>{result.learner_profile.knowledge_level}</b></p>
          <p>Learning Speed: <b>{result.learner_profile.learning_speed}</b></p>
          <p>Weak Topics: {result.learner_profile.weak_topics.join(", ") || "None"}</p>
          <button className="btn-primary" onClick={() => router.push("/dashboard")}>Go to Dashboard</button>
        </div>
      </Layout>
    );
  }

  const current = questions[idx];

  return (
    <Layout>
      <div className="card space-y-3">
        <h2 className="text-xl font-bold">Diagnostic Quiz ({idx + 1}/{questions.length})</h2>
        <p>Skips used: {skipCount}/2</p>
        <p className="font-medium">{current.question}</p>
        <div className="grid gap-2">
          {current.options.map((opt, i) => (
            <button key={i} className="btn-secondary text-left" onClick={() => select(i)}>{opt}</button>
          ))}
          <button className="btn-secondary" onClick={() => select(null)}>Skip</button>
        </div>
        {idx === questions.length - 1 && (
          <button className="btn-primary" onClick={submit}>Submit Quiz</button>
        )}
      </div>
    </Layout>
  );
}
