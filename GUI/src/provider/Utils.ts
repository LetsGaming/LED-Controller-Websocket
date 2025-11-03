import config from "../../config.json";

const SERVER_BASE_URL = config.server.baseUrl || "";
const SERVER_PORT = config.server.port || "";

const LOCALHOST_BASE_URL = "http://localhost";
const API_PORT = ":5000";

export const fetchJson = async (url: string, options = {}, useLocalhost = false) => {
    let SERVER_URL;
    if(useLocalhost) {
        SERVER_URL = LOCALHOST_BASE_URL + API_PORT;
    } else {
        SERVER_URL = SERVER_BASE_URL + (SERVER_PORT ? `:${SERVER_PORT}` : "");
    }
    
    const requestUrl = `${SERVER_URL}${url}`;

    const response = await fetch(requestUrl, options);
    return response.json();
};