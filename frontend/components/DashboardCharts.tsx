import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Line, Doughnut } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Tooltip, Legend);

export default function DashboardCharts({ weekly, mastery }) {
  const lineData = {
    labels: weekly.map((x) => x.date),
    datasets: [
      {
        label: "Weekly Learning Progress",
        data: weekly.map((x) => x.score),
        borderColor: "#0ea5e9",
        backgroundColor: "rgba(14,165,233,0.2)",
      },
    ],
  };

  const topics = Object.keys(mastery || {});
  const values = Object.values(mastery || {});

  const doughnutData = {
    labels: topics,
    datasets: [
      {
        data: values,
        backgroundColor: ["#22c55e", "#f59e0b", "#ef4444", "#3b82f6", "#a855f7", "#14b8a6"],
      },
    ],
  };

  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="card">
        <h3 className="font-semibold mb-3">Weekly Progress</h3>
        <Line data={lineData} />
      </div>
      <div className="card">
        <h3 className="font-semibold mb-3">Topic Mastery</h3>
        <Doughnut data={doughnutData} />
      </div>
    </div>
  );
}
