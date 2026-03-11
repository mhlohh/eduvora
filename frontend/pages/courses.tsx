import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Layout from "../components/Layout";
import api from "../lib/api";

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const router = useRouter();

  useEffect(() => {
    api.get("/api/courses").then((res) => setCourses(res.data));
  }, []);

  const choose = (id: number) => {
    localStorage.setItem("selected_course", String(id));
    router.push("/quiz");
  };

  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-4">Choose Your Course</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {courses.map((c: any) => (
          <div key={c.id} className="card">
            <h3 className="font-bold text-lg">{c.name}</h3>
            <p className="text-slate-600 mb-3">{c.description}</p>
            <button className="btn-primary" onClick={() => choose(c.id)}>Start Diagnostic Quiz</button>
          </div>
        ))}
      </div>
    </Layout>
  );
}
