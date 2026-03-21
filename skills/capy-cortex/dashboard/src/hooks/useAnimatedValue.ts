import { useEffect, useRef, useState } from 'react';

export function useAnimatedValue(target: number, duration = 800): number {
  const [value, setValue] = useState(0);
  const startRef = useRef(0);
  const startTimeRef = useRef(0);
  const rafRef = useRef(0);

  useEffect(() => {
    startRef.current = value;
    startTimeRef.current = performance.now();

    const animate = (now: number) => {
      const elapsed = now - startTimeRef.current;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const current = startRef.current + (target - startRef.current) * eased;
      setValue(Math.round(current));
      if (progress < 1) rafRef.current = requestAnimationFrame(animate);
    };

    rafRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafRef.current);
  }, [target, duration]);

  return value;
}
