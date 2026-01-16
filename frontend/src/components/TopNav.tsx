import { useState } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faX } from "@fortawesome/free-solid-svg-icons";
import { cn } from "@/lib/utils";

interface NavItem {
  path: string;
  label: string;
}

interface TopNavProps {
  items: NavItem[];
}

export default function TopNav({ items }: TopNavProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="flex items-center justify-end gap-2 p-4">
      <div
        className={cn(
          "flex items-center gap-2 overflow-hidden transition-all duration-300 ease-in-out",
          isOpen ? "max-w-[500px] opacity-100" : "max-w-0 opacity-0"
        )}
      >
        {items.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-full px-4 py-2 text-sm font-medium whitespace-nowrap shadow-md transition-colors"
            onClick={() => setIsOpen(false)}
          >
            {item.label}
          </Link>
        ))}
      </div>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-primary text-primary-foreground flex h-12 w-12 items-center justify-center rounded-full shadow-lg transition-transform hover:scale-105"
        aria-label={isOpen ? "Close menu" : "Open menu"}
      >
        <FontAwesomeIcon icon={isOpen ? faX : faBars} className="h-5 w-5" />
      </button>
    </nav>
  );
}
