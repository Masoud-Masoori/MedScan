// Camera setup
let stream = null;
const video = document.getElementById('camera-view');

async function setupCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        video.srcObject = stream;
    } catch (err) {
        console.error('Error accessing camera:', err);
        alert('Unable to access camera. Please make sure you have granted camera permissions.');
    }
}

// Initialize camera when page loads
if (video) {
    setupCamera();
}

document.getElementById('capture').onclick = captureImage;

// Capture image and send to backend
async function captureImage() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const imageData = canvas.toDataURL('image/jpeg');

    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        const result = await response.json();
        if (result.success) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `
                <h2>Medication Details</h2>
                <p><strong>Name:</strong> ${result.medication}</p>
                <p><strong>Dosage:</strong> ${result.dosage}</p>
                <p><strong>Frequency:</strong> ${result.frequency}</p>
                <p><strong>Duration:</strong> ${result.duration}</p>
                <button onclick="location.href='reminder.html?pill=${encodeURIComponent(result.medication)}&dosage=${encodeURIComponent(result.dosage)}&frequency=${encodeURIComponent(result.frequency)}'">Set Reminder</button>
            `;
            resultDiv.style.display = 'block';
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process image');
    }
}

// Set reminder from result page
function setReminder() {
    const pill = document.getElementById('medication-name').textContent;
    const dosage = document.getElementById('dosage').textContent;
    const frequency = document.getElementById('frequency').textContent;
    
    // Redirect to reminder page with pre-filled information
    const params = new URLSearchParams({
        pill: pill,
        dosage: dosage,
        frequency: frequency
    });
    
    location.href = `reminder.html?${params.toString()}`;
}

// Show error message
function showError(message) {
    const resultContainer = document.querySelector('.result-container');
    resultContainer.innerHTML = `
        <div class="error-message">
            <h2>⚠️ ${message}</h2>
            <button class="primary-btn" onclick="location.href='scan.html'">
                <span class="icon">📷</span>
                Try Again
            </button>
        </div>
    `;
}

// Load reminder form data from URL parameters
function loadFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const pill = urlParams.get('pill');
    const dosage = urlParams.get('dosage');
    const frequency = urlParams.get('frequency');
    
    if (pill) {
        document.getElementById('pill').value = pill;
    }
    if (dosage) {
        document.getElementById('dosage').value = dosage;
    }
    if (frequency) {
        // Parse frequency and set appropriate checkboxes
        const days = frequency.toLowerCase().split(',');
        const checkboxes = document.querySelectorAll('input[name="days"]');
        checkboxes.forEach(checkbox => {
            if (days.includes(checkbox.value)) {
                checkbox.checked = true;
            }
        });
    }
}

// Initialize reminder form
if (document.getElementById('reminderForm')) {
    loadFromUrl();
}

function retryScan() {
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'none';
}

// Help function
function showHelp() {
    alert('To scan a pill:\n1. Place the pill on a flat surface\n2. Make sure the pill is well-lit\n3. Hold your camera steady\n4. Press "Take Photo" when ready\n\nIf you need more help, please call your caregiver.');
}

// Clean up camera when leaving page
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
