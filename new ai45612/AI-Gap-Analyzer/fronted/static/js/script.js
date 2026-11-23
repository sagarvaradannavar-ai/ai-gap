
console.log("AI Gap Analyzer Dashboard Loaded!");

document.addEventListener("DOMContentLoaded", function () {

    const careerForm = document.getElementById("careerForm");

    if (!careerForm) {
        console.log("Career form not found on this page.");
        return;
    }

    careerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const resume = document.getElementById("resume").files[0];
        const career = document.getElementById("career").value;
        const skills = document.getElementById("skills").value.trim();

        const message = document.getElementById("careerMessage");
        const analyzeBtn = document.getElementById("analyzeBtn");
        const results = document.getElementById("analysisResults");

        if (!career) {
            message.textContent = "Please select your desired career.";
            return;
        }

        if (!resume && !skills) {
            message.textContent =
                "Please upload a resume or enter your current skills.";
            return;
        }

        if (resume && !resume.name.toLowerCase().endsWith(".pdf")) {
            message.textContent = "Please upload a PDF file only.";
            return;
        }

        const formData = new FormData();

        formData.append("career", career);
        formData.append("skills", skills);

        if (resume) {
            formData.append("resume", resume);
        }

        message.textContent = "Analyzing your skills. Please wait...";

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = "Analyzing...";

        results.hidden = true;

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/analyze-career",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Analysis failed.");
            }

            const matched = data.matched_skills || [];
            const missing = data.missing_skills || [];
            const recommendations = data.recommendations || [];

            const percentage = Math.max(
                0,
                Math.min(100, Number(data.match_percentage) || 0)
            );

            const total = matched.length + missing.length;

            // Career information
            document.getElementById("resultCareer").textContent =
                data.career;

            // Match percentage
            document.getElementById("matchPercentage").textContent =
                percentage + "%";

            document.getElementById("progressCircle").style.setProperty(
                "--score",
                percentage + "%"
            );

            // Dashboard statistics
            document.getElementById("totalSkills").textContent = total;
            document.getElementById("matchedCount").textContent =
                matched.length;

            document.getElementById("missingCount").textContent =
                missing.length;

            document.getElementById("matchedLabel").textContent =
                matched.length;

            document.getElementById("missingLabel").textContent =
                missing.length;

            // Display skill lists
            function displayList(elementId, items, emptyMessage) {

                const list = document.getElementById(elementId);

                list.replaceChildren();

                if (items.length === 0) {

                    const li = document.createElement("li");

                    li.textContent = emptyMessage;
                    li.className = "empty-list";

                    list.appendChild(li);

                    return;
                }

                items.forEach(function (item) {

                    const li = document.createElement("li");

                    li.textContent = item;

                    list.appendChild(li);

                });
            }

            displayList(
                "matchedSkills",
                matched,
                "No matched skills found."
            );

            displayList(
                "missingSkills",
                missing,
                "Excellent! No missing skills."
            );

            displayList(
                "recommendations",
                recommendations,
                "Keep practising your existing skills!"
            );

            // Show dashboard
            results.hidden = false;

            message.textContent = "Your career dashboard is ready!";

            // Scroll to dashboard
            results.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

            console.log("Dashboard Data:", data);

        }

        catch (error) {

            console.error("Analysis Error:", error);

            message.textContent = "Error: " + error.message;

        }

        finally {

            analyzeBtn.disabled = false;
            analyzeBtn.textContent = "Analyze My Skills →";

        }

    });

});
