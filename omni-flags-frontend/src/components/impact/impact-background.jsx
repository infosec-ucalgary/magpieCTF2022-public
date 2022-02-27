import React from "react";
import { StaticImage } from "gatsby-plugin-image";

import Impact from "./impact";

const ImpactBackground = () => {
  return (
    <div className="grid">
      <StaticImage
        style={{
          gridArea: "1/1",
        }}
        className="h-screen overflow-hidden"
        layout="fullWidth"
        src="../../images/impact-bg.jpg"
        placeholder="blurred"
      />
      <div
        style={{
          gridArea: "1/1",
          position: "relative",
          display: "grid",
        }}
      >
        <Impact />
      </div>
    </div>
  );
};

export default ImpactBackground;
