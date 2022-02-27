import React from "react";
import ReactAnime from "react-animejs";
import { StaticImage } from "gatsby-plugin-image";

const { Anime, stagger } = ReactAnime;

const Map = () => {
  return (
    <Anime
      className="w-full lg:w-3/5 my-10"
      animeConfig={{
        autoplay: true,
        loop: true,
      }}
      initial={[
        {
          targets: "#line-0",
          duration: 5000,
          easing: "linear",
          delay: stagger(1500),
          strokeDashoffset: [1000, 0],
        },
        {
          targets: "#line-1",
          duration: 5000,
          easing: "linear",
          delay: stagger(1500),
          strokeDashoffset: [1000, 0],
        },
        {
          targets: "#line-2",
          duration: 5000,
          easing: "linear",
          delay: stagger(1500),
          strokeDashoffset: [1000, 0],
        },
        {
          targets: "#line-0",
          duration: 5000,
          easing: "linear",
          strokeDashoffset: [0, -1000],
        },
        {
          targets: "#line-1",
          duration: 5000,
          easing: "linear",
          strokeDashoffset: [0, -1000],
        },
        {
          targets: "#line-2",
          duration: 5000,
          easing: "linear",
          strokeDashoffset: [0, -1000],
          endDelay: 3000,
        },
      ]}
    >
      <div className="mx-auto my-10 relative">
        <StaticImage
          className="block"
          src="../../images/world-map.png"
          placeholder="none"
        />
        <svg
          className="absolute top-0 bottom-0 h-full w-full"
          viewBox="0 0 1600 840"
        >
          <path
            id="line-0"
            d="M220 150 Q675 70 1130 150"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="1130" cy="150" r="8" fill="#FFD700" />
          <path
            id="line-1"
            d="M1130 150 Q815 150 500 520"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="500" cy="520" r="8" fill="#FFD700" />
          <path
            id="line-1"
            d="M1130 150 Q1260 130 1300 340"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="1300" cy="340" r="8" fill="#FFD700" />
          <path
            id="line-0"
            d="M220 150 Q452 150 700 430"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <path
            id="line-1"
            d="M700 430 Q1000 300 1500 640"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="1500" cy="640" r="8" fill="#FFD700" />
          <circle cx="700" cy="430" r="8" fill="#FFD700" />
          <path
            id="line-1"
            d="M700 430 Q430 130 180 320"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="180" cy="320" r="8" fill="#FFD700" />
          <path
            id="line-2"
            d="M500 520 Q690 430 880 680"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="880" cy="680" r="8" fill="#FFD700" />
          <path
            id="line-2"
            d="M1500 640 Q1600 355 1500 90"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="1500" cy="90" r="8" fill="#FFD700" />
          <path
            id="line-2"
            d="M220 150 Q360 200 500 520"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <path
            id="line-2"
            d="M1500 90 Q1315 60 1130 150"
            fill="none"
            stroke="#FFD700"
            strokeWidth="5"
            strokeLinecap="round"
            strokeDashoffset="0"
            strokeDasharray="1000"
          />
          <circle cx="220" cy="150" r="8" fill="red" />
        </svg>
      </div>
    </Anime>
  );
};

export default Map;
