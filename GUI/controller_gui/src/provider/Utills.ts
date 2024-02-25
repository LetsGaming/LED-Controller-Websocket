const SERVER_BASE_URL = ""; // ADD URL of your Server here, or use localhost

const LOCALHOST_BASE_URL = "http://localhost";
const API_PORT = ":5000";

export const fetchJson = async (url: string, options = {}, useLocalhost: boolean = false): Promise<any> => {
    const baseUrl = useLocalhost ? LOCALHOST_BASE_URL + API_PORT : SERVER_BASE_URL;
    const requestUrl = `${baseUrl}${url}`;

    const response = await fetch(requestUrl, options);
    return response.json();
};
