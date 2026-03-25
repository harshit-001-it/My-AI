// Initialize Particles.js
particlesJS("particles-js", {
    "particles": {
        "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": "#00d2ff" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5, "random": false },
        "size": { "value": 3, "random": true },
        "line_linked": { "enable": true, "distance": 150, "color": "#00d2ff", "opacity": 0.4, "width": 1 },
        "move": { "enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": { "onhover": { "enable": true, "mode": "repulse" }, "onclick": { "enable": true, "mode": "push" }, "resize": true },
        "modes": { "grab": { "distance": 400, "line_linked": { "opacity": 1 } }, "bubble": { "distance": 400, "size": 40, "duration": 2, "opacity": 8, "speed": 3 }, "repulse": { "distance": 200, "duration": 0.4 }, "push": { "particles_nb": 4 }, "remove": { "particles_nb": 2 } }
    },
    "retina_detect": true
});

// Initialize SiriWave
var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: window.innerWidth,
    height: 150,
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
}

// Start listening visualization
function start_listening() {
    update_status("Listening...");
    siriWave.setAmplitude(1);
    siriWave.start();
}

function stop_listening() {
    update_status("Processing...");
    siriWave.setAmplitude(0);
}

// Click event to start Niva
document.getElementById("arc-reactor").addEventListener("click", () => {
    update_status("Initialising...");
    eel.start_niva();
});

// Optional: Auto-start after a delay
window.onload = () => {
    setTimeout(() => {
        update_status("Click the Arc Reactor to Start");
    }, 2000);
};
