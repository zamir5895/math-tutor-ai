import axios from "axios";

export const axiosAuthInstance  = axios.create({
    baseURL:"http://localhost:8080/api/auth",
});