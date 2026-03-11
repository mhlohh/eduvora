import { useRouter } from "next/router";

export default function NotificationsPage() {
  const router = useRouter();

  const choose = async (choice: string) => {
    if (choice !== "don't_allow" && typeof window !== "undefined" && "Notification" in window) {
      try {
        await Notification.requestPermission();
      } catch {
        // ignore for unsupported browsers
      }
    }
    router.push("/login");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="card max-w-lg w-full space-y-4">
        <h1 className="text-2xl font-bold">Enable Notifications</h1>
        <p>Choose how EduVora should notify you about study reminders and streaks.</p>
        <div className="grid gap-2">
          <button className="btn-primary" onClick={() => choose("allow")}>Allow while using the app</button>
          <button className="btn-secondary" onClick={() => choose("once")}>Only this time</button>
          <button className="btn-secondary" onClick={() => choose("don't_allow")}>Don't allow</button>
        </div>
      </div>
    </div>
  );
}
