async function checkApi() {
    const status = document.querySelector("#api-status");

    try {
        const response = await fetch("/api/v1/health/ready");

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        status.textContent = "ONLINE";
    } catch {
        status.textContent = "OFFLINE";
    }
}

checkApi();