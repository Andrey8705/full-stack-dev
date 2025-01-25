import {jwtDecode} from "jwt-decode";

export const saveTokens = (accessToken: string, refreshToken: string) => {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
  };
  
  export const getAccessToken = (): string | null => {
    return localStorage.getItem("access_token");
  };
  
  export const getRefreshToken = (): string | null => {
    return localStorage.getItem("refresh_token");
  };
  
  export const clearTokens = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };
  
  interface JWTPayload {
    exp: number; // Время истечения токена в формате Unix
  }
  
  // Получение времени истечения из access_token
  export const getTokenExpiration = (accessToken: string): number | null => {
    try {
      const decoded: JWTPayload = jwtDecode(accessToken);
      return decoded.exp * 1000; // Преобразуем в миллисекунды
    } catch (error) {
      console.error("Failed to decode token:", error);
      return null;
    }
  };
  
  // Проверка истечения токена
  export const isTokenExpired = (accessToken: string): boolean => {
    const expirationTime = getTokenExpiration(accessToken);
    if (!expirationTime) return true; // Если токен некорректный
    return Date.now() > expirationTime;
  };
  