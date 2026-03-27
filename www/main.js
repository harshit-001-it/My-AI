// Initialize SiriWave
var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 500,
    height: 100,
    style: "ios9",
    amplitude: 0,
    speed: 0.2,
    color: "#00d2ff"
});

// Function to update UI from Python
eel.expose(update_status);
function update_status(text) {
    document.getElementById("status").innerText = text;
}

eel.expose(set_amplitude);
function set_amplitude(val) {
    siriWave.setAmplitude(val);
    
    // Heartbeat Pulse Logic
    // Scale heart based on amplitude (1.0 to 1.5 range)
    const scale = 1.0 + (val * 0.5);
    document.documentElement.style.setProperty('--pulse-scale', scale);
}

// Click event to start Niva
document.getElementById("niva-heart-trigger").addEventListener("click", () => {
    update_status("AUTHENTICATING...");
    eel.start_niva();
});

// Optional: Auto-start after a delay
window.onload = () => {
    setTimeout(() => {
        update_status("READY FOR COMMAND");
    }, 1500);
};
