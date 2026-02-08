import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

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

type Phase = "waiting" | "typing" | "pausing" | "deleting" | "done";

const finalWord = "software engineer.";

export default function Hero() {
  const [showGreeting, setShowGreeting] = useState(false);
  const [showIntro, setShowIntro] = useState(false);
  const [wordIndex, setWordIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [phase, setPhase] = useState<Phase>("waiting");
  const [cycleComplete, setCycleComplete] = useState(false);

  // Staggered fade-in effect
  useEffect(() => {
    const greetingTimeout = setTimeout(() => setShowGreeting(true), 300);
    const introTimeout = setTimeout(() => setShowIntro(true), 1000);
    const typingTimeout = setTimeout(() => setPhase("typing"), 1700);

    return () => {
      clearTimeout(greetingTimeout);
      clearTimeout(introTimeout);
      clearTimeout(typingTimeout);
    };
  }, []);

  // Typing effect
  useEffect(() => {
    if (phase === "waiting" || phase === "done") return;

    const currentWord = cycleComplete ? finalWord : words[wordIndex];

    const timeout = window.setTimeout(
      () => {
        switch (phase) {
          case "typing":
            if (displayText.length < currentWord.length) {
              setDisplayText(currentWord.slice(0, displayText.length + 1));
            } else if (cycleComplete) {
              setPhase("done");
            } else {
              setPhase("pausing");
            }
            break;
          case "pausing":
            setPhase("deleting");
            break;
          case "deleting":
            if (displayText.length > 0) {
              setDisplayText(displayText.slice(0, -1));
            } else {
              const nextIndex = (wordIndex + 1) % words.length;
              if (nextIndex === 0) {
                setCycleComplete(true);
              }
              setWordIndex(nextIndex);
              setPhase("typing");
            }
            break;
        }
      },
      phase === "typing" ? 75 : phase === "pausing" ? 1400 : 45
    );

    return () => clearTimeout(timeout);
  }, [displayText, phase, wordIndex, cycleComplete]);

  return (
    <section className="my-10">
      <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
        <p
          className={cn(
            "transition-opacity duration-700",
            showGreeting ? "opacity-100" : "opacity-0"
          )}
        >
          Hi, my name is Ben.
        </p>
        <p
          className={cn(
            "mt-4 transition-opacity duration-700",
            showIntro ? "opacity-100" : "opacity-0"
          )}
        >
          I'm a <span className="text-blue-500">{displayText}</span>
          <span className="ml-1 animate-pulse">|</span>
        </p>
      </h1>
    </section>
  );
}
