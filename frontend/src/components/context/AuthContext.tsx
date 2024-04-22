export const isAuthenticated = () => {
    const accessToken = localStorage.getItem('access_token');
    const tokenType = localStorage.getItem('token_type');
    return accessToken && tokenType;
};