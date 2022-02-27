import React from "react";

import { StaticImage } from "gatsby-plugin-image";

const DistributionCenter = () => {
  return (
    <div className="about-pane w-3/4 my-20 mx-auto border-2 text-white p-6 sm:p-12 overflow-x-auto">
      <p className="text-center font-bold text-3xl sm:text-4xl mb-4">
        DISTRIBUTION
      </p>
      <hr className="border-2 mb-8 w-3/4 mx-auto" />
      <div className="w-full flex flex-col lg:flex-row justify-evenly items-center">
        <StaticImage
          className="m-3"
          src="../../images/headquarters.jpg"
          placeholder="blurred"
        />
        <p className="w-full lg:w-1/2 text-2xl m-3 text-center">
          Our Omni-Flag distribution centers have done away with the costly use of "human" workers.
          Instead we use eco-conscious, low-cost semi-unmanned drones for the delivery of all
          flags.
          <br />
          <br />
          With Omni-Prime, you can have your flags delivered to you with our guaranteed One-Day Delivery!
          Just click 'One-Day Delivery' at checkout and one of our semi-unmanned drones will be at your door
          before you know it!
        </p>
      </div>
    </div>
  );
};

export default DistributionCenter;
