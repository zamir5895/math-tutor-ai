import axios, { AxiosError, type AxiosInstance } from "axios";
import type { User, UserLogin, UserRegister } from "./types";

export class AuthService {
  private readonly axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: "http://localhost:8000/",
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  public async login(data: UserLogin): Promise<User | AxiosError> {
    try {
      console.log("Iniciando sesión con los datos:", data);
      const response = await this.axiosInstance.post<User>("usuarios/login", data);
      console.log("La data que viene", response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Error en la petición:", error.message);
        return error;
      }
      throw error; 
    }
  }
  public async signup(data: UserRegister): Promise<User | AxiosError> {
    try {
      const response = await this.axiosInstance.post<User>("usuarios/registrar", data);
      console.log("La data que viene", response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Error en la petición:", error.message);
        return error;
      }
      throw error; 
    }
  }
  

}
export const authService = new AuthService();