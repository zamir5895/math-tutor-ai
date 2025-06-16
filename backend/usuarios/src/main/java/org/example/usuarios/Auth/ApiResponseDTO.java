package org.example.usuarios.Auth;

public class ApiResponseDTO {
    private String mensaje;
    private Object data;
    private int totalRegistrados;

    public ApiResponseDTO(String mensaje) {
        this.mensaje = mensaje;
    }

    public ApiResponseDTO(String mensaje, Object data) {
        this.mensaje = mensaje;
        this.data = data;
    }

    public ApiResponseDTO(String mensaje, int totalRegistrados) {
        this.mensaje = mensaje;
        this.totalRegistrados = totalRegistrados;
    }

    public String getMensaje() { return mensaje; }
    public void setMensaje(String mensaje) { this.mensaje = mensaje; }
    public Object getData() { return data; }
    public void setData(Object data) { this.data = data; }
    public int getTotalRegistrados() { return totalRegistrados; }
    public void setTotalRegistrados(int totalRegistrados) { this.totalRegistrados = totalRegistrados; }
}