import React from "react";
import ReactAnime from "react-animejs";

const { Anime } = ReactAnime;

const MapInfo = () => {
  return (
    <div
      className="w-full lg:w-2/5 mx-10 my-10 p-3"
      style={{
        color: "#FFD700",
      }}
    >
      <Anime
        className=""
        animeConfig={{
          autoplay: true,
          loop: false,
        }}
        initial={[
          {
            targets: "#map-counter-0",
            innerText: [1, 9],
            easing: "easeOutSine",
            round: true,
            duration: 3000,
          },
        ]}
      >
        <div className="map-pane border-2 pt-4 pb-7 px-2 text-center flex flex-row justify-center bg-black overflow-x-auto">
          <div>
            <span className="text-3xl lg:text-4xl xl:text-5xl text-white">
              Distributing to{" "}
            </span>
            <span
              id="map-counter-0"
              className="text-4xl lg:text-5xl xl:text-6xl font-bold"
            >
              0
            </span>
            <p className="text-3xl lg:text-4xl xl:text-5xl text-white">
              global regions
            </p>
          </div>
        </div>
      </Anime>
    </div>
  );
};

export default MapInfo;
