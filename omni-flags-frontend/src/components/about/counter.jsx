import React from "react";
import ReactAnime from "react-animejs";

const { Anime } = ReactAnime;

const Counter = () => {
  return (
    <div
      className="flex flex-col xl:flex-row items-center justify-around font-bold w-3/4 mx-auto"
      style={{
        color: "#FFD700",
      }}
    >
      <Anime
        className="my-4"
        animeConfig={{
          autoplay: true,
          loop: false,
        }}
        initial={[
          {
            targets: "#counter-0",
            innerText: [0, 352121],
            easing: "easeOutCubic",
            round: true,
            duration: 2000,
          },
        ]}
      >
        <div className="flex flex-col items-center justify-center">
          <div id="counter-0" className="text-5xl">
            0
          </div>
          <p className="text-3xl text-center">FLAGS PRODUCED</p>
        </div>
      </Anime>
      <Anime
        className="my-4"
        animeConfig={{
          autoplay: true,
          loop: false,
        }}
        initial={[
          {
            targets: "#counter-1",
            innerText: [0, 9973],
            easing: "easeOutCubic",
            round: true,
            duration: 8000,
          },
        ]}
      >
        <div className="flex flex-col items-center justify-center">
          <div id="counter-1" className="text-5xl">
            0
          </div>
          <p className="text-3xl text-center">CUSTOMERS</p>
        </div>
      </Anime>
      <Anime
        className="my-4"
        animeConfig={{
          autoplay: true,
          loop: false,
        }}
        initial={[
          {
            targets: "#counter-2",
            innerText: [0, 36],
            easing: "easeOutCubic",
            round: true,
            duration: 8000,
          },
        ]}
      >
        <div className="flex flex-col items-center justify-center">
          <div id="counter-2" className="text-5xl">
            0
          </div>
          <p className="text-3xl text-center">SATISFIED CUSTOMERS</p>
        </div>
      </Anime>
    </div>
  );
};

export default Counter;
