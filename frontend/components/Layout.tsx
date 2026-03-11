import Link from "next/link";

export default function Layout({ children }) {
  return (
    <div className="min-h-screen">
      <header className="bg-dark text-white px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">EduVora</h1>
        <nav className="flex gap-4 text-sm">
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/courses">Courses</Link>
          <Link href="/quiz">Quiz</Link>
          <Link href="/coding_workspace">Coding Workspace</Link>
        </nav>
      </header>
      <main className="max-w-6xl mx-auto p-6">{children}</main>
    </div>
  );
}
