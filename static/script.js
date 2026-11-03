
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

    // After the server responds and the page reloads,
    // automatically scroll to the prediction result.
    if (result.children.length > 0) {
        setTimeout(() => {
            result.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }, 300);
    }
});
