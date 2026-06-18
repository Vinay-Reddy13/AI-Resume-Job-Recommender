import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadResume = async () => {
    if (!file) {
      alert("Please select a resume PDF");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/upload-resume",
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Upload failed. Check FastAPI server and console.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h1 style={styles.title}>AI Resume Job Recommender</h1>
        <p style={styles.subtitle}>
          Upload your resume and get recommended job links based on your skills.
        </p>

        <div style={styles.uploadBox}>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button style={styles.button} onClick={uploadResume}>
            {loading ? "Analyzing..." : "Upload Resume"}
          </button>
        </div>

        {result && (
          <div style={styles.results}>
            <div style={styles.card}>
              <h2>Suggested Role</h2>
              <p style={styles.role}>{result.suggested_role}</p>
            </div>

            <div style={styles.card}>
              <h2>Extracted Skills</h2>
              <div style={styles.skills}>
                {result.skills.map((skill, index) => (
                  <span key={index} style={styles.skillBadge}>
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div style={styles.card}>
              <h2>Recommended Jobs</h2>

              {result.recommended_jobs.map((job, index) => (
                <div key={index} style={styles.jobCard}>
                  <h3>{job.title}</h3>
                  <p>
                    <strong>Company:</strong> {job.company}
                  </p>
                  <p>
                    <strong>Location:</strong> {job.location}
                  </p>
                  <p>
                    <strong>Match Score:</strong>{" "}
                    <span style={styles.score}>{job.match_score}%</span>
                  </p>

                  <p>
                    <strong>Matched Skills:</strong>{" "}
                    {job.matched_skills.join(", ")}
                  </p>

                  {job.missing_skills.length > 0 && (
                    <p>
                      <strong>Missing Skills:</strong>{" "}
                      {job.missing_skills.join(", ")}
                    </p>
                  )}

                  <a
                    href={job.apply_link}
                    target="_blank"
                    rel="noreferrer"
                    style={styles.link}
                  >
                    Apply Here
                  </a>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f6f8",
    padding: "40px",
    fontFamily: "Arial, sans-serif",
  },
  container: {
    maxWidth: "1000px",
    margin: "0 auto",
    background: "#ffffff",
    borderRadius: "12px",
    padding: "30px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
  },
  title: {
    textAlign: "center",
    fontSize: "42px",
    marginBottom: "10px",
  },
  subtitle: {
    textAlign: "center",
    color: "#666",
    marginBottom: "30px",
  },
  uploadBox: {
    display: "flex",
    justifyContent: "center",
    gap: "15px",
    marginBottom: "30px",
  },
  button: {
    background: "#2563eb",
    color: "white",
    border: "none",
    padding: "10px 18px",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  results: {
    marginTop: "30px",
  },
  card: {
    background: "#f9fafb",
    padding: "20px",
    borderRadius: "10px",
    marginBottom: "20px",
    border: "1px solid #e5e7eb",
  },
  role: {
    fontSize: "22px",
    fontWeight: "bold",
    color: "#2563eb",
  },
  skills: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
  },
  skillBadge: {
    background: "#dbeafe",
    color: "#1e40af",
    padding: "8px 12px",
    borderRadius: "20px",
    fontWeight: "bold",
  },
  jobCard: {
    background: "white",
    padding: "18px",
    borderRadius: "8px",
    marginTop: "15px",
    border: "1px solid #ddd",
  },
  score: {
    color: "#16a34a",
    fontWeight: "bold",
  },
  link: {
    display: "inline-block",
    marginTop: "10px",
    background: "#16a34a",
    color: "white",
    padding: "10px 14px",
    borderRadius: "6px",
    textDecoration: "none",
    fontWeight: "bold",
  },
};

export default App;