import React from "react";

import Map from "./map";
import MapInfo from "./map-info";
import Statement from "./statement";
import DistributionCenter from "./distribution-center";

const Impact = () => {
  return (
    <div className="w-full h-screen overflow-y-auto">
      <div className="px-4 sm:px-24 py-8 flex flex-col lg:flex-row items-center justify-evenly">
        <MapInfo />
        <Map />
      </div>
      <Statement />
      <DistributionCenter />
    </div>
  );
};

export default Impact;
