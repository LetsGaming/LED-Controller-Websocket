const SERVER_BASE_URL = ""; // ADD URL of your Server here, or use localhost
const LOCALHOST_BASE_URL = "http://127.0.0.1:5000";

export const fetchJson = async (url: string, options = {}, useLocalhost: boolean): Promise<any> => {
    let request_url = SERVER_BASE_URL + url;
    if(useLocalhost) request_url = LOCALHOST_BASE_URL + url
    const response = await fetch(request_url, options);
    return response.json();
};

