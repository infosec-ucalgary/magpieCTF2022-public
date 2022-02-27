import React from "react";

import InfoPane from "./info-pane";
import LetterWall from "./letter-wall";

const Home = () => {
  return (
    <div className="flex flex-col xl:flex-row w-full h-screen overflow-y-auto">
      <div className="w-full xl:w-1/2 mt-10 hidden sm:flex items-center justify-center">
        <LetterWall />
      </div>
      <div className="w-full mt-10 flex sm:hidden items-center justify-center">
        <p
          className="text-center text-6xl font-bold p-4"
          style={{
            color: "#FFD700",
          }}
        >
          Omni-Flags Inc.
        </p>
      </div>
      <div className="w-full xl:w-1/2 px-4">
        <div className="h-2/5 flex items-center justify-center my-10 xl:my-0">
          <p
            className="text-center xl:text-left text-5xl xl:text-6xl font-bold p-4"
            style={{
              color: "#2b2b2b",
            }}
          >
            Working hard to make ourselves a more profitable future.
          </p>
        </div>
        <div className="h-3/5 flex flex-col sm:flex-row">
          <InfoPane
            paneId="pane-0"
            title="About Us"
            body="Omni-Flags was founded in 1968 by Flag Pioneers Ashford, Spencer, and Marcus. Their goal was to create a world
                  of harmony through flags. They envisioned a world in which the elite flagholders would bear the responsibility
                  of hoarding all flags so that the less fortunate wouldn't need to burden themselves, and could instead focus
                  on more productive uses of their time: flag production!"
            link="/about"
          />
          <InfoPane
            paneId="pane-1"
            title="Impact"
            body="We proudly support our environment and our workers. Whether it be our dedication to reducing flag spillage in North America or
                  our generous $5 an hour minimum wage for all factory workers, one can see that Omni-Flags Inc. is truly like a Family."
            link="/impact"
          />
        </div>
        <div className="flex flex-col sm:flex-row justify-center">
          <InfoPane
            paneId="pane-2"
            title="Employees"
            link="/employees"
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
