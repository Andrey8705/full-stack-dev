import { getAccessToken, getRefreshToken, isTokenExpired, saveTokens, clearTokens,  } from "./Service";

const API_BASE_URL = "http://localhost:8000/api";

export const authFetch = async (input: RequestInfo, init?: RequestInit): Promise<Response> => {
  let accessToken = getAccessToken();
  const refreshToken = getRefreshToken();

  // Проверяем, истек ли access_token
  if (accessToken && isTokenExpired(accessToken)) {
    console.log("Access token expired. Attempting to refresh...");

    try {
      // Запрос к /refresh-token
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        accessToken = data.access_token;
        

        // Сохраняем новый токен
        if (refreshToken !== null)
          saveTokens(data.access_token, refreshToken);
          console.log("Access token refreshed.");
        } else {
          console.error("Failed to refresh token:", response.statusText);
          clearTokens(); // Удаляем токены
          throw new Error("Unable to refresh access token. Please login again.");
        }
    } catch (error) {
      console.error("Error refreshing token:", error);
      clearTokens();
      throw error; // Перебрасываем ошибку для обработки в UI
    }
  }

  // Добавляем access_token в заголовок Authorization
  const authHeaders: HeadersInit = accessToken ? { Authorization: `Bearer ${accessToken}` } : {};

  return fetch(input, {
    ...init,
    headers: {
      ...init?.headers,
      ...authHeaders,
    },
  });
};
