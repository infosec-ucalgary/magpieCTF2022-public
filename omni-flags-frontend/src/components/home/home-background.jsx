import React from "react";
import { StaticImage } from "gatsby-plugin-image";

import Home from "./home";

const HomeBackground = () => {
  return (
    <div className="grid">
      <StaticImage
        style={{
          gridArea: "1/1",
        }}
        className="h-screen overflow-hidden"
        layout="fullWidth"
        src="../../images/home-bg.jpg"
        placeholder="blurred"
      />
      <div
        style={{
          gridArea: "1/1",
          position: "relative",
          display: "grid",
        }}
      >
        <Home />
      </div>
    </div>
  );
};

export default HomeBackground;
