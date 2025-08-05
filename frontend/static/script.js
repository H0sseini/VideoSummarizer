document.getElementById("summarizeForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = this.querySelector("input[type='file']");
    const file = fileInput.files[0];
	const summarizeButton = document.getElementById("submitting");
	const toggleSettingsButton = document.getElementById("toggleSettings");
    if (!file) return;

    document.getElementById("fullNarrative").value = "⏳ Summarizing, please wait...";
    document.getElementById("summaryText").value = "⏳ Summarizing, please wait...";
	

    const formData = new FormData();
    formData.append("file", file);

    
	summarizeButton.disabled = true;
	toggleSettingsButton.disabled = true;

	try {
		const response = await fetch("/summarize", {
			method: "POST",
			body: formData,
		});
	
		const result = await response.json();
	
		if (result.status === "success") {
			document.getElementById("summary_textarea").value = result.summary;
			document.getElementById("full_textarea").value = result.fullNarrative;
		} else {
			document.getElementById("summary_textarea").value = "⚠️ An error occurred.";
			document.getElementById("full_textarea").value = result.message + "\n\n" + result.traceback;
		}
	
	} catch (err) {
		document.getElementById("summary_textarea").value = "⚠️ An error occurred.";
		document.getElementById("full_textarea").value = err.message;
	} finally {
		summarizeButton.disabled = false;
		toggleSettingsButton.disabled = false;
	}
	
});

document.getElementById("toggleSettings").addEventListener("click", async function () {
    const settingsDiv = document.getElementById("settingsSection");

    // Toggle visibility
    settingsDiv.style.display = settingsDiv.style.display === "none" ? "block" : "none";

    // If now visible, fetch and populate settings
    if (settingsDiv.style.display === "block") {
        try {
            const response = await fetch("/read_settings");
            const settings = await response.json();

            for (const [section, values] of Object.entries(settings)) {
                for (const [key, val] of Object.entries(values)) {
                    const inputElement = document.getElementById(`${section}_${key}`);
                    if (inputElement) {
                        inputElement.value = val;
                    } else {
                        console.warn(`⚠️ No input field found for: ${section}_${key}`);
                    }
                }
            }
        } catch (err) {
            console.error("❌ Failed to load settings:", err);
        }
    }
});


document.getElementById("restoreDefaults").addEventListener("click", async function () {
    await fetch("/restore_defaults", { method: "POST" });
    alert("🔄 Defaults restored!");
});

document.getElementById("saveSettings").addEventListener("click", async function () {
    const data = {
        audio: {
            language: document.getElementById("audio_language").value,
            model_size: document.getElementById("audio_model_size").value
        },
        video: {
            frame_interval: parseFloat(document.getElementById("video_frame_interval").value),
            scene_threshold: parseFloat(document.getElementById("video_scene_threshold").value)
        },
        frame: {
            use_clip: document.getElementById("frame_use_clip").checked
        },
        narrative: {
            caption_threshold: parseFloat(document.getElementById("narrative_threshold").value)
        }
    };

    await fetch("/modify_inputs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    document.getElementById("settingsSection").style.display = "none";
});
