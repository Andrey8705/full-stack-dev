import {
  getAccessToken,
  getRefreshToken,
  isTokenExpired,
  saveTokens,
  clearTokens,
} from "./Service";

export const API_BASE_URL = "http://localhost:8000/api/";

export const authFetch = async (
  input: RequestInfo,
  init?: RequestInit
): Promise<Response> => {
  let accessToken = getAccessToken();
  const refreshToken = getRefreshToken();

  // Проверка срока действия токена
  if (accessToken && isTokenExpired(accessToken)) {
    console.log("Access token expired. Attempting to refresh...");

    const success = await tryRefreshToken(refreshToken);
    if (success) {
      accessToken = getAccessToken(); // обновлённый
    } else {
      throw new Error("Unable to refresh token");
    }
  }

  // Выполняем первый запрос
  let response = await fetch(input, {
    ...init,
    headers: {
      ...init?.headers,
      Authorization: `Bearer ${accessToken}`,
    },
  });

  // Если получаем 401, пробуем обновить и повторить
  if (response.status === 401 && refreshToken) {
    console.warn("Received 401. Trying to refresh and retry...");

    const success = await tryRefreshToken(refreshToken);
    if (success) {
      const retryAccessToken = getAccessToken();
      response = await fetch(input, {
        ...init,
        headers: {
          ...init?.headers,
          Authorization: `Bearer ${retryAccessToken}`,
        },
      });
    } else {
      console.error("Refresh token failed. Logging out...");
      clearTokens();
    }
  }

  return response;
};

// Вспомогательная функция для обновления токена
const tryRefreshToken = async (refreshToken: string | null): Promise<boolean> => {
  if (!refreshToken) return false;

  try {
    const response = await fetch(`${API_BASE_URL}auth/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) return false;

    const data = await response.json();
    saveTokens(data.access_token, data.refresh_token);
    console.log("Token refreshed successfully");
    return true;
  } catch (error) {
    console.error("Error refreshing token:", error);
    return false;
  }
};
