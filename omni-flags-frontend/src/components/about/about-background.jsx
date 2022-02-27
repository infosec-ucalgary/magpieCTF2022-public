import React from "react";
import { StaticImage } from "gatsby-plugin-image";

import About from "./about";

const AboutBackground = () => {
  return (
    <div className="grid">
      <StaticImage
        style={{
          gridArea: "1/1",
        }}
        className="h-screen overflow-hidden"
        layout="fullWidth"
        src="../../images/about-bg.jpg"
        placeholder="blurred"
      />
      <div
        style={{
          gridArea: "1/1",
          position: "relative",
          display: "grid",
        }}
      >
        <About />
      </div>
    </div>
  );
};

export default AboutBackground;
