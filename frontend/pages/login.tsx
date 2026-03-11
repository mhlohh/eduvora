import { useState } from "react";
import { useRouter } from "next/router";
import api from "../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");

  const loginEmail = async () => {
    const { data } = await api.post("/api/auth/login", { email, password });
    localStorage.setItem("eduvora_token", data.access_token);
    router.push("/personalization");
  };

  const loginMobile = async () => {
    const { data } = await api.post("/api/auth/login", { mobile, password });
    localStorage.setItem("eduvora_token", data.access_token);
    router.push("/personalization");
  };

  const loginGoogle = async () => {
    const fakeGoogleToken = `google-${Date.now()}`;
    const { data } = await api.post("/api/auth/google", { id_token: fakeGoogleToken });
    localStorage.setItem("eduvora_token", data.access_token);
    router.push("/personalization");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="card max-w-xl w-full space-y-4">
        <h1 className="text-2xl font-bold">Login to EduVora</h1>
        <div className="space-y-2">
          <input className="w-full border rounded p-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input className="w-full border rounded p-2" placeholder="Mobile" value={mobile} onChange={(e) => setMobile(e.target.value)} />
          <input type="password" className="w-full border rounded p-2" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <div className="grid md:grid-cols-3 gap-2">
          <button className="btn-primary" onClick={loginMobile}>Mobile number login</button>
          <button className="btn-primary" onClick={loginGoogle}>Continue with Google</button>
          <button className="btn-primary" onClick={loginEmail}>Continue with Email</button>
        </div>
      </div>
    </div>
  );
}
