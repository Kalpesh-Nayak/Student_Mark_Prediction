
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("prediction-form");
    const result = document.getElementById("result");
    const submitButton = form?.querySelector('button[type="submit"]');

    if (!form || !result || !submitButton) {
        console.error("Prediction form elements were not found.");
        return;
    }

    form.addEventListener("submit", () => {
        // Clear the previous result before submitting.
        result.replaceChildren();

        // Show a loading state while the server processes the form.
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";
    });
});
