import React from "react";

import { StaticImage } from "gatsby-plugin-image";

const Executive = () => {
  return (
    <div className="about-pane w-3/4 my-20 mx-auto border-2 text-white p-6 sm:p-12 overflow-x-auto">
      <p className="text-center font-bold text-4xl mb-4">EXECUTIVE</p>
      <hr className="border-2 mb-8 w-3/4 mx-auto" />
      <div className="w-full flex justify-center">
        <StaticImage src="../../images/executive.jpg" placeholder="blurred" />
      </div>
    </div>
  );
};

export default Executive;
