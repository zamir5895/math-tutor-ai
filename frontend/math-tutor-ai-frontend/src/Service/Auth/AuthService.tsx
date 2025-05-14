import type { LoginRequest } from "../../Types/Auth/LoginType";
import { axiosAuthInstance } from "../AxiosConfig";

export const login = async (data:LoginRequest)=>{
    try{
        const response = await axiosAuthInstance.post("/login", data)
        console.log("la data que viene ", response)
        return response.data;
    }catch(error){
        return error;
    }
}
