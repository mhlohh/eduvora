import { useState } from "react";
import { useRouter } from "next/router";
import api from "../lib/api";
import Layout from "../components/Layout";

export default function PersonalizationPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [fieldOfStudy, setFieldOfStudy] = useState("");
  const [interest, setInterest] = useState("");

  const submit = async () => {
    await api.post("/api/users/personalization", {
      name,
      field_of_study: fieldOfStudy,
      learning_interest: interest,
    });
    router.push("/courses");
  };

  return (
    <Layout>
      <div className="card max-w-2xl">
        <h2 className="text-2xl font-bold mb-2">Hello, let's customize your EduVora journey</h2>
        <div className="space-y-3">
          <input className="w-full border rounded p-2" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
          <input className="w-full border rounded p-2" placeholder="Field of study" value={fieldOfStudy} onChange={(e) => setFieldOfStudy(e.target.value)} />
          <input className="w-full border rounded p-2" placeholder="Learning interest" value={interest} onChange={(e) => setInterest(e.target.value)} />
          <button className="btn-primary" onClick={submit}>Continue</button>
        </div>
      </div>
    </Layout>
  );
}
