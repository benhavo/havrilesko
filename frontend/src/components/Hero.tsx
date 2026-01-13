import { useEffect, useState } from "react";

const words = [
  "software engineer",
  "builder",
  "problem solver",
  "math nerd",
  "systems designer",
  "full-stack developer",
  "musician",
  "lifelong learner",
  "Linux enthusiast",
];

export default function Hero() {
  const [wordIndex, setWordIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [displayText, setDisplayText] = useState("");

  useEffect(() => {
    const currentWord = words[wordIndex];
    let timeout: number;

    if (!isDeleting) {
      timeout = window.setTimeout(() => {
        const next = currentWord.slice(0, charIndex + 1);
        setDisplayText(next);
        setCharIndex((prev) => prev + 1);

        if (next.length === currentWord.length) {
          setTimeout(() => setIsDeleting(true), 1400);
        }
      }, 75);
    } else {
      timeout = window.setTimeout(() => {
        const next = currentWord.slice(0, charIndex - 1);
        setDisplayText(next);
        setCharIndex((prev) => prev - 1);

        if (next.length === 0) {
          setIsDeleting(false);
          setWordIndex((prev) => (prev + 1) % words.length);
        }
      }, 45);
    }

    return () => clearTimeout(timeout);
  }, [charIndex, isDeleting, wordIndex]);

  return (
    <section className="my-10">
      <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
        Hi, my name is Ben. I'm a{" "}
        <span className="text-blue-500">{displayText}</span>
        <span className="ml-1 animate-pulse">|</span>
      </h1>
    </section>
  );
}
