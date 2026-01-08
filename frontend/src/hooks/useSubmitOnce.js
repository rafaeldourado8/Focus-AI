import { useState, useCallback } from 'react';

export const useSubmitOnce = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const withSubmit = useCallback(async (fn) => {
    if (isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      await fn();
    } finally {
      setIsSubmitting(false);
    }
  }, [isSubmitting]);

  return { isSubmitting, withSubmit };
};
