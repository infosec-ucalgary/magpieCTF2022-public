import React, { useState } from "react";
import ReactAnime from "react-animejs";

import Logo from "./logo";

const { Anime, stagger } = ReactAnime;

const SplashScreen = () => {
  const [meta, setMeta] = useState({
    progress: 0,
    currentTime: 0,
    duration: 0,
  });

  return (
    <Anime
      setMeta={setMeta}
      animeConfig={{
        autoplay: true,
        loop: false,
        duration: 800,
        easing: "easeOutExpo",
      }}
      initial={[
        {
          duration: 400,
        },
        {
          targets: "#splash-flag",
          opacity: [0, 1],
          scale: [0.75, 1],
          duration: 2000,
          endDelay: 100,
          easing: "easeOutElastic",
        },
        {
          targets: "#splash-name div",
          opacity: [0, 1],
          translateX: [-25, 0],
          rotate: [-15, 0],
          delay: stagger(90),
          color: "#FFD700",
          endDelay: 0,
        },
        {
          targets: "#splash-inc",
          opacity: [0, 1],
          translateX: [-10, 0],
          endDelay: 0,
        },
        {
          targets: "#splash-tagline",
          opacity: [0, 1],
          translateY: [-25, 0],
          offset: "-=400",
          endDelay: 2000,
        },
        {
          targets: "#splash-logo",
          opacity: [1, 0],
          duration: 1000,
          scale: [1, 0.95],
          endDelay: 0,
        },
        {
          targets: "#splash-background",
          opacity: [1, 0],
          duration: 5000,
        },
      ]}
    >
      <div
        id="splash-background"
        className="absolute flex justify-center items-center w-full h-screen min-h-full text-white font-bold z-50 select-none"
        style={{
          pointerEvents: meta.progress <= 60 ? "auto" : "none",
        }}
      >
        <div
          id="splash-logo"
          className="flex flex-col items-center pointer-events-none overflow-hidden	"
        >
          <div className="flex flex-row items-center text-3xl sm:text-6xl">
            <div id="splash-name" className="flex flex-row">
              <div className="opacity-0">O</div>
              <div className="opacity-0">M</div>
              <div className="opacity-0">N</div>
            </div>
            <Logo />
            <div id="splash-name" className="flex flex-row">
              <div className="opacity-0">-</div>
              <div className="opacity-0">F</div>
              <div className="opacity-0">L</div>
              <div className="opacity-0">A</div>
              <div className="opacity-0">G</div>
              <div className="opacity-0">S</div>
            </div>
          </div>
          <div
            id="splash-inc"
            className="absolute ml-28 sm:ml-52 mt-12 sm:mt-24 text:xl sm:text-3xl opacity-0"
          >
            INC.
          </div>
          <div
            id="splash-tagline"
            className="text-2xl sm:text-4xl mt-6 opacity-0"
          >
            A Family Company
          </div>
        </div>
      </div>
    </Anime>
  );
};
export default SplashScreen;
