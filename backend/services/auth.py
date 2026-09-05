from supaInit.supabaseInit import supabaseClient


def get_current_user(access_token: str) -> str:
    """
    Validates the JWT access_token by calling Supabase get_user().
    Returns the authenticated user's UUID (str) on success.
    Raises ValueError if the token is missing, invalid, or expired.
    """
    if not access_token:
        raise ValueError("No access token provided.")

    try:
        response = supabaseClient.auth.get_user(access_token)
    except Exception as e:
        raise ValueError(f"Token validation failed: {str(e)}")

    user = response.user if response else None
    if not user or not user.id:
        raise ValueError("Invalid or expired token.")

    return str(user.id)   # UUID of the authenticated user


def login(email: str, password: str):

    try:
        response = supabaseClient.auth.sign_in_with_password({
            "email": email,
            "password": password,
            # "options": {
            #     "email_redirect_to": "http://localhost:4200/dashboard"
            # }
        })
        return response
    except Exception as e:
        raise ValueError(f"Authentication failed: {str(e)}")


def signup(email: str, password: str):
    try:
        response = supabaseClient.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "email_redirect_to": "http://localhost:4200/login"
            }
        })
        return response
    except Exception as e:
        raise ValueError(f"Signup failed: {str(e)}")