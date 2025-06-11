document.getElementById("scanForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const url = document.getElementById("url").value;
  const enableKeywords = document.getElementById("keywords").checked;
  const enableForms = document.getElementById("forms").checked;
  const enableSubdomains = document.getElementById("subdomains").checked;
  const enableDirsearch = document.getElementById("dirsearch").checked;
  const enableScreenshots = document.getElementById("screenshots").checked;

  const requestBody = {
    url: url,
    enable_forms: enableForms,
    enable_keywords: enableKeywords,
    enable_subdomains: enableSubdomains,
    enable_dirsearch: enableDirsearch,
    enable_screenshots: enableScreenshots,
    enable_pdf_report: true
  };

  console.log("Request body to be sent:", requestBody);

  const output = document.getElementById("output");
  output.innerHTML = `<span style="color: #aaa;">⏳ The scan is being processed please wait...</span>`;

  fetch("/api/crawl", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestBody)
  })
    .then(async (res) => {
      const contentType = res.headers.get("content-type");

      // If returning JSON (Option 1)
      if (contentType && contentType.includes("application/json")) {
        const data = await res.json();

        let resultText = `✅ ${data.message}<br>🔗 URLs Found: ${data.total_urls}<br>`;

        if (data.report_generated && data.report_url) {
          const fullUrl = data.report_url;
          resultText += `📄 <a href="${fullUrl}" target="_blank" style="color:#4fd1c5;">Download Report</a>`;
        }

        output.innerHTML = resultText;
      } else if (res.ok) {
        // If returning a file directly (Option 2), force download
        const blob = await res.blob();
        const fileURL = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = fileURL;
        a.download = "ReconX_Report.pdf";
        a.click();
        output.innerHTML = "📄 Report downloaded successfully.";
      } else {
        const text = await res.text();
        throw new Error(text || res.statusText);
      }
    })
    .catch((error) => {
      output.innerHTML = `❌ <span style="color:#f87171;">Error: ${error.message}</span>`;
    });
});
