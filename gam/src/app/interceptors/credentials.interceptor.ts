import { HttpInterceptorFn } from '@angular/common/http';

/**
 * Automatically attaches `withCredentials: true` to every outgoing HTTP request
 * so that the HttpOnly `access_token` cookie is sent to the backend.
 */
export const credentialsInterceptor: HttpInterceptorFn = (req, next) => {
  const cloned = req.clone({ withCredentials: true });
  return next(cloned);
};
