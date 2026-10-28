# GSAP & Motion Animation Patterns

> Canonical implementation skeletons, hardware acceleration rules, and strictly forbidden animation anti-patterns.

---

## 1. Canonical Implementation Skeletons

### 1.A Sticky-Stack Pattern (Scroll-Pinned Card Stacking)

A true sticky-stack pins cards at the top of the viewport and shrinks previous cards as new ones arrive:

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",           // Pin precisely at top of viewport
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

---

### 1.B Horizontal-Pan Pattern (Vertical Scroll to Horizontal Slide)

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",
          end: () => `+=${distance}`,
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

---

### 1.C Scroll-Reveal Stagger (Lightweight Motion Alternative)

For simple reveal animations without pinned layouts, prefer Motion's `whileInView`:

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

---

### 1.D Modern `@gsap/react` Hook (`useGSAP`)

> [!NOTE]
> All GSAP bonus plugins (`SplitText`, `ScrollSmoother`, `Flip`, `MorphSVG`) are **100% free** for commercial use. When using React 18/19 or Next.js, always use `@gsap/react` (`useGSAP()`) instead of raw `useEffect` to guarantee automated lifecycle teardown and StrictMode immunity.

```tsx
"use client";
import { useRef } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(useGSAP, ScrollTrigger, SplitText);

export function EditorialHero({ title }: { title: string }) {
  const container = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      // Split text by lines and characters with overflow-hidden mask
      const split = new SplitText(".hero-headline", { type: "lines,chars", linesClass: "overflow-hidden" });
      
      gsap.from(split.chars, {
        yPercent: 120,
        opacity: 0,
        stagger: 0.02,
        duration: 1.1,
        ease: "power4.out",
        delay: 0.15,
      });
    },
    { scope: container }
  );

  return (
    <div ref={container} className="relative py-24">
      <h1 className="hero-headline text-6xl md:text-8xl font-black tracking-tight leading-none">
        {title}
      </h1>
    </div>
  );
}
```

---

### 1.E `ScrollSmoother` Luxury Page Scroller

```tsx
"use client";
import { useRef } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ScrollSmoother } from "gsap/ScrollSmoother";

gsap.registerPlugin(useGSAP, ScrollTrigger, ScrollSmoother);

export function SmoothWrapper({ children }: { children: React.ReactNode }) {
  useGSAP(() => {
    ScrollSmoother.create({
      smooth: 1.2,               // Seconds to "catch up" to actual scroll position
      effects: true,             // Look for data-speed and data-lag attributes
      smoothTouch: 0.1,          // Light touch smoothing
    });
  });

  return (
    <div id="smooth-wrapper">
      <div id="smooth-content">
        {children}
      </div>
    </div>
  );
}
```

---

## 2. Forbidden Animation Anti-Patterns

1. **`window.addEventListener("scroll", ...)` is STRICTLY BANNED**: It runs on every scroll frame unbatched, causing severe frame drops. Use `ScrollTrigger`, `useScroll()`, or CSS `animation-timeline`.
2. **`window.scrollY` in React Component State**: Never call `setScrollY(window.scrollY)` in React state. It triggers full component tree re-renders 60+ times per second.
3. **`requestAnimationFrame` updating React State**: Use Motion's `useMotionValue` and `useTransform` outside React's render loop.
4. **Animating Layout Geometry (`top`, `left`, `width`, `height`)**: Animate **only** `transform` and `opacity` to preserve GPU hardware acceleration.
5. **Ignoring `prefers-reduced-motion`**: Any animation above `MOTION_INTENSITY > 3` must wrap in `useReducedMotion()` or `@media (prefers-reduced-motion: reduce)` and gracefully collapse to static.
6. **More Than 1 Marquee per Page**: Multiple horizontal auto-scrolling marquees read as cheap visual filler. Cap at 1 marquee per page maximum.
