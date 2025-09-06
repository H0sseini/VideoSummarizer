document.getElementById("summarizeForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = this.querySelector("input[type='file']");
    const file = fileInput.files[0];
	const summarizeButton = document.getElementById("submitting");
	const toggleSettingsButton = document.getElementById("toggleSettings");
	const fullButton = document.getElementById("copyFullBtn");
	const summaryButton = document.getElementById("copySumBtn");
    if (!file) return;

    document.getElementById("fullNarrative").value = "⏳ Summarizing, please wait...";
    document.getElementById("summaryTextArea").value = "⏳ Summarizing, please wait...";
	

    const formData = new FormData();
    formData.append("file", file);

    
	summarizeButton.disabled = true;
	toggleSettingsButton.disabled = true;
	summarizeButton.style.backgroundColor = "gray";
	toggleSettingsButton.style.backgroundColor = "gray";
	fullButton.disabled = true;
	summaryButton.disabled = true;
	fullButton.style.backgroundColor = "gray";
	summaryButton.style.backgroundColor = "gray";

	try {
		const response = await fetch("/summarize", {
			method: "POST",
			body: formData,
		});
	
		const result = await response.json();
	
		if (result.status === "success") {
			document.getElementById("summaryTextArea").value = result.summary_text;
			document.getElementById("fullNarrative").value = result.fullNarrative;
		} else {
			document.getElementById("summaryTextArea").value = "⚠️ An error occurred.";
			document.getElementById("fullNarrative").value = result.message + "\n\n" + result.traceback;
		}
	
	} catch (err) {
		document.getElementById("summaryTextArea").value = "⚠️ An error occurred.";
		document.getElementById("fullNarrative").value = err.message;
	} finally {
		summarizeButton.disabled = false;
		toggleSettingsButton.disabled = false;
		summarizeButton.style.backgroundColor = "rgb(0, 123, 255)";
		toggleSettingsButton.style.backgroundColor = "rgb(0, 123, 255)";
		fullButton.disabled = false;
		summaryButton.disabled = false;
		fullButton.style.backgroundColor = "rgb(0, 123, 255)";
		summaryButton.style.backgroundColor = "rgb(0, 123, 255)";
		
	}
	
});

document.getElementById("toggleSettings").addEventListener("click", async function () {
    const settingsDiv = document.getElementById("settingsSection");
    // Toggle visibility
    settingsDiv.style.display = settingsDiv.style.display === "none" ? "block" : "none";
    // If now visible, load and populate
    if (settingsDiv.style.display === "block") {
        await read_settings();
    }
});


document.getElementById("restoreDefaults").addEventListener("click", async function () {
    await fetch("/restore_defaults", { method: "POST" });
    
});



async function saveSettings() {
    const audioModel = document.getElementById("audio_model_box")?.value || null;
    const audioModelSize = document.getElementById("audio_model_size")?.value || null;

    const videoIntervalSec = document.getElementById("video_interval_sec")?.value || null;
    const videoStability = document.getElementById("video_scene_stability_sec")?.value || null;
    const videoThreshold = document.getElementById("video_diff_threshold")?.value || null;

    const frameCLIPSetting = document.getElementById("frame_clip_model_id")?.value || null;
    const frameBLIPSetting = document.getElementById("frame_blip_model_id")?.value || null;

    const narrativeConfidence = document.getElementById("narrative_confidence")?.value || null;
    const narrativeModelID = document.getElementById("narrative_model_id")?.value || null;
    const narrativeFPS = document.getElementById("video_fps")?.value || null;
    const summaryMode = document.getElementById("video_summary_mode")?.value || null;

    const settings = {
        audio: { audio_model: audioModel, model_size: audioModelSize },
        video: { interval_sec: videoIntervalSec, scene_stability_sec: videoStability, diff_threshold: videoThreshold },
        frame: { clip_model_id: frameCLIPSetting, blip_model_id: frameBLIPSetting },
        narrative: { confidence: narrativeConfidence, model_id: narrativeModelID, fps: narrativeFPS, summary_mode: summaryMode }
    };

    try {
        const response = await fetch("/write_inputs", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(settings),
        });

        const result = await response.json();
        if (result.status === "success") {
            alert("✅ Settings saved successfully!");
        } else {
            alert("⚠️ Failed to save settings: " + result.message);
        }
    } catch (err) {
        alert("❌ Error: " + err.message);
    }
	read_settings();
    document.getElementById("settingsSection").style.display = "none";
}

document.getElementById("restoreDefaults").addEventListener("click", async () => {
    if (!confirm("Are you sure you want to restore default settings? This will overwrite current settings.")) {
        return;
    }

    try {
        // Disable button while processing
        const btn = document.getElementById("restoreDefaults");
        btn.disabled = true;
		btn.style.backgroundColor = "gray";
        btn.innerText = "Restoring...";

        const response = await fetch("/restore_defaults", {
            method: "POST"
        });

        const result = await response.json();

        if (result.status === "success") {
            alert("✅ Defaults restored successfully!");
            // Optionally reload settings on frontend
            read_settings();
        } else {
            alert("⚠️ Error restoring defaults:\n" + result.message);
        }
    } catch (err) {
        alert("⚠️ Request failed:\n" + err.message);
    } finally {
        const btn = document.getElementById("restoreDefaults");
        btn.disabled = false;
		btn.style.backgroundColor = "rgb(0, 123, 255)";
        btn.innerText = "Restore Defaults";
		document.getElementById("settingsSection").style.display = "none";
    }
});

async function read_settings() {
    try {
        const response = await fetch("/read_settings");
        const result = await response.json();

        if (result.error) {
            console.error("⚠️ Failed to load settings:", result.error);
            return; // Optionally clear fields or handle UI feedback here
        } else {
            const MySettings = result; // Directly use result as settings

            // Fill Audio
            document.getElementById("audio_model_box").value = MySettings.audio?.audio_model || "";
            document.getElementById("audio_model_size").value = MySettings.audio?.model_size || "";

            // Fill Video
            document.getElementById("video_interval_sec").value = MySettings.video?.interval_sec || "";
            document.getElementById("video_scene_stability_sec").value = MySettings.video?.scene_stability_sec || "";
            document.getElementById("video_diff_threshold").value = MySettings.video?.diff_threshold || "";

            // Fill Frame
            document.getElementById("frame_clip_model_id").value = MySettings.frame?.clip_model_id || "";
            document.getElementById("frame_blip_model_id").value = MySettings.frame?.blip_model_id || "";

            // Fill Narrative
            document.getElementById("narrative_confidence").value = MySettings.narrative?.confidence || "";
            document.getElementById("narrative_model_id").value = MySettings.narrative?.model_id || "";
            document.getElementById("video_fps").value = MySettings.narrative?.fps || "";
            document.getElementById("video_summary_mode").value = MySettings.narrative?.summary_mode || "";
        }
    } catch (err) {
        console.error("❌ Error fetching settings:", err);
    }
}


document.getElementById("copyFullBtn").addEventListener('click', function() {
                navigator.clipboard.writeText(document.getElementById("fullNarrative").value).then(function() {
                    document.getElementById("copyFullBtn").textContent = "✅ Copied!";
                    setTimeout(function() {
                        document.getElementById("copyFullBtn").textContent = "Copy to Clipboard";
                    }, 2000);
                }).catch(function(err) {
                    alert("Failed to copy: " + err);
                });
 });
 
 document.getElementById("copySumBtn").addEventListener('click', function() {
                navigator.clipboard.writeText(document.getElementById("summaryTextArea").value).then(function() {
                    document.getElementById("copySumBtn").textContent = "✅ Copied!";
                    setTimeout(function() {
                        document.getElementById("copySumBtn").textContent = "Copy to Clipboard";
                    }, 2000);
                }).catch(function(err) {
                    alert("Failed to copy: " + err);
                });
 });