export interface RetryOptions {
  maxRetries?: number;
  delay?: number;
  backoffMultiplier?: number;
}

export const handleNetworkErrorWithRetry = async <T>(
  requestFn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> => {
  const { maxRetries = 3, delay = 1000, backoffMultiplier = 2 } = options;

  let lastError: any;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      lastError = error;

      // Don't retry if it's not a network error (e.g., validation error)
      if (attempt === maxRetries) {
        break;
      }

      // Check if it's a network error that should be retried
      const shouldRetry = isRetryableError(error);
      if (!shouldRetry) {
        break;
      }

      // Wait before retrying (exponential backoff)
      if (attempt < maxRetries) {
        const waitTime = delay * Math.pow(backoffMultiplier, attempt);
        await sleep(waitTime);
      }
    }
  }

  throw lastError;
};

const isRetryableError = (error: any): boolean => {
  // Check if it's a network error that can be retried
  if (!error || !error.response) {
    // Likely a network error (request failed to reach server)
    return true;
  }

  const status = error.response?.status;

  // Retry on 5xx server errors and certain 4xx errors
  return (
    // Server errors
    (status >= 500 && status < 600) ||
    // Rate limiting
    status === 429 ||
    // Connection timeout or similar
    status === 408 ||
    // Gateway errors
    status === 502 || status === 503 || status === 504
  );
};

const sleep = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

// Higher-order function to wrap API calls with retry logic
export const withRetry = <T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
) => {
  return () => handleNetworkErrorWithRetry(fn, options);
};