import React from "react";
import ReactAnime from "react-animejs";

const { Anime, stagger } = ReactAnime;

const LetterWall = () => {
  return (
    <Anime
      animeConfig={{
        targets: ".letter",
        delay: stagger(100, {
          grid: [10, 15],
          from: "first",
        }),
        autoplay: true,
        loop: true,
        duration: 1500,
        endDelay: 2000,
        easing: "easeOutExpo",
      }}
      initial={[
        {
          letterSpacing: "25px",
          endDelay: 8000,
        },
        {
          targets: ".not-flag",
          opacity: [1, 0.3],
          color: "#888888",
        },
        {
          fontSize: "1.25rem",
          lineHeight: "1.75rem",
          endDelay: 1000,
        },
        {
          letterSpacing: "30px",
        },
        {
          targets: ".not-flag",
          opacity: [0.3, 1],
          color: "#FFD700",
          duration: 500,
          endDelay: 0,
        },
        {
          targets: ".not-o",
          opacity: [1, 0.3],
          color: "#888888",
          endDelay: 1300,
        },
        {
          targets: ".not-o",
          opacity: [0.3, 1],
          color: "#FFD700",
          duration: 500,
          endDelay: 0,
        },
        {
          targets: ".not-f",
          opacity: [1, 0.3],
          color: "#888888",
          endDelay: 1300,
        },
        {
          targets: ".not-f",
          opacity: [0.3, 1],
          color: "#FFD700",
        },
        {
          fontSize: "1.875rem",
          lineHeight: "2.25rem",
        },
        {
          targets: ".letter",
          opacity: [1, 0.3],
          color: "#888888",
          duration: 500,
          endDelay: 200,
        },
        {
          targets: ".letter",
          opacity: [0.3, 1],
          color: "#FFD700",
          duration: 500,
        },
        {
          letterSpacing: "35px",
          endDelay: 1300,
        },
      ]}
    >
      <div
        className="font-bold select-none"
        style={{
          color: "#FFD700",
          letterSpacing: "35px",
          fontSize: "1.875rem",
          lineHeight: "2.25rem",
        }}
      >
        <div>
          <span class="letter f not-o flag">O</span>
          <span class="letter f not-o not-flag">M</span>
          <span class="letter f not-o not-flag">N</span>
          <span class="letter f not-o not-flag">I</span>
          <span class="letter f o not-flag">-</span>
          <span class="letter f o not-flag">F</span>
          <span class="letter f not-o not-flag">L</span>
          <span class="letter f not-o not-flag">A</span>
          <span class="letter f not-o not-flag">G</span>
          <span class="letter f not-o not-flag">S</span>
        </div>
        <div>
          <span class="letter f not-o flag">F</span>
          <span class="letter f not-o flag">L</span>
          <span class="letter f not-o flag">A</span>
          <span class="letter f o flag">G</span>
          <span class="letter f o flag">S</span>
          <span class="letter f o flag">-</span>
          <span class="letter f o flag">O</span>
          <span class="letter f not-o flag">M</span>
          <span class="letter f not-o flag">N</span>
          <span class="letter f not-o flag">I</span>
        </div>
        <div>
          <span class="letter f not-o flag">O</span>
          <span class="letter f not-o flag">M</span>
          <span class="letter f o flag">N</span>
          <span class="letter f o flag">I</span>
          <span class="letter f o flag">-</span>
          <span class="letter f o flag">F</span>
          <span class="letter f o flag">L</span>
          <span class="letter f o flag">A</span>
          <span class="letter f not-o flag">G</span>
          <span class="letter f not-o flag">S</span>
        </div>
        <div>
          <span class="letter f not-o flag">F</span>
          <span class="letter f o flag">L</span>
          <span class="letter f o flag">A</span>
          <span class="letter not-f o flag">G</span>
          <span class="letter not-f o flag">S</span>
          <span class="letter not-f o flag">-</span>
          <span class="letter not-f o flag">O</span>
          <span class="letter not-f o flag">M</span>
          <span class="letter not-f o flag">N</span>
          <span class="letter not-f not-o flag">I</span>
        </div>
        <div>
          <span class="letter f o flag">O</span>
          <span class="letter f o flag">M</span>
          <span class="letter f o flag">N</span>
          <span class="letter not-f o flag">I</span>
          <span class="letter not-f not-o flag">-</span>
          <span class="letter not-f not-o flag">F</span>
          <span class="letter not-f o flag">L</span>
          <span class="letter not-f o flag">A</span>
          <span class="letter not-f o flag">G</span>
          <span class="letter not-f o flag">S</span>
        </div>
        <div>
          <span class="letter f o flag">F</span>
          <span class="letter f o flag">L</span>
          <span class="letter f o flag">A</span>
          <span class="letter not-f not-o flag">G</span>
          <span class="letter not-f not-o flag">S</span>
          <span class="letter not-f not-o flag">-</span>
          <span class="letter not-f not-o flag">O</span>
          <span class="letter not-f o flag">M</span>
          <span class="letter not-f o flag">N</span>
          <span class="letter not-f o flag">I</span>
        </div>
        <div>
          <span class="letter f o flag">O</span>
          <span class="letter f o flag">M</span>
          <span class="letter f not-o flag">N</span>
          <span class="letter f not-o flag">I</span>
          <span class="letter f not-o flag">-</span>
          <span class="letter f not-o flag">F</span>
          <span class="letter f not-o flag">L</span>
          <span class="letter f not-o flag">A</span>
          <span class="letter f o flag">G</span>
          <span class="letter f o flag">S</span>
        </div>
        <div>
          <span class="letter f o flag">F</span>
          <span class="letter f o flag">L</span>
          <span class="letter f not-o flag">A</span>
          <span class="letter f not-o flag">G</span>
          <span class="letter f not-o flag">S</span>
          <span class="letter f not-o flag">-</span>
          <span class="letter f not-o flag">O</span>
          <span class="letter f not-o flag">M</span>
          <span class="letter f o flag">N</span>
          <span class="letter f o flag">I</span>
        </div>
        <div>
          <span class="letter f o flag">O</span>
          <span class="letter f o not-flag">M</span>
          <span class="letter f not-o not-flag">N</span>
          <span class="letter f not-o not-flag">I</span>
          <span class="letter f not-o not-flag">-</span>
          <span class="letter f not-o not-flag">F</span>
          <span class="letter f not-o not-flag">L</span>
          <span class="letter f not-o not-flag">A</span>
          <span class="letter f o not-flag">G</span>
          <span class="letter f o not-flag">S</span>
        </div>
        <div>
          <span class="letter f o flag">F</span>
          <span class="letter f o not-flag">L</span>
          <span class="letter f o not-flag">A</span>
          <span class="letter not-f not-o not-flag">G</span>
          <span class="letter not-f not-o not-flag">S</span>
          <span class="letter not-f not-o not-flag">-</span>
          <span class="letter not-f not-o not-flag">O</span>
          <span class="letter not-f o not-flag">M</span>
          <span class="letter not-f o not-flag">N</span>
          <span class="letter not-f o not-flag">I</span>
        </div>
        <div>
          <span class="letter f o flag">O</span>
          <span class="letter f o not-flag">M</span>
          <span class="letter f o not-flag">N</span>
          <span class="letter not-f o not-flag">I</span>
          <span class="letter not-f not-o not-flag">-</span>
          <span class="letter not-f not-o not-flag">F</span>
          <span class="letter not-f o not-flag">L</span>
          <span class="letter not-f o not-flag">A</span>
          <span class="letter not-f o not-flag">G</span>
          <span class="letter not-f o not-flag">S</span>
        </div>
        <div>
          <span class="letter f not-o flag">F</span>
          <span class="letter f o not-flag">L</span>
          <span class="letter f o not-flag">A</span>
          <span class="letter not-f o not-flag">G</span>
          <span class="letter not-f o not-flag">S</span>
          <span class="letter not-f o not-flag">-</span>
          <span class="letter not-f o not-flag">O</span>
          <span class="letter not-f o not-flag">M</span>
          <span class="letter not-f o not-flag">N</span>
          <span class="letter not-f not-o not-flag">I</span>
        </div>
        <div>
          <span class="letter f not-o flag">O</span>
          <span class="letter f not-o not-flag">M</span>
          <span class="letter f o not-flag">N</span>
          <span class="letter not-f o not-flag">I</span>
          <span class="letter not-f o not-flag">-</span>
          <span class="letter not-f o not-flag">F</span>
          <span class="letter not-f o not-flag">L</span>
          <span class="letter not-f o not-flag">A</span>
          <span class="letter not-f not-o not-flag">G</span>
          <span class="letter not-f not-o not-flag">S</span>
        </div>
        <div>
          <span class="letter f not-o flag">F</span>
          <span class="letter f not-o not-flag">L</span>
          <span class="letter f not-o not-flag">A</span>
          <span class="letter not-f o not-flag">G</span>
          <span class="letter not-f o not-flag">S</span>
          <span class="letter not-f o not-flag">-</span>
          <span class="letter not-f o not-flag">O</span>
          <span class="letter not-f not-o not-flag">M</span>
          <span class="letter not-f not-o not-flag">N</span>
          <span class="letter not-f not-o not-flag">I</span>
        </div>
        <div>
          <span class="letter f not-o flag">O</span>
          <span class="letter f not-o not-flag">M</span>
          <span class="letter f not-o not-flag">N</span>
          <span class="letter not-f not-o not-flag">I</span>
          <span class="letter not-f o not-flag">-</span>
          <span class="letter not-f o not-flag">F</span>
          <span class="letter not-f not-o not-flag">L</span>
          <span class="letter not-f not-o not-flag">A</span>
          <span class="letter not-f not-o not-flag">G</span>
          <span class="letter not-f not-o not-flag">S</span>
        </div>
      </div>
    </Anime>
  );
};

export default LetterWall;
