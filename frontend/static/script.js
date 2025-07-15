document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('summary-form');
    const loadingBox = document.getElementById('loading');
    const errorBox = document.getElementById('error');
    const fullNarrativeText = document.getElementById('narrativeText');
    const summarizedText = document.getElementById('summaryText');
    const copyButtons = document.querySelectorAll('.copyBtn');
    const advancedToggle = document.getElementById('advanced-toggle');
    const advancedSection = document.getElementById('advanced-section');
	
	
	document.getElementById('video-path').value = './temp/video';
    // Toggle advanced settings
    advancedToggle.addEventListener('click', () => {
        advancedSection.classList.toggle('hidden');
        advancedToggle.textContent = advancedSection.classList.contains('hidden') ? "Show Advanced Settings" : "Hide Advanced Settings";
    });

    // Handle form submit
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        loadingBox.classList.remove('hidden');
        errorBox.classList.add('hidden');
        fullNarrativeText.value = "Loading results...";
        summarizedText.value = "";

        const fileInput = document.getElementById('file');
        const file = fileInput.files[0];
        if (!file) {
            loadingBox.classList.add('hidden');
            errorBox.textContent = "❗ Please upload a video file.";
            errorBox.classList.remove('hidden');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        // Append advanced settings
        ["audio", "video", "frame", "narrative"].forEach(section => {
            const input = document.getElementById(`${section}-settings`);
            formData.append(`${section}_settings`, input.value);
        });

        try {
            const response = await fetch("/summarize", {
                method: "POST",
                body: formData
            });

            const html = await response.text();
            document.open();
            document.write(html);
            document.close();
        } catch (error) {
            loadingBox.classList.add('hidden');
            errorBox.textContent = "⚠️ Internal server error or connection failed.";
            errorBox.classList.remove('hidden');
        }
    });

    // Copy to clipboard buttons
    copyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            const textarea = document.getElementById(targetId);
            if (textarea) {
                navigator.clipboard.writeText(textarea.value).then(() => {
                    btn.textContent = "✅ Copied!";
                    setTimeout(() => btn.textContent = "Copy to Clipboard", 2000);
                }).catch(err => {
                    alert("Copy failed: " + err);
                });
            }
        });
    });
});
