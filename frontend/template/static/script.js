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
    read_settings();
	
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

async function saveSettings() {
    const audioModel = document.getElementById("audio_model_box")?.value || "";
	const audioModelSize = document.getElementById("audio_model_size")?.value || null;
    const videoIntervalSec = document.getElementById("interval_sec")?.value || null;
	const videoStability = document.getElementById("scene_stability_sec")?.value || null;
	const videoThreshold = document.getElementById("video_diff_threshold")?.value || null;
    const frameCLIPSetting = document.getElementById("clip_model_id")?.value || null;
	const frameBLIPSetting = document.getElementById("blip_model_id")?.value || null;
    const narrativeConfidence = document.getElementById("frame_confidence")?.value || null;
	const narrativeModelID = document.getElementById("narrative_model_id")?.value || null;
	const narrativeFPS = document.getElementById("video_fps")?.value || null;
	const summaryMode = document.getElementById("video_summary_mode")?.value || null;

    const settings = {
        audio: { audio_model: audioModel, model_size:  audioModelSize},
        video: { interval_sec: videoIntervalSec, scene_stability_sec: videoStability, diff_threshold: videoThreshold},
        frame: { clip_model_id: frameCLIPSetting, blip_model_id: frameBLIPSetting },
        narrative: { confidence: narrativeConfidence, model_id: narrativeModelID, fps: narrativeFPS, summary_mode: summaryMode}
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

    // Optionally hide settings section
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

        if (result.status === "success") {
            const settings = result.settings;

            // Fill Audio settings
			document.getElementById("audio_model_box").value = settings.audio?.audio_model || "";;
			document.getElementById("audio_model_size").value = settings.audio?.model_size || "";
			
            // Fill Video settings
            document.getElementById("video_interval_sec").value = settings.video?.interval_sec || "";
			document.getElementById("video_scene_stability_sec").value = settings.video?.scene_stability_sec || "";
			document.getElementById("video_diff_threshold").value = settings.video?.diff_threshold || "";
          
            // Fill Frame settings
            document.getElementById("frame_clip_model_id").value = settings.frame?.clip_model_id || "";
			document.getElementById("frame_blip_model_id").value = settings.frame?.blip_model_id || "";
           
            // Fill Narrative settings
            document.getElementById("narrative_confidence").value = settings.narrative?.confidence || "";
			document.getElementById("narrative_model_id").value = settings.narrative?.model_id || "";
			document.getElementById("video_fps").value = settings.narrative?.fps || "";
			document.getElementById("video_summary_mode").value  = settings.narrative?.summary_mode || "";
   
        } else {
            console.error("Failed to load settings:", result);
        }
    } catch (err) {
        console.error("Error fetching settings:", err);
    }
}

document.addEventListener("DOMContentLoaded", read_settings);

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