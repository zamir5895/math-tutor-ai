export type User = {
    id: string;
    nombre: string;
    username: string;
    fecha_registro: string;
};

export type UserLogin = {
    username: string;
    password: string;
}

export type UserRegister = {
    nombre: string;
    username: string;
    password: string;
};