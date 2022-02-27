import React from "react";
import ReactAnime from "react-animejs";
import { Link } from "gatsby";

const { Anime } = ReactAnime;

const InfoPane = (props) => {
  return (
    <Anime
      className="p-4 w-full sm:w-1/2"
      animeConfig={{
        autoplay: false,
        loop: false,
      }}
      _onMouseEnter={[
        {
          targets: `#${props.paneId}`,
          duration: 200,
          scale: [1, 1.01],
          borderWidth: 4,
          opacity: [0.8, 0.9],
          easing: "linear",
        },
      ]}
      _onMouseLeave={[
        {
          targets: `#${props.paneId}`,
          duration: 200,
          scale: [1.01, 1],
          borderWidth: 2,
          opacity: [0.9, 0.8],
          easing: "linear",
        },
      ]}
    >
      <div
        id={props.paneId}
        className="pane flex flex-col justify-between border-2 h-full opacity-80 text-white p-4 overflow-x-auto"
      >
        <div>
          <p className="text-2xl xl:text-4xl font-bold mb-1">{props.title}</p>
          <hr className="border-2 mb-8 w-3/4" />
          <p className="text-lg xl:text-xl">{props.body}</p>
        </div>
        <Link
          to={props.link}
          className="border-2 text-center mx-4 mt-3 xl:mx-10 py-3"
        >
          View
        </Link>
      </div>
    </Anime>
  );
};

export default InfoPane;
